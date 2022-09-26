create materialized view data_models.player_shot_trios as
(
    select match_id,
       match_date,
       player_link,
       case
           when sca_1_player_link is null then 'self'
           else sca_1_player_link
           end as sca_1_player,
       sca_2_player_link as sca_2_player,
       count(*) as shots
    from raw.shots
    group by match_id, match_date, player_link, sca_1_player_link, sca_2_player_link
);