from mongoengine import DecimalField, Document, FloatField, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class block(EmbeddedDocument):
    block = IntField()
    category = StringField()


class conversion(EmbeddedDocument):
    attempt = IntField()
    category = StringField()
    complete = IntField()
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


class defense_conversion(EmbeddedDocument):
    attempt = IntField()
    category = StringField()
    complete = IntField()


class down_conversion(EmbeddedDocument):
    attempt = IntField()
    complete = IntField()
    down = IntField()


class extra_point(EmbeddedDocument):
    aborted = IntField()
    attempt = IntField()
    blocked = IntField()
    made = IntField()
    missed = IntField()
    returned = IntField()
    safety = IntField()


class field_goal(EmbeddedDocument):
    att_yards = IntField()
    attempt = IntField()
    blocked = IntField()
    made = IntField()
    missed = IntField()
    nullified = BooleanField()
    returned = IntField()
    yards = IntField()


class first_down(EmbeddedDocument):
    category = StringField()


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


class kickj(EmbeddedDocument):
    nullified = BooleanField()


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


class penalty(EmbeddedDocument):
    penalty = IntField()
    yards = IntField()


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


class Pkreturn(EmbeddedDocument):
    category = StringField()
    downed = IntField()
    faircatch = IntField()
    firstdown = IntField()
    lateral = IntField()
    nullified = BooleanField()
    out_of_bounds = IntField()
    play_category = StringField()
    PKreturn = IntField()
    touchback = IntField()
    touchdown = IntField()
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


class PlayerStats(Document):
    blocks = EmbeddedDocumentListField(block)
    conversions = EmbeddedDocumentListField(conversion)
    defenses = EmbeddedDocumentListField(defense)
    # ... other fields ...

    meta = {"collection": "PlayerStats"}  # Specify the collection name

    def __str__(self):
        return "PlayerStats: " + str({
            "blocks": self.blocks,
            "conversions": self.conversions,
            "defenses": self.defenses,
            # ... other fields ...
        })
