from mongoengine import DecimalField, EmbeddedDocumentField, Document, DateField, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class teams(EmbeddedDocument):
    teamid = StringField()
    teamname = StringField()


class division(EmbeddedDocument):
    did = StringField()
    dalias = StringField()
    dname = StringField()
    teams = EmbeddedDocumentListField(teams)


class conference(EmbeddedDocument):
    cid = StringField()
    calias = StringField()
    cname = StringField()
    divisions = EmbeddedDocumentListField(division)


class league(EmbeddedDocument):
    id = StringField(primary_key=True)
    alias = StringField()
    name = StringField()
    conferences = EmbeddedDocumentListField(conference)


class typeleague(EmbeddedDocument):
    code = StringField()


class LeagueHierarchy(Document):
    league = EmbeddedDocumentField(league)
    conferences = EmbeddedDocumentListField(conference)
    divisions = EmbeddedDocumentListField(division)
    typeleague = EmbeddedDocumentListField(typeleague)
    teams = EmbeddedDocumentListField(teams)
    id = StringField(primary_key=True)
    meta = {"collection": "LeagueHierarchy"}

    def __str__(self):
        return "LeagueHierarchy: "

    def save(self):
        if isinstance(self.league, dict) and 'id' in self.league:
            self.id = self.league['id']
        elif hasattr(self.league, 'id'):
            self.id = self.league.id
        # ... rest of the save method ...
