with raw_data as (
    select
        transaction_id::varchar as transaction_id,
        coalesce(customer_id::varchar, 'unknown') as customer_id,
        case
            when transaction_date ~ '^\d{2}-\d{2}-\d{4}$' then to_date(transaction_date, 'dd-mm-yyyy')
            when transaction_date ~ '^\d{4}-\d{2}-\d{2}$' then to_date(transaction_date, 'yyyy-mm-dd')
            else null
        end as transaction_date,
        product_id::varchar as product_id,
        product_name::varchar as product_name,
        coalesce(quantity, 
            (
                select 
                    percentile_cont(0.5) within group (order by quantity) 
            from 
                {{ source('raw_customer_transactions', 'customer_transactions') }}
            )
            ) as quantity,
        case
            when price ~ '^\d+(\.\d+)?$' then price::numeric
            when price = 'two hundred' then 200
            else null
        end as price,
        case
            when tax ~ '^\d+(\.\d+)?$' then tax::numeric
            when tax = 'fifteen' then 15
            else null
        end as tax
    from {{ source('raw_customer_transactions', 'customer_transactions') }}
)
select *
from raw_data
where transaction_date is not null
  and price is not null
  and tax is not null
