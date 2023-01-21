INSERT INTO raw.lineups (
    match_id,
    match_date,
    season,
    competition,
    team,
    home,
    formation,
    starter,
    player_link
) SELECT * FROM staging.lineups
ON CONFLICT ON CONSTRAINT lineups_pk
DO UPDATE SET
    match_id = excluded.match_id,
    match_date = excluded.match_date,
    season = excluded.season,
    competition = excluded.competition,
    team = excluded.team,
    home = excluded.home,
    formation = excluded.formation,
    starter = excluded.starter,
    player_link = excluded.player_link;