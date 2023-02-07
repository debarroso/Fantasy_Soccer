create materialized view data_models.mv_team_matches as (
    select
        t.*,
        mm.match_id,
        mm.match_date,
        mm.season,
        mm.competition,
        mm.away_team as opponent,
        split_part(mm.away_team_link, '/', 4) as opponent_id,
        TRUE as home,
        CASE
            WHEN mm.home_score > mm.away_score THEN 'win'
            WHEN mm.home_score = mm.away_score THEN 'draw'
            ELSE 'loss'
        END AS result,
        mm.home_score as goals,
        mm.home_xg as xg,
        mm.away_score as goals_allowed,
        mm.away_xg as xg_allowed,
        mm.venue,
        mm.attendance
    from data_models.mv_dim_team t
    inner join raw.match_metadata mm on split_part(mm.home_team_link, '/', 4) = team_id

    union all

    select
        t.*,
        mm.match_id,
        mm.match_date,
        mm.season,
        mm.competition,
        mm.home_team as opponent,
        split_part(mm.home_team_link, '/', 4) as opponent_id,
        FALSE as home,
        CASE
            WHEN mm.home_score < mm.away_score THEN 'win'
            WHEN mm.home_score = mm.away_score THEN 'draw'
            ELSE 'loss'
        END AS result,
        mm.away_score as goals,
        mm.away_xg as xg,
        mm.home_score as goals_allowed,
        mm.home_xg as xg_allowed,
        mm.venue,
        mm.attendance
    from data_models.mv_dim_team t
    inner join raw.match_metadata mm on split_part(mm.away_team_link, '/', 4) = team_id
);