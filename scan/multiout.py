import logging

from django.conf import settings
from django.core.cache import cache
from django.db import connection, transaction

from burst.constants import TxSubtypePayment, TxType
from burst.libs.multiout import MultiOutPack
from java_wallet.models import Block, Transaction
from scan.helpers.decorators import lock_decorator
from scan.models import MultiOut

logger = logging.getLogger(__name__)


def set_aggr_block_signature(service: str, height: int, block_signature: bytes) -> None:
    key = f"aggr:{service}:height:{height}"
    cache.set(key, block_signature, settings.AGGR_STORE_BLOCK_SIGNATURE)


def get_aggr_block_signature(service: str, height: int) -> bytes or None:
    key = f"aggr:{service}:height:{height}"
    return cache.get(key)


def group_list(lst: list or tuple, n: int):
    for i in range(0, len(lst), n):
        val = lst[i : i + n]
        if len(val) == n:
            yield tuple(val)


def find_last_actual_aggr_block(height: int) -> int:
    heights = (
        MultiOut.objects.values_list("height", flat=True)
        .filter(height__lte=height)
        .order_by("-height")
        .distinct()
    )

    for h in heights.iterator(16):
        bs0 = (
            Block.objects.using("java_wallet")
            .values_list("block_signature", flat=True)
            .filter(height=h)
            .first()
        )
        bs1 = get_aggr_block_signature("multiout", h)

        if bs1 is None:
            break

        if bs0 == bs1:
            return h

    return 0


def clean_out_all() -> None:
    cursor = connection.cursor()
    cursor.execute(f"TRUNCATE TABLE {MultiOut._meta.db_table}")


@lock_decorator(key="multiout", expire=60, auto_renewal=True)
def clean_out_all_cmd() -> None:
    clean_out_all()


def delete_greater_height(height: int) -> None:
    MultiOut.objects.filter(height__gt=height).delete()


@lock_decorator(key="multiout", expire=60, auto_renewal=True)
def delete_greater_height_cmd(height: int) -> None:
    delete_greater_height(height)


def aggregate_greater_height(height: int) -> None:
    _last_aggr_height = None

    txs = (
        Transaction.objects.using("java_wallet")
        .filter(
            type=TxType.PAYMENT,
            subtype__in={TxSubtypePayment.MULTI_OUT, TxSubtypePayment.MULTI_OUT_SAME},
            height__gt=height,
        )
        .order_by("height")
    )

    for tx in txs.iterator():
        instances = []
        logger.info("Aggregating height #%s transaction #%s", tx.height, tx.id)

        if tx.height != _last_aggr_height:
            # if process will aborted nothing bad
            set_aggr_block_signature("multiout", tx.height, tx.block.block_signature)
            _last_aggr_height = tx.height

        if tx.subtype == MultiOut.TxSubtype.MULTI_OUT:
            data = MultiOutPack().unpack_multi_out(tx.attachment_bytes)
            for r, amount in group_list(data, 2):
                instances.append(
                    MultiOut(
                        height=tx.height,
                        tx_id=tx.id,
                        sender_id=tx.sender_id,
                        recipient_id=r,
                        amount=amount,
                        tx_subtype=MultiOut.TxSubtype.MULTI_OUT,
                        tx_timestamp=tx.timestamp,
                    )
                )

        elif tx.subtype == MultiOut.TxSubtype.MULTI_OUT_SAME:
            recipients = MultiOutPack().unpack_multi_out_same(tx.attachment_bytes)
            amount = tx.amount / len(recipients)
            for r in recipients:
                instances.append(
                    MultiOut(
                        height=tx.height,
                        tx_id=tx.id,
                        sender_id=tx.sender_id,
                        recipient_id=r,
                        amount=amount,
                        tx_subtype=MultiOut.TxSubtype.MULTI_OUT_SAME,
                        tx_timestamp=tx.timestamp,
                    )
                )

        MultiOut.objects.bulk_create(instances)


@lock_decorator(key="multiout", expire=60, auto_renewal=True)
@transaction.atomic
def aggregate_cmd():
    logger.info("Start")

    last_block = (
        Block.objects.using("java_wallet")
        .values("height", "block_signature")
        .order_by("-height")
        .first()
    )

    if not last_block:
        logger.info("No blocks, sync node, exit")
        return

    last_aggr_height = (
        MultiOut.objects.values_list("height", flat=True).order_by("-height").first()
    )

    if last_aggr_height:
        last_aggr_block_signature = get_aggr_block_signature(
            "multiout", last_aggr_height
        )

        if (
            last_block["height"] == last_aggr_height
            and last_block["block_signature"] == last_aggr_block_signature
        ):
            # TODO: can optimize, last_aggr_height is last block with multiout, compare with last viewed in aggr
            logger.info("All aggregated already, exit")
            return
        else:
            # if heights are equal, condition above, signatures are not equal
            # if last_block['height'] < last_aggr_block['height'], aggr data have more data than real
            is_not_forked = last_block["height"] > last_aggr_height
            if is_not_forked:
                # if with height all right, compare block signature of last aggr height
                _block_signature = (
                    Block.objects.using("java_wallet")
                    .values_list("block_signature", flat=True)
                    .get(height=last_aggr_height)
                )
                is_not_forked = last_aggr_block_signature == _block_signature

            if is_not_forked:
                height = last_aggr_height
            else:
                logger.warning("Fork detected")
                height = find_last_actual_aggr_block(
                    min(last_block["height"], last_aggr_height)
                )
                logger.warning("Last actual block found: %d", height)
                if height == 0:
                    clean_out_all()
                    logger.warning("All aggregated data was cleaned out")
                else:
                    delete_greater_height(height)
                    logger.warning("Forked data was deleted greater height: %d", height)
    else:
        height = 0

    logger.info("Aggregating from height: %d", height)

    aggregate_greater_height(height)

    logger.info("Aggregation finished")
