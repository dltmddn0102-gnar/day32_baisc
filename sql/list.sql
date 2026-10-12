SELECT
    id,
    label,
    weight,
    fee,
    rule_version
FROM shipping_quotes
ORDER BY id DESC
LIMIT 100;
