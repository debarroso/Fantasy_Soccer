create materialized view data_models.player_shot_duos as
(
    select match_id,
       match_date,
       player_link,
       case
           when sca_1_player_link is null then 'self'
           else sca_1_player_link
           end as sca_1_player,
       count(*) as shots
    from raw.shots
    group by match_id, match_date, player_link, sca_1_player_link
);