
select
    transaction_id,
    customer_id,
    transaction_date,
    product_id,
    product_name,
    quantity,
    price,
    tax,
    (quantity * price + tax) as total_value
from {{ ref('clean_customer_transactions') }}
