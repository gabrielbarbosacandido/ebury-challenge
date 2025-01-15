
with monthly_transactions as (
    select
        customer_id,
        date_trunc('month'
    , transaction_date) as transaction_month,
        count(transaction_id) as transaction_count,
        sum(quantity) as total_quantity,
        sum(price * quantity + tax) as total_value
    from {{ ref('fact_transactions') }}
    group by customer_id
    , transaction_month
)
select *
from monthly_transactions
