create table raw.players
(
    match_id                    text not null,
    match_date                  date,
    season                      integer,
    competition                 text,
    player_link                 text not null,
    player                      text,
    shirtnumber                 integer,
    country_link                text,
    nationality                 text,
    position                    text,
    age                         text,
    minutes                     integer,
    goals                       integer,
    assists                     integer,
    pens_made                   integer,
    pens_att                    integer,
    shots                       integer,
    shots_on_target             integer,
    cards_yellow                integer,
    cards_red                   integer,
    touches                     integer,
    tackles                     integer,
    interceptions               integer,
    blocks                      integer,
    xg                          numeric,
    npxg                        numeric,
    xg_assist                   numeric,
    sca                         integer,
    gca                         integer,
    passes_completed            integer,
    passes                      integer,
    passes_pct                  numeric,
    progressive_passes          integer,
    dribbles_completed          integer,
    dribbles                    integer,
    passes_total_distance       integer,
    passes_progressive_distance integer,
    passes_completed_short      integer,
    passes_short                integer,
    passes_pct_short            numeric,
    passes_completed_medium     integer,
    passes_medium               integer,
    passes_pct_medium           numeric,
    passes_completed_long       integer,
    passes_long                 integer,
    passes_pct_long             numeric,
    pass_xa                     numeric,
    assisted_shots              integer,
    passes_into_final_third     integer,
    passes_into_penalty_area    integer,
    crosses_into_penalty_area   integer,
    passes_live                 integer,
    passes_dead                 integer,
    passes_free_kicks           integer,
    through_balls               integer,
    passes_switches             integer,
    crosses                     integer,
    throw_ins                   integer,
    corner_kicks                integer,
    corner_kicks_in             integer,
    corner_kicks_out            integer,
    corner_kicks_straight       integer,
    passes_offsides             integer,
    passes_blocked              integer,
    tackles_won                 integer,
    tackles_def_3rd             integer,
    tackles_mid_3rd             integer,
    tackles_att_3rd             integer,
    dribble_tackles             integer,
    dribbles_vs                 integer,
    dribble_tackles_pct         numeric,
    dribbled_past               integer,
    blocked_shots               integer,
    blocked_passes              integer,
    tackles_interceptions       integer,
    clearances                  integer,
    errors                      integer,
    touches_def_pen_area        integer,
    touches_def_3rd             integer,
    touches_mid_3rd             integer,
    touches_att_3rd             integer,
    touches_att_pen_area        integer,
    touches_live_ball           integer,
    dribbles_completed_pct      numeric,
    miscontrols                 integer,
    dispossessed                integer,
    passes_received             integer,
    progressive_passes_received integer,
    cards_yellow_red            integer,
    fouls                       integer,
    fouled                      integer,
    offsides                    integer,
    pens_won                    integer,
    pens_conceded               integer,
    own_goals                   integer,
    ball_recoveries             integer,
    aerials_won                 integer,
    aerials_lost                integer,
    aerials_won_pct             numeric,
    constraint players_pk
        primary key (match_id, player_link)
);

alter table raw.players
    owner to postgres;

create index players_assists_index
    on raw.players (assists);

create index players_cards_red_index
    on raw.players (cards_red);

create index players_cards_yellow_index
    on raw.players (cards_yellow);

create index players_competition_index
    on raw.players (competition);

create index players_goals_index
    on raw.players (goals);

create index players_match_date_index
    on raw.players (match_date desc);

create index players_match_id_index
    on raw.players (match_id);

create index players_minutes_index
    on raw.players (minutes);

create index players_pens_att_index
    on raw.players (pens_att);

create index players_pens_made_index
    on raw.players (pens_made);

create index players_player_index
    on raw.players (player);

create index players_player_link_index
    on raw.players (player_link);

create index players_position_index
    on raw.players (position);

create index players_shots_index
    on raw.players (shots);

create index players_shots_on_target_index
    on raw.players (shots_on_target);

create index players_tackles_index
    on raw.players (tackles);

create index players_touches_index
    on raw.players (touches);

