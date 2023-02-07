create materialized view data_models.mv_dim_team as (
    select distinct split_part(team_link, '/', 4) as team_id, max(team) as team_name from
    (
        select home_team as team, home_team_link as team_link from raw.match_metadata
        union distinct
        select away_team as team, away_team_link as team_link from raw.match_metadata
    ) t
    group by team_id
    order by team_name
);