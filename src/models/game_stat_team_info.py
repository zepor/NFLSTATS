from mongoengine import DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField, DictField


class int_returns(EmbeddedDocument):
    longest = IntField()
    longest_touchdown = IntField()
    avg_yards = IntField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class passing(EmbeddedDocument):
    longest = IntField()
    longest_touchdown = IntField()
    air_yards = IntField()
    attempts = IntField()
    avg_pocket_time = DecimalField()
    avg_yards = DecimalField()
    batted_passes = IntField()
    blitzes = IntField()
    cmp_pct = DecimalField()
    completions = IntField()
    defended_passes = IntField()
    dropped_passes = IntField()
    first_downs = IntField()
    hurries = IntField()
    int_touchdowns = IntField()
    interceptions = IntField()
    knockdowns = IntField()
    net_yards = IntField()
    on_target_throws = IntField()
    pocket_time = IntField()
    poor_throws = IntField()
    rating = DecimalField()
    redzone_attempts = IntField()
    sack_yards = IntField()
    sacks = IntField()
    spikes = IntField()
    throw_aways = IntField()
    touchdowns = IntField()
    yards = IntField()


class receiving(EmbeddedDocument):
    longest = IntField()
    longest_touchdown = IntField()
    air_yards = IntField()
    avg_yards = DecimalField()
    broken_tackles = IntField()
    catchable_passes = IntField()
    dropped_passes = IntField()
    first_downs = IntField()
    receptions = IntField()
    redzone_targets = IntField()
    targets = IntField()
    touchdowns = IntField()
    yards = IntField()
    yards_after_catch = IntField()
    yards_after_contact = IntField()


class defense(EmbeddedDocument):
    assists = IntField()
    batted_passes = IntField()
    blitzes = IntField()
    combined = IntField()
    def_comps = IntField()
    def_targets = IntField()
    forced_fumbles = IntField()
    fourth_down_stops = IntField()
    fumble_recoveries = IntField()
    hurries = IntField()
    interceptions = IntField()
    knockdowns = IntField()
    misc_assists = IntField()
    misc_forced_fumbles = IntField()
    misc_fumble_recoveries = IntField()
    misc_tackles = IntField()
    missed_tackles = IntField()
    passes_defended = IntField()
    qb_hits = IntField()
    sack_yards = IntField()
    sacks = IntField()
    safeties = IntField()
    sp_assists = IntField()
    sp_blocks = IntField()
    sp_forced_fumbles = IntField()
    sp_fumble_recoveries = IntField()
    sp_tackles = IntField()
    tackles = IntField()
    three_and_outs_forced = IntField()
    tloss = IntField()
    tloss_yards = IntField()


