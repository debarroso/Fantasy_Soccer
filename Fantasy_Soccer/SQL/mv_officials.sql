create materialized view data_models.officials as
(
select officials_exploded.*,
       stats.match_date,
       stats.competition,
       stats.venue,
       stats.venuetime,
       stats.attendance,
       stats.fouls,
       stats.tackles,
       stats.cards_yellow,
       stats.cards_red
from (
         select match_id,
                match_date,
                competition,
                venue,
                venuetime,
                attendance,
                sum(fouls)        as fouls,
                sum(tackles)      as tackles,
                sum(cards_yellow) as cards_yellow,
                sum(cards_red)    as cards_red
         from data_models.team_agg
         group by match_id, match_date, competition, venue, venuetime, attendance
     ) as stats
         inner join
     (
         select match_id,
                trim(split_part(a[1], '(', 1)) as referee,
                trim(split_part(a[2], '(', 1)) as ar1,
                trim(split_part(a[3], '(', 1)) as ar2,
                trim(split_part(a[4], '(', 1)) as fourth,
                trim(split_part(a[5], '(', 1)) as var
         from (
                  select match_id, regexp_split_to_array(officials, ',') as a
                  from raw.match_metadata
                  group by match_id, regexp_split_to_array(officials, ',')
              ) as t
     ) as officials_exploded on stats.match_id = officials_exploded.match_id
)