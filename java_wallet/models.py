# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .fields import PositiveBigIntegerField, TimestampField


class Account(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    creation_height = models.IntegerField()
    public_key = models.CharField(max_length=32, blank=True, null=True)
    key_height = models.IntegerField(blank=True, null=True)
    balance = PositiveBigIntegerField()
    unconfirmed_balance = PositiveBigIntegerField()
    forged_balance = PositiveBigIntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account'
        unique_together = (('id', 'height'),)


class AccountAsset(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    account_id = PositiveBigIntegerField()
    asset_id = PositiveBigIntegerField()
    quantity = PositiveBigIntegerField()
    unconfirmed_quantity = PositiveBigIntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account_asset'
        unique_together = (('account_id', 'asset_id', 'height'),)


class Alias(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    account_id = PositiveBigIntegerField()
    alias_name = models.CharField(max_length=100)
    alias_name_lower = models.CharField(max_length=100)
    alias_uri = models.TextField()
    timestamp = TimestampField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'alias'
        unique_together = (('id', 'height'),)


class AliasOffer(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    price = PositiveBigIntegerField()
    buyer_id = PositiveBigIntegerField(blank=True, null=True)
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'alias_offer'
        unique_together = (('id', 'height'),)


class AskOrder(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    account_id = PositiveBigIntegerField()
    asset_id = PositiveBigIntegerField()
    price = PositiveBigIntegerField()
    quantity = PositiveBigIntegerField()
    creation_height = models.IntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ask_order'
        unique_together = (('id', 'height'),)


class Asset(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField(unique=True)
    account_id = PositiveBigIntegerField()
    name = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    quantity = PositiveBigIntegerField()
    decimals = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'asset'


class AssetTransfer(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField(unique=True)
    asset_id = PositiveBigIntegerField()
    sender_id = PositiveBigIntegerField()
    recipient_id = PositiveBigIntegerField()
    quantity = PositiveBigIntegerField()
    timestamp = TimestampField()
    height = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'asset_transfer'


class At(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    creator_id = PositiveBigIntegerField()
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    version = models.SmallIntegerField()
    csize = models.IntegerField()
    dsize = models.IntegerField()
    c_user_stack_bytes = models.IntegerField()
    c_call_stack_bytes = models.IntegerField()
    creation_height = models.IntegerField()
    ap_code = models.TextField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'at'
        unique_together = (('id', 'height'),)


class AtState(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    at_id = PositiveBigIntegerField()
    state = models.TextField()
    prev_height = models.IntegerField()
    next_height = models.IntegerField()
    sleep_between = models.IntegerField()
    prev_balance = PositiveBigIntegerField()
    freeze_when_same_balance = models.IntegerField()
    min_activate_amount = PositiveBigIntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'at_state'
        unique_together = (('at_id', 'height'),)


class BidOrder(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    account_id = PositiveBigIntegerField()
    asset_id = PositiveBigIntegerField()
    price = PositiveBigIntegerField()
    quantity = PositiveBigIntegerField()
    creation_height = models.IntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bid_order'
        unique_together = (('id', 'height'),)


class Block(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField(unique=True)
    version = models.IntegerField()
    timestamp = TimestampField(unique=True)
    previous_block = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='previous_block_r', to_field='id')
    total_amount = PositiveBigIntegerField()
    total_fee = PositiveBigIntegerField()
    payload_length = models.IntegerField()
    generator_public_key = models.CharField(max_length=32)
    previous_block_hash = models.CharField(max_length=32, blank=True, null=True)
    cumulative_difficulty = models.TextField()
    base_target = PositiveBigIntegerField()
    next_block = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='next_block_r', to_field='id')
    height = models.IntegerField(unique=True)
    generation_signature = models.BinaryField(max_length=64)
    block_signature = models.CharField(max_length=64)
    payload_hash = models.CharField(max_length=32)
    generator_id = PositiveBigIntegerField()
    nonce = PositiveBigIntegerField()
    ats = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'block'


class Escrow(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    sender_id = PositiveBigIntegerField()
    recipient_id = PositiveBigIntegerField()
    amount = PositiveBigIntegerField()
    required_signers = models.IntegerField(blank=True, null=True)
    deadline = models.IntegerField()
    deadline_action = models.IntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'escrow'
        unique_together = (('id', 'height'),)


class EscrowDecision(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    escrow_id = PositiveBigIntegerField()
    account_id = PositiveBigIntegerField()
    decision = models.IntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'escrow_decision'
        unique_together = (('escrow_id', 'account_id', 'height'),)


class Goods(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    seller_id = PositiveBigIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    timestamp = TimestampField()
    quantity = models.IntegerField()
    price = PositiveBigIntegerField()
    delisted = models.IntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goods'
        unique_together = (('id', 'height'),)


class Peer(models.Model):
    address = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'peer'


class Purchase(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    buyer_id = PositiveBigIntegerField()
    goods_id = PositiveBigIntegerField()
    seller_id = PositiveBigIntegerField()
    quantity = models.IntegerField()
    price = PositiveBigIntegerField()
    deadline = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    nonce = models.CharField(max_length=32, blank=True, null=True)
    timestamp = TimestampField()
    pending = models.IntegerField()
    goods = models.TextField(blank=True, null=True)
    goods_nonce = models.CharField(max_length=32, blank=True, null=True)
    refund_note = models.TextField(blank=True, null=True)
    refund_nonce = models.CharField(max_length=32, blank=True, null=True)
    has_feedback_notes = models.IntegerField()
    has_public_feedbacks = models.IntegerField()
    discount = PositiveBigIntegerField()
    refund = PositiveBigIntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'purchase'
        unique_together = (('id', 'height'),)


class PurchaseFeedback(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    feedback_data = models.TextField()
    feedback_nonce = models.CharField(max_length=32)
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'purchase_feedback'


class PurchasePublicFeedback(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    public_feedback = models.TextField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'purchase_public_feedback'


class RewardRecipAssign(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    account_id = PositiveBigIntegerField()
    prev_recip_id = PositiveBigIntegerField()
    recip_id = PositiveBigIntegerField()
    from_height = models.IntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'reward_recip_assign'
        unique_together = (('account_id', 'height'),)


class Subscription(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField()
    sender_id = PositiveBigIntegerField()
    recipient_id = PositiveBigIntegerField()
    amount = PositiveBigIntegerField()
    frequency = models.IntegerField()
    time_next = models.IntegerField()
    height = models.IntegerField()
    latest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subscription'
        unique_together = (('id', 'height'),)


class Trade(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    asset_id = PositiveBigIntegerField()
    block_id = PositiveBigIntegerField()
    ask_order_id = PositiveBigIntegerField()
    bid_order_id = PositiveBigIntegerField()
    ask_order_height = models.IntegerField()
    bid_order_height = models.IntegerField()
    seller_id = PositiveBigIntegerField()
    buyer_id = PositiveBigIntegerField()
    quantity = PositiveBigIntegerField()
    price = PositiveBigIntegerField()
    timestamp = TimestampField()
    height = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trade'
        unique_together = (('ask_order_id', 'bid_order_id'),)


class Transaction(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField(unique=True)
    deadline = models.SmallIntegerField()
    sender_public_key = models.CharField(max_length=32)
    recipient_id = PositiveBigIntegerField(blank=True, null=True)
    amount = PositiveBigIntegerField()
    fee = PositiveBigIntegerField()
    height = models.IntegerField()
    block = models.ForeignKey(Block, models.DO_NOTHING, to_field='id')
    signature = models.CharField(max_length=64, blank=True, null=True)
    timestamp = TimestampField()
    type = models.IntegerField()
    subtype = models.IntegerField()
    sender_id = PositiveBigIntegerField()
    block_timestamp = TimestampField()
    full_hash = models.CharField(unique=True, max_length=32)
    referenced_transaction_fullhash = models.CharField(max_length=32, blank=True, null=True)
    attachment_bytes = models.TextField(blank=True, null=True)
    version = models.IntegerField()
    has_message = models.IntegerField()
    has_encrypted_message = models.IntegerField()
    has_public_key_announcement = models.IntegerField()
    ec_block_height = models.IntegerField(blank=True, null=True)
    ec_block_id = PositiveBigIntegerField(blank=True, null=True)
    has_encrypttoself_message = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'transaction'


class UnconfirmedTransaction(models.Model):
    db_id = models.BigAutoField(primary_key=True)
    id = PositiveBigIntegerField(unique=True)
    expiration = models.IntegerField()
    transaction_height = models.IntegerField()
    fee_per_byte = PositiveBigIntegerField()
    timestamp = TimestampField()
    transaction_bytes = models.TextField()
    height = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'unconfirmed_transaction'


class Version(models.Model):
    next_update = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'version'