class thirddown(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class fourthdown(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class goaltogo(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class redzone(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class kicks(EmbeddedDocument):
    attempts = IntField()
    blocked = IntField()
    made = IntField()
    missed = IntField()
    pct = DecimalField()


class field_goals(EmbeddedDocument):
    longest = IntField()
    attempts = IntField()
    attempts_19 = IntField()
    attempts_29 = IntField()
    attempts_39 = IntField()
    attempts_49 = IntField()
    attempts_50 = IntField()
    avg_yards = DecimalField()
    blocked = IntField()
    made = IntField()
    made_19 = IntField()
    made_29 = IntField()
    made_39 = IntField()
    made_49 = IntField()
    made_50 = IntField()
    missed = IntField()
    net_attempts = IntField()
    pct = DecimalField()
    yards = IntField()


class punts(EmbeddedDocument):
    longest = IntField()
    attempts = IntField()
    avg_hang_time = IntField()
    avg_net_yards = DecimalField()
    avg_yards = DecimalField()
    blocked = IntField()
    hang_time = IntField()
    inside_20 = IntField()
    net_yards = IntField()
    return_yards = IntField()
    touchbacks = IntField()
    yards = IntField()


class rushing(EmbeddedDocument):
    longest = IntField()
    longest_touchdown = IntField()
    attempts = IntField()
    avg_yards = DecimalField()
    broken_tackles = IntField()
    first_downs = IntField()
    kneel_downs = IntField()
    redzone_attempts = IntField()
    scrambles = IntField()
    tlost = IntField()
    tlost_yards = IntField()
    touchdowns = IntField()
    yards = IntField()
    yards_after_contact = IntField()


class kick_returns(EmbeddedDocument):
    longest = IntField()
    longest_touchdown = IntField()
    avg_yards = DecimalField()
    faircatches = IntField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class punt_returns(EmbeddedDocument):
    longest = IntField()
    longest_touchdown = IntField()
    avg_yards = DecimalField()
    faircatches = IntField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class misc_returns(EmbeddedDocument):
    blk_fg_touchdowns = IntField()
    blk_punt_touchdowns = IntField()
    ez_rec_touchdowns = IntField()
    fg_return_touchdowns = IntField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class conversions(EmbeddedDocument):
    defense_attempts = IntField()
    defense_successes = IntField()
    pass_attempts = IntField()
    pass_successes = IntField()
    rush_attempts = IntField()
    rush_successes = IntField()
    turnover_successes = IntField()


class kickoffs(EmbeddedDocument):
    endzone = IntField()
    inside_20 = IntField()
    kickoffs = IntField()
    out_of_bounds = IntField()
    return_yards = IntField()
    total_endzone = IntField()
    touchbacks = IntField()
    yards = IntField()


class fumbles(EmbeddedDocument):
    ez_rec_tds = IntField()
    forced_fumbles = IntField()
    fumbles = IntField()
    lost_fumbles = IntField()
    opp_rec = IntField()
    opp_rec_tds = IntField()
    opp_rec_yards = IntField()
    out_of_bounds = IntField()
    own_rec = IntField()
    own_rec_tds = IntField()
    own_rec_yards = IntField()


class penalties(EmbeddedDocument):
    penalties = IntField()
    yards = IntField()


class touchdowns(EmbeddedDocument):
    fumble_return = IntField()
    int_return = IntField()
    kick_return = IntField()
    other = IntField()
    passing = IntField()
    punt_return = IntField()
    rush = IntField()
    total = IntField()
    total_return = IntField()


class interceptions(EmbeddedDocument):
    interceptions = IntField()
    return_yards = IntField()
    returned = IntField()


class first_downs(EmbeddedDocument):
    passing = IntField()
    penalty = IntField()
    rush = IntField()
    total = IntField()


class GameStatsTeamInfo(Document):
    _id = StringField(required=True)
    game_id = StringField(required=True)
    season_type = StringField(required=True)
    season_year = IntField(required=True)
    week = IntField(required=True)
    team = StringField(required=True)
    stats = DictField()
    int_returns = EmbeddedDocumentListField(int_returns)
    kick_returns = EmbeddedDocumentListField(kick_returns)
    misc_returns = EmbeddedDocumentListField(misc_returns)
    passing = EmbeddedDocumentListField(passing)
    punts = EmbeddedDocumentListField(punts)
    receiving = EmbeddedDocumentListField(receiving)
    rushing = EmbeddedDocumentListField(rushing)
    fumbles = EmbeddedDocumentListField(fumbles)
    kickoffs = EmbeddedDocumentListField(kickoffs)
    defense = EmbeddedDocumentListField(defense)
    penalties = EmbeddedDocumentListField(penalties)
    punt_returns = EmbeddedDocumentListField(punt_returns)
    conversions = EmbeddedDocumentListField(conversions)
    first_downs = EmbeddedDocumentListField(first_downs)
    redzone = EmbeddedDocumentListField(redzone)
    goaltogo = EmbeddedDocumentListField(goaltogo)
    field_goals = EmbeddedDocumentListField(field_goals)
    touchdowns = EmbeddedDocumentListField(touchdowns)
    interceptions = EmbeddedDocumentListField(interceptions)
    thirdown = EmbeddedDocumentListField(thirddown)
    fourthdown = EmbeddedDocumentListField(fourthdown)
    kicks = EmbeddedDocumentListField(kicks)


meta = {"collection": "GameStatsTeamInfo"}


def __str__(self):
    return f"GameStatsTeamInfo: {self.game_id} - {self.team}"
