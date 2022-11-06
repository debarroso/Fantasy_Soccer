create materialized view data_models.player_tackles as
(
    select l.match_id,
       l.match_date,
       l.team,
       l.home,
       t.opponent,
       t.competition,
       t.result,
       l.formation,
       l.starter,
       l.player_link,
       p.player,
       p.position,
       p.minutes,
       p.cards_yellow,
       p.cards_red,
       p.pressures,
       p.tackles,
       p.interceptions,
       p.blocks,
       p.tackles_won,
       p.tackles_def_3rd,
       p.tackles_mid_3rd,
       p.tackles_att_3rd,
       p.dribble_tackles,
       p.dribbles_vs,
       p.dribbled_past,
       p.pressure_regains,
       p.pressures_def_3rd,
       p.pressures_mid_3rd,
       p.pressures_att_3rd,
       p.blocked_shots,
       p.blocked_shots_saves,
       p.blocked_passes,
       p.tackles_interceptions,
       p.clearances,
       p.errors,
       p.fouls,
       p.ball_recoveries,
       p.aerials_won,
       p.aerials_lost
    from raw.players p
         inner join lineups l on p.player_link = l.player_link and p.match_id = l.match_id
         inner join data_models.team_agg t on l.match_id = t.match_id and l.team = t.team
);