from mongoengine import DecimalField, EmbeddedDocumentField, Document, DateField, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class game(EmbeddedDocument):
    seasonoid = StringField()
    seasonname = StringField()
    leagueweekid = StringField()
    gameid = StringField()


class season(EmbeddedDocument):
    weekid = StringField()
    id = StringField()
    name = StringField()
    status = StringField()
    type = StringField()
    year = IntField()
    start_date = DateField()
    end_date = DateField()


class changelog(EmbeddedDocument):
    id = StringField()
    end_time = DateTimeField()
    start_time = DateTimeField()


class leagueweek(EmbeddedDocument):
    id = StringField()
    sequence = IntField()
    title = StringField()
    byeweekteamalias = StringField()
    byeweekteamid = StringField()
    byeweekteamname = StringField()
    byeweekteamsrid = StringField()


class LeagueInfo(Document):
    season = EmbeddedDocumentField(season)
    changelog = EmbeddedDocumentListField(changelog)
    leagueweek = EmbeddedDocumentListField(leagueweek)
    _id = StringField(primary_key=True)
    meta = {"collection": "LeagueInfo"}

    def __str__(self):
        return f"LeagueInfo: {self.id}, Seasons: {len(self.season)}, ChangeLogs: {len(self.changelog)}, LeagueWeeks: {len(self.leagueweek)}"

    def save(self, *args, **kwargs):
        self._id = self.season.weekid
        super(LeagueInfo, self).save(*args, **kwargs)
