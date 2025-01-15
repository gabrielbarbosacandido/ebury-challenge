with customers as (
    select distinct
        customer_id
    from {{ ref('clean_customer_transactions') }}
)
select
    row_number() over (order by customer_id) as customer_key,
    customer_id
from customers
