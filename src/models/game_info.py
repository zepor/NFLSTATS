from mongoengine import DecimalField,EmbeddedDocumentField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import DecimalField, EmbeddedDocument, EmbeddedDocumentField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocumentListField

class gamegame(EmbeddedDocument):
    id = StringField(primary_key=True)
    number = IntField()
    conference_game = BooleanField()
    coverage = StringField()
    duration = StringField()
    entry_mode = StringField()
    game_type = StringField()
    sr_id = StringField()
    last_modified = DateTimeField()
    scheduled = DateTimeField()
    status = StringField()
    title = StringField()
    neutral_site = BooleanField()
    seasonid = StringField()
    leagueweek = StringField()
    venueid = StringField()
class awayteam(EmbeddedDocument):
    alias = StringField()
    id = StringField()
    name = StringField()
    game_number = IntField()
    sr_id = StringField()
    market = StringField()
class hometeam(EmbeddedDocument):
    alias = StringField()
    id = StringField()
    name = StringField()
    game_number = IntField()
    sr_id = StringField()
    market = StringField()
class broadcast(EmbeddedDocument):
    channel = StringField()
    internet = StringField()
    network = StringField()
    satellite = IntField()
class weather(EmbeddedDocument):
    condition = StringField()
    humidity = IntField()
    temp = IntField()
class wind(EmbeddedDocument):
    direction = StringField()
    speed = IntField()
class GameInfo(Document):
    id = StringField(primary_key=True) 
    gamegame = EmbeddedDocumentField(gamegame)
    awayteam = EmbeddedDocumentField(awayteam)
    hometeam = EmbeddedDocumentField(hometeam)
    broadcast = EmbeddedDocumentField(broadcast)
    weather = EmbeddedDocumentField(weather)
    wind = EmbeddedDocumentField(wind)

    meta = {"collection": 'GameInfo'}

    def __str__(self):
        return f"GameInfo: {self.gamegame}"
    def save(self, *args, **kwargs):
        self.id = self.gamegame.id
        super(GameInfo, self).save(*args, **kwargs)
