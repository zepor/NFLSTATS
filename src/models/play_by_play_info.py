from mongoengine import DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class quarter(EmbeddedDocument):
    id = UUIDField()
    number = IntField()
    sequence = IntField()


class location(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    name = StringField()
    market = StringField()
    sr_id = UUIDField()
    yardline = IntField()


class possession(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    name = StringField()
    market = StringField()
    sr_id = UUIDField()


class start_location(EmbeddedDocument):
    alias = StringField()
    yardline = IntField()


class play(EmbeddedDocument):
    away_points = IntField()
    home_points = IntField()
    blitz = BooleanField()
    id = UUIDField()
    sequence = DecimalField()
    clock = StringField()
    created_at = DateTimeField()
    fake_field_goals = BooleanField()
    fake_punts = BooleanField()
    hash_mark = StringField()
    huddle = StringField()
    left_tightends = IntField()
    men_in_box = IntField()
    pass_route = StringField()
    play_action = BooleanField()
    play_direction = StringField()
    play_type = StringField()
    players_rushed = IntField()
    pocket_location = StringField()
    qb_at_snap = StringField()
    right_tightends = IntField()
    run_pass_option = BooleanField()
    running_lane = StringField()
    scoring_play = BooleanField()
    screen_pass = BooleanField()
    type = StringField()
    updated_at = DateTimeField()
    wall_clock = StringField()


class score(EmbeddedDocument):
    away_points = IntField()
    points = IntField()
    home_points = IntField()
    sequence = DecimalField()
    clock = StringField()


class detail(EmbeddedDocument):
    category = StringField()
    sequence = IntField()
    direction = StringField()
    first_touch = StringField()
    no_attempt = IntField()
    onside = StringField()
    reason_missed = StringField()
    result = StringField()
    sack_split = StringField()
    yards = IntField()


class event(EmbeddedDocument):
    id = UUIDField()
    sequence = DecimalField()
    clock = StringField()
    created_at = DateTimeField()
    type = StringField()
    updated_at = DateTimeField()


class end_situation(EmbeddedDocument):
    clock = StringField()
    down = IntField()
    yfd = IntField()


class start_situation(EmbeddedDocument):
    clock = StringField()
    down = IntField()
    yfd = IntField()


class drive(EmbeddedDocument):
    id = UUIDField()
    sequence = IntField()
    created_at = DateTimeField()
    duration = StringField()
    end_clock = StringField()
    end_reason = StringField()
    first_downs = IntField()
    first_drive_yardline = IntField()
    gain = StringField()
    inside_20 = BooleanField()
    last_drive_yardline = IntField()
    net_yards = IntField()
    pat_points_attempted = IntField()
    pat_points_attempted = BooleanField()
    penalty_yards = IntField()
    play_count = IntField()
    scoring_drive = BooleanField()
    start_clock = StringField()
    start_reason = StringField()
    team_sequence = StringField()
    updated_at = DateTimeField()


class description(EmbeddedDocument):
    Description = StringField()


class penalty(EmbeddedDocument):
    Description = StringField()
    no_play = StringField()
    result = StringField()
    safety = IntField()
    yards = IntField()


class defensive_team(EmbeddedDocument):
    points = IntField()
    id = UUIDField()


class offensive_team(EmbeddedDocument):
    points = IntField()
    id = UUIDField()


class period(EmbeddedDocument):
    id = UUIDField()
    number = IntField()
    sequence = IntField()


class points_after_play(EmbeddedDocument):
    id = UUIDField()
    sequence = DecimalField()
    type = StringField()


class PlayByPlayInfo(Document):
    _id = StringField(required=True)
    game_id = StringField(required=True)
    season_type = StringField(required=True)
    season_year = IntField(required=True)
    week = IntField(required=True)
    away_team = StringField(required=True)
    home_team = StringField(required=True)
    away_score = IntField(required=True)
    home_score = IntField(required=True)
    clock = StringField(required=True)
    clock_secs = IntField(required=True)
    down = IntField(required=True)
    yfd = IntField(required=True)
    yard_line = IntField(required=True)
    yard_line_territory = StringField(required=True)
    quarter = EmbeddedDocumentListField(quarter)
    location = EmbeddedDocumentListField(location)
    possession = EmbeddedDocumentListField(possession)
    start_location = EmbeddedDocumentListField(start_location)
    play = EmbeddedDocumentListField(play)
    score = EmbeddedDocumentListField(score)
    detail = EmbeddedDocumentListField(detail)
    event = EmbeddedDocumentListField(event)
    end_situation = EmbeddedDocumentListField(end_situation)
    start_situation = EmbeddedDocumentListField(start_situation)
    drive = EmbeddedDocumentListField(drive)
    description = EmbeddedDocumentListField(description)
    penalty = EmbeddedDocumentListField(penalty)
    defensive_team = EmbeddedDocumentListField(defensive_team)
    offensive_team = EmbeddedDocumentListField(offensive_team)
    period = EmbeddedDocumentListField(period)
    points_after_play = EmbeddedDocumentListField(points_after_play)


meta = {"collection": "PlayByPlayInfo"}  # Specify the collection name


def __str__(self):
    return "PlayByPlayGameInfo: "
