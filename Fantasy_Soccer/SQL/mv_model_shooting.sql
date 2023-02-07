create materialized view data_models.mv_model_shooting as (
    select
        match_id,
        match_date,
        competition,
        team_id,
        team,
        formation,
        player_link,
        player,
        starter,
        country_link,
        position,
        age,
        minutes,
        goals,
        assists,
        pens_made,
        pens_att,
        shots,
        shots_on_target,
        touches,
        xg,
        npxg,
        xg_assist,
        sca,
        gca,
        dribbles_completed,
        dribbles,
        assisted_shots,
        touches_att_3rd,
        touches_att_pen_area,
        miscontrols,
        dispossessed,
        passes_received,
        progressive_passes_received,
        fouled,
        pens_won,
        ball_recoveries,
        aerials_won,
        aerials_lost,
        aerials_won_pct
    from data_models.mv_player_matches
);