from mongoengine import DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class team(EmbeddedDocument):
    losses = IntField()
    points_against = IntField()
    points_for = IntField()
    ties = IntField()
    win_pct = DecimalField()
    wins = IntField()


class record(EmbeddedDocument):
    category = StringField()
    losses = IntField()
    points_against = IntField()
    points_for = IntField()
    ties = IntField()
    win_pct = DecimalField()
    wins = IntField()


class rank(EmbeddedDocument):
    clinched = StringField()
    conference = StringField()
    division = StringField()


class streak(EmbeddedDocument):
    desc = StringField()
    length = IntField()
    type = StringField()


class sos(EmbeddedDocument):
    sos = DecimalField()
    total = IntField()
    wins = IntField()


class sov(EmbeddedDocument):
    sov = DecimalField()
    total = IntField()
    wins = IntField()


class StandingsInfo(Document):
    team = EmbeddedDocumentListField(team)
    record = EmbeddedDocumentListField(record)
    rank = EmbeddedDocumentListField(rank)
    streak = EmbeddedDocumentListField(streak)
    sos = EmbeddedDocumentListField(sos)
    sov = EmbeddedDocumentListField(sov)


meta = {"collection": "Standings_info"}  # Specify the collection name


def __str__(self):
    return "Standings_info: "
