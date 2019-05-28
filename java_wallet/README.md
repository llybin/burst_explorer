# Development

After upgrading [init-mysql.sql](https://github.com/burst-apps-team/burstcoin/blob/develop/init-mysql.sql) from wallet repository add first line `USE data;`

# Production and development

Add indexes in your wallet DB for speedups:

```
CREATE INDEX height ON transaction(height);
CREATE INDEX timestamp ON transaction(timestamp);
CREATE INDEX height ON asset(height);
```
