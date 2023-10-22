from mongoengine import (IntField, BooleanField, EmbeddedDocument,
                         StringField,EmbeddedDocumentListField, FloatField,
                         Document)

class extra_point(EmbeddedDocument):
    aborted = IntField()
    attempt = IntField()
    blocked = IntField()
    made = IntField()
    missed = IntField()
    returned = IntField()
    safety = IntField()


class defense(EmbeddedDocument):
    ast_sacks = IntField()
    ast_tackle = IntField()
    ast_tackle = StringField()
    ast_tlost = IntField()
    batted_pass = IntField()
    blitz = IntField()
    block = IntField()
    def_comp = IntField()
    def_target = IntField()
    forced_fumble = IntField()
    hurry = IntField()
    int_touchdown = IntField()
    int_yards = IntField()
    interception = IntField()
    knockdown = IntField()
    nullified = BooleanField()
    pass_defended = IntField()
    primary = IntField()
    qb_hit = IntField()
    sack = IntField()
    sack_yards = IntField()
    safety = IntField()
    tackle = IntField()
    tlost = IntField()
    tlost_yards = IntField()


class field_goal(EmbeddedDocument):
    att_yards = IntField()
    attempt = IntField()
    blocked = IntField()
    made = IntField()
    missed = IntField()
    nullified = BooleanField()
    returned = IntField()
    yards = IntField()


class passing(EmbeddedDocument):
    att_yards = IntField()
    attempt = IntField()
    batted_pass = IntField()
    blitz = IntField()
    complete = IntField()
    firstdown = IntField()
    goaltogo = IntField()
    hurry = IntField()
    incompletion_type = StringField()
    inside_20 = IntField()
    int_touchdown = IntField()
    interception = IntField()
    knockdown = IntField()
    nullified = BooleanField()
    on_target_throw = IntField()
    pocket_time = FloatField()
    sack = IntField()
    sack_yards = IntField()
    safety = IntField()
    touchdown = IntField()
    yards = IntField()


class conversion(EmbeddedDocument):
    attempt = IntField()
    category = StringField()
    complete = IntField()
    safety = IntField()


class defense_conversion(EmbeddedDocument):
    attempt = IntField()
    category = StringField()
    complete = IntField()


class down_conversion(EmbeddedDocument):
    attempt = IntField()
    complete = IntField()
    down = IntField()


class kick(EmbeddedDocument):
    attempt = IntField()
    endzone = IntField()
    gross_yards = IntField()
    inside_20 = IntField()
    onside_attempt = IntField()
    onside_success = IntField()
    own_rec = IntField()
    own_rec_td = IntField()
    squib_kick = IntField()
    touchback = IntField()
    yards = IntField()
    nullified = BooleanField()


class punt(EmbeddedDocument):
    attempt = IntField()
    blocked = IntField()
    downed = IntField()
    endzone = IntField()
    faircatch = IntField()
    hang_time = IntField()
    inside_20 = IntField()
    nullified = BooleanField()
    out_of_bounds = IntField()
    touchback = IntField()
    yards = IntField()


class rush(EmbeddedDocument):
    attempt = IntField()
    broken_tackles = IntField()
    firstdown = IntField()
    goaltogo = IntField()
    inside_20 = IntField()
    kneel_down = IntField()
    lateral = IntField()
    nullified = BooleanField()
    safety = IntField()
    scramble = IntField()
    tlost = IntField()
    tlost_yards = IntField()
    touchdown = IntField()
    yards = IntField()
    yards_after_contact = IntField()


class block(EmbeddedDocument):
    block = IntField()
    category = StringField()


class receive(EmbeddedDocument):
    broken_tackles = IntField()
    catchable = IntField()
    dropped = IntField()
    firstdown = IntField()
    goaltogo = IntField()
    inside_20 = IntField()
    nullified = BooleanField()
    reception = IntField()
    safety = IntField()
    target = IntField()
    touchdown = IntField()
    yards = IntField()
    yards_after_catch = IntField()
    yards_after_contact = IntField()


class first_down(EmbeddedDocument):
    category = StringField()


class kickreturn(EmbeddedDocument):
    category = StringField()
    downed = IntField()
    faircatch = IntField()
    firstdown = IntField()
    lateral = IntField()
    nullified = BooleanField()
    out_of_bounds = IntField()
    play_category = StringField()
    kickreturn = IntField()
    touchback = IntField()
    touchdown = IntField()
    yards = IntField()


class penalty(EmbeddedDocument):
    penalty = IntField()
    yards = IntField()


class fumble(EmbeddedDocument):
    forced = IntField()
    fumble = IntField()
    lost = IntField()
    nullified = BooleanField()
    opp_rec = IntField()
    opp_rec_td = IntField()
    opp_rec_yards = IntField()
    out_of_bounds = BooleanField()
    own_rec = IntField()
    own_rec_td = IntField()
    own_rec_yards = IntField()
    play_category = StringField()


class PlayByPlayGameStatsTeamInfo(Document):
    extra_point = EmbeddedDocumentListField(extra_point)
    defense = EmbeddedDocumentListField(defense)
    field_goal = EmbeddedDocumentListField(field_goal)
    passing = EmbeddedDocumentListField(passing)
    conversion = EmbeddedDocumentListField(conversion)
    defense_conversion = EmbeddedDocumentListField(defense_conversion)
    down_conversion = EmbeddedDocumentListField(down_conversion)
    kick = EmbeddedDocumentListField(kick)
    punt = EmbeddedDocumentListField(punt)
    rush = EmbeddedDocumentListField(rush)
    block = EmbeddedDocumentListField(block)
    receive = EmbeddedDocumentListField(receive)
    first_down = EmbeddedDocumentListField(first_down)
    kickreturn = EmbeddedDocumentListField(kickreturn)
    penalty = EmbeddedDocumentListField(penalty)
    fumble = EmbeddedDocumentListField(fumble)

    # Specify the collection name
    meta = {"collection": "PlayByPlayGameStatsTeamInfo"}

    def __str__(self):
        # You can add more specific details here if needed
        return "PlayByPlayGameStatsTeamInfo: "
