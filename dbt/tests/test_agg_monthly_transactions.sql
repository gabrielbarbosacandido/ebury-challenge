select *
from {{ ref('agg_monthly_transactions') }}
where transaction_month is null or transaction_count < 0
