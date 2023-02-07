create table raw.goalkeepers
(
    match_id                        text not null,
    match_date                      date,
    season                          integer,
    competition                     text,
    player_link                     text not null,
    player                          text,
    country_link                    text,
    nationality                     text,
    age                             text,
    minutes                         integer,
    gk_shots_on_target_against      integer,
    gk_goals_against                integer,
    gk_saves                        integer,
    gk_save_pct                     numeric,
    gk_psxg                         numeric,
    gk_passes_completed_launched    integer,
    gk_passes_launched              integer,
    gk_passes_pct_launched          numeric,
    gk_passes                       integer,
    gk_passes_throws                integer,
    gk_pct_passes_launched          numeric,
    gk_passes_length_avg            numeric,
    gk_goal_kicks                   integer,
    gk_pct_goal_kicks_launched      numeric,
    gk_goal_kick_length_avg         numeric,
    gk_crosses                      integer,
    gk_crosses_stopped              integer,
    gk_crosses_stopped_pct          numeric,
    gk_def_actions_outside_pen_area integer,
    gk_avg_distance_def_actions     numeric,
    constraint goalkeepers_pk
        primary key (match_id, player_link)
);

alter table raw.goalkeepers
    owner to postgres;

create index goalkeepers_competition_index
    on raw.goalkeepers (competition);

create index goalkeepers_match_date_index
    on raw.goalkeepers (match_date desc);

create index goalkeepers_match_id_index
    on raw.goalkeepers (match_id);

create index goalkeepers_player_index
    on raw.goalkeepers (player);

create index goalkeepers_player_link_index
    on raw.goalkeepers (player_link);

create index goalkeepers_season_index
    on raw.goalkeepers (season);

