from mongoengine import DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class GameStatTeamSummaryInfo(Document):
    avg_gain = DecimalField()
    fumbles = IntField()
    lost_fumbles = IntField()
    penalties = IntField()
    penalty_yards = IntField()
    play_count = IntField()
    possession_time = StringField()
    return_yards = IntField()
    rush_plays = IntField()
    safeties = IntField()
    total_yards = IntField()
    turnovers = IntField()


meta = {"collection": "GameStatTeamSummaryInfo"}


def __str__(self):
    return "GameStatTeamSummaryInfo: "
