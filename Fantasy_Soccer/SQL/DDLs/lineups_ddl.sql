create table raw.lineups
(
    match_id    text not null,
    match_date  date,
    season      integer,
    competition text,
    team        text,
    home        boolean,
    formation   text,
    starter     boolean,
    player_link text not null,
    constraint lineups_pk
        primary key (match_id, player_link)
);

alter table raw.lineups
    owner to postgres;

create index lineups_competition_index
    on raw.lineups (competition);

create index lineups_home_index
    on raw.lineups (home);

create index lineups_match_date_index
    on raw.lineups (match_date desc);

create index lineups_match_id_index
    on raw.lineups (match_id);

create index lineups_player_link_index
    on raw.lineups (player_link);

create index lineups_starter_index
    on raw.lineups (starter);

create index lineups_team_index
    on raw.lineups (team);

