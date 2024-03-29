INSERT INTO raw.match_metadata (
    match_id,
    match_date,
    season,
    competition,
    matchweek,
    home_team,
    home_team_link,
    home_record,
    home_score,
    home_manager,
    home_xg,
    away_team,
    away_team_link,
    away_record,
    away_score,
    away_manager,
    away_xg,
    venuetime,
    attendance,
    venue,
    officials
) SELECT * FROM staging.match_metadata
ON CONFLICT ON CONSTRAINT match_metadata_pk
DO UPDATE SET
    match_id = excluded.match_id,
    match_date = excluded.match_date,
    season = excluded.season,
    competition = excluded.competition,
    matchweek = excluded.matchweek,
    home_team = excluded.home_team,
    home_team_link = excluded.home_team_link,
    home_record = excluded.home_record,
    home_score = excluded.home_score,
    home_manager = excluded.home_manager,
    home_xg = excluded.home_xg,
    away_team = excluded.away_team,
    away_team_link = excluded.away_team_link,
    away_record = excluded.away_record,
    away_score = excluded.away_score,
    away_manager = excluded.away_manager,
    away_xg = excluded.away_xg,
    venuetime = excluded.venuetime,
    attendance = excluded.attendance,
    venue = excluded.venue,
    officials = excluded.officials;