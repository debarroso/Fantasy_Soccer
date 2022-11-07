create materialized view data_models.team_agg as
(
select l.*,
       trim(split_part(matchweek, '(', 1)) as competition,
       case
           when l.home is true then mm.away_team
           else mm.home_team
           end                             as opponent,
       case
           when mm.home_score = mm.away_score then 'tie'
           when l.home is true and mm.home_score > mm.away_score then 'win'
           when l.home is true and mm.home_score < mm.away_score then 'loss'
           when l.home is false and mm.home_score < mm.away_score then 'win'
           when l.home is false and mm.home_score > mm.away_score then 'loss'
           end                             as result,
       mm.venue,
       mm.venuetime,
       mm.attendance,
       mm.home_score,
       mm.home_xg,
       mm.home_manager,
       mm.home_record,
       mm.away_score,
       mm.away_xg,
       mm.away_manager,
       mm.away_record,
       ts_agg.assists,
       ts_agg.pens_made,
       ts_agg.pens_att,
       ts_agg.shots_total,
       ts_agg.shots_on_target,
       ts_agg.cards_yellow,
       ts_agg.cards_red,
       ts_agg.total_touches,
       ts_agg.total_pressures,
       ts_agg.tackles,
       ts_agg.interceptions,
       ts_agg.blocks,
       ts_agg.passes_completed,
       ts_agg.passes_attempted,
       ts_agg.passes_into_final_third,
       ts_agg.crosses,
       ts_agg.corners,
       ts_agg.fouls,
       ts_agg.fouled,
       ts_agg.offsides,
       ts_agg.aerials_won,
       ts_agg.aerials_lost

from match_metadata mm
         inner join
     (
         select distinct match_id, match_date, team, home, formation
         from lineups
     ) as l on mm.match_id = l.match_id
         inner join
     (
         select p.match_id                   as match_id,
                l_tmp.team                   as team,
                sum(assists)                 as assists,
                sum(pens_made)               as pens_made,
                sum(pens_att)                as pens_att,
                sum(shots_total)             as shots_total,
                sum(shots_on_target)         as shots_on_target,
                sum(cards_yellow)            as cards_yellow,
                sum(cards_red)               as cards_red,
                sum(touches)                 as total_touches,
                sum(pressures)               as total_pressures,
                sum(tackles)                 as tackles,
                sum(interceptions)           as interceptions,
                sum(blocks)                  as blocks,
                sum(passes_completed)        as passes_completed,
                sum(passes)                  as passes_attempted,
                sum(passes_into_final_third) as passes_into_final_third,
                sum(crosses)                 as crosses,
                sum(corner_kicks)            as corners,
                sum(fouls)                   as fouls,
                sum(fouled)                  as fouled,
                sum(offsides)                as offsides,
                sum(aerials_won)             as aerials_won,
                sum(aerials_lost)            as aerials_lost
         from lineups l_tmp
                  inner join players p on l_tmp.match_id = p.match_id and l_tmp.player_link = p.player_link
         group by p.match_id, team
     ) as ts_agg on ts_agg.match_id = l.match_id and ts_agg.team = l.team
)