create table raw.match_metadata
(
    match_id       text not null
        constraint match_metadata_pk
            primary key,
    match_date     date,
    season         integer,
    competition    text,
    matchweek      text,
    home_team      text,
    home_team_link text,
    home_record    text,
    home_score     integer,
    home_manager   text,
    home_xg        numeric,
    away_team      text,
    away_team_link text,
    away_record    text,
    away_score     integer,
    away_manager   text,
    away_xg        numeric,
    venuetime      text,
    attendance     integer,
    venue          text,
    officials      text
);

alter table raw.match_metadata
    owner to postgres;

create index match_metadata_attendance_index
    on raw.match_metadata (attendance);

create index match_metadata_away_manager_index
    on raw.match_metadata (away_manager);

create index match_metadata_away_team_index
    on raw.match_metadata (away_team);

create index match_metadata_away_team_link_index
    on raw.match_metadata (away_team_link);

create index match_metadata_competition_index
    on raw.match_metadata (competition);

create index match_metadata_home_manager_index
    on raw.match_metadata (home_manager);

create index match_metadata_home_team_index
    on raw.match_metadata (home_team);

create index match_metadata_home_team_link_index
    on raw.match_metadata (home_team_link);

create index match_metadata_match_date_index
    on raw.match_metadata (match_date desc);

create index match_metadata_match_id_index
    on raw.match_metadata (match_id);

create index match_metadata_venue_index
    on raw.match_metadata (venue);

create index match_metadata_home_team_id_index
    on raw.match_metadata (split_part(home_team_link, '/'::text, 4));

create index match_metadata_away_team_id_index
    on raw.match_metadata (split_part(away_team_link, '/'::text, 4));

