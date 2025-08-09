{{ config(materialized='table') }}

select
    m.message_id,
    c.channel_id,
    d.date_day as message_date,
    m.message_length,
    m.has_media,
    m.text
from {{ ref('stg_telegram_messages') }} m
join {{ ref('dim_channels') }} c on m.channel_name = c.channel_name
join {{ ref('dim_dates') }} d on m.message_date::date = d.date_day
