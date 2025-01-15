
select *
from {{ ref('fact_transactions') }}
where transaction_id is null or customer_id is null or transaction_date is null
