from mongoengine import EmbeddedDocumentField, UUIDField, DateTimeField, EmbeddedDocumentListField, EmbeddedDocument, Document, StringField, DecimalField, IntField, ListField, DictField


class coach(EmbeddedDocument):
    first_name = StringField()
    full_name = StringField()
    id = StringField()
    last_name = StringField()
    name_suffix = StringField()
    position = StringField()
    source_id = UUIDField()


class rgb_color(EmbeddedDocument):
    blue = IntField()
    green = IntField()
    red = IntField()


class team_color(EmbeddedDocument):
    alpha = DecimalField()
    hex_color = StringField()
    type = StringField()


class team(EmbeddedDocument):
    alias = StringField()
    direction = StringField()
    id = StringField(primary_key=True)
    last_modified = DateTimeField()
    market = StringField()
    name = StringField()
    sequence = IntField()
    sr_id = StringField()


class TeamInfo(Document):
    team = EmbeddedDocumentField(team)
    coachs = EmbeddedDocumentListField(coach)
    rgb_colors = EmbeddedDocumentListField(rgb_color)
    team_colors = EmbeddedDocumentListField(team_color)
    conference_id = StringField()
    division_id = StringField()
    id = StringField(primary_key=True)

    meta = {"collection": "TeamInfo"}

    def __str__(self):
        return f"TeamInfo: {self.name}, {self.alias}, {self.market}"

    def save(self, *args, **kwargs):
        self.id = self.team.id
        super(TeamInfo, self).save(*args, **kwargs)
