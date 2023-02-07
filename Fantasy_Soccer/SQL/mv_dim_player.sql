create materialized view data_models.mv_dim_player as (
    select distinct * from (
    select distinct split_part(player_link, '/', 4) as player_id, player, player_link from raw.players

    union all

    select distinct split_part(player_link, '/', 4) as player_id, player, player_link from raw.goalkeepers
    ) as _
);