# Java Wallet models

[https://github.com/burst-apps-team/burstcoin](https://github.com/burst-apps-team/burstcoin)

## Upgrade DB schema, new wallet version

Replace init-mysql.sql from [init-mysql.sql](https://github.com/burst-apps-team/burstcoin/blob/develop/init-mysql.sql)

Add first line: `USE java_wallet;`

Generate new models:

``` console
manage.py inspectdb --database java_wallet > java_wallet/models_new.py
```

Execute replaces:

``` console
sed -i '/from django.db import models/a from .fields import PositiveBigIntegerField, TimestampField' java_wallet/models_new.py
sed -i 's/models.BigIntegerField/PositiveBigIntegerField/g' java_wallet/models_new.py
sed -i 's/timestamp = models.IntegerField/timestamp = TimestampField/g' java_wallet/models_new.py
sed -i "s/block = models.ForeignKey(Block, models.DO_NOTHING)/block = models.ForeignKey(Block, models.DO_NOTHING, to_field='id')/g" java_wallet/models_new.py
sed -i 's/generation_signature = models.CharField(max_length=64)/generation_signature = models.BinaryField(max_length=64)/g' java_wallet/models_new.py
sed -i "s/previous_block = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)/previous_block = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='previous_block_r', to_field='id')/g" java_wallet/models_new.py
sed -i "s/next_block = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)/next_block = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='next_block_r', to_field='id')/g" java_wallet/models_new.py
```

Compare current and new model:

``` console
diff java_wallet/models.py java_wallet/models_new.py
```

Replace model

``` console
mv java_wallet/models_new.py java_wallet/models.py
```

Do changes in code if needed.

## Production and development

Add indexes in your wallet DB for speedups:

``` sql
CREATE INDEX height ON transaction(height);
CREATE INDEX timestamp ON transaction(timestamp);
CREATE INDEX height ON asset(height);
```
