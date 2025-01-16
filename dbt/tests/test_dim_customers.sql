select *
from {{ ref('dim_customers') }}
where customer_id is null
