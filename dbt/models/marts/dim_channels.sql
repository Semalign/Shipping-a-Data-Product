{{ config(materialized='table') }}

with channels as (
    select distinct channel_name
    from {{ ref('stg_telegram_messages') }}
)

select
    row_number() over () as channel_id,
    channel_name,
    null as channel_display_name,
    null as channel_description
from channels
