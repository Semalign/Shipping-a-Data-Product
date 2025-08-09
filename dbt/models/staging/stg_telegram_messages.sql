{{ config(materialized='view') }}

with raw as (

    select
        message_id,
        channel_name,
        message_date::timestamp as message_date,
        text,
        media_path,
        raw_json
    from {{ source('raw', 'telegram_messages') }}

)

select
    message_id,
    channel_name,
    message_date,
    text,
    coalesce(length(text),0) as message_length,
    case when media_path is not null then true else false end as has_media,
    media_path,
    raw_json
from raw
