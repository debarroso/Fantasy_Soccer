create table raw.shots
(
    match_id          text,
    match_date        date,
    season            integer,
    competition       text,
    minute            text,
    player_link       text,
    player            text,
    team              text,
    xg_shot           numeric,
    psxg_shot         numeric,
    outcome           text,
    distance          integer,
    body_part         text,
    notes             text,
    sca_1_player_link text,
    sca_1_player      text,
    sca_1_type        text,
    sca_2_player_link text,
    sca_2_player      text,
    sca_2_type        text
);

alter table raw.shots
    owner to postgres;

create index shots_competition_index
    on raw.shots (competition);

create index shots_distance_index
    on raw.shots (distance);

create index shots_match_date_index
    on raw.shots (match_date);

create index shots_match_id_index
    on raw.shots (match_id);

create index shots_outcome_index
    on raw.shots (outcome);

create index shots_player_link_index
    on raw.shots (player_link);

create index shots_sca_1_player_link_index
    on raw.shots (sca_1_player_link);

create index shots_sca_2_player_link_index
    on raw.shots (sca_2_player_link);

create index shots_team_index
    on raw.shots (team);

