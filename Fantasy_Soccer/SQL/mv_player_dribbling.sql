create materialized view data_models.player_dribbling as
(
    select l.match_id,
       l.match_date,
       l.team,
       l.home,
       l.formation,
       l.starter,
       l.player_link,
       p.player,
       p.position,
       p.minutes,
       p.touches,
       p.carries,
       p.progressive_carries,
       p.dribbles_completed,
       p.dribbles,
       p.passes_pressure as passes_under_pressure,
       p.errors,
       p.players_dribbled_past,
       p.nutmegs,
       p.carry_distance,
       p.carry_progressive_distance,
       p.carries_into_final_third,
       p.carries_into_penalty_area,
       p.miscontrols,
       p.dispossessed,
       p.pass_targets,
       p.passes_received,
       p.fouled
    from raw.players p
         inner join raw.lineups l on p.player_link = l.player_link and p.match_id = l.match_id
);