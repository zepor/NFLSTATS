from curses.ascii import EM
from mongoengine import DecimalField, EmbeddedDocumentField, Document, DateField, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class gamebs(EmbeddedDocument):
    id = StringField(primary_key=True)
    attendance = IntField()
    hometeam = StringField()
    awayteam = StringField()
    awayteamtotalpoints = IntField()
    hometeamtotalpoints = IntField()


class overtime(EmbeddedDocument):
    overtime_id = StringField()
    overtime_number = IntField()
    overtime_sequence = DecimalField()
    awayteamovertimepoints = IntField()
    hometeamovertimepoints = IntField()


class quarter(EmbeddedDocument):
    quarter_id = StringField()
    quarter_number = IntField()
    quarter_sequence = IntField()
    awayteampointsforquarter = IntField()
    hometeampointsforquarter = IntField()


class coin_toss(EmbeddedDocument):
    awayteamcoincointossdecision = StringField()
    awayteamcoincointossdirection = StringField()
    awayteamcoincointossoutcome = StringField()
    hometeamcoincointossdecision = StringField()
    hometeamcoincointossdirection = StringField()
    hometeamcoincointossoutcome = StringField()


class challenges(EmbeddedDocument):
    awayteamchallengeschallengesremaining = IntField()
    awayteamchallengeschallengesused = IntField()
    clock = StringField()
    hometeamchallengeschallengesremaining = IntField()
    hometeamchallengeschallengesused = IntField()


class timeouts(EmbeddedDocument):
    awayteamtimeoutstimeoutsremaining = IntField()
    awayteamtimeoutstimeoutsused = IntField()
    clock = StringField()
    hometeamtimeoutstimeoutsremaining = IntField()
    hometeamtimeoutstimeoutsused = IntField()

class situation(EmbeddedDocument):
    currentsituationclock = StringField()
    currentsituationdown = IntField()
    currentsituationyardstofirstdown = IntField()


class event(EmbeddedDocument):
    lasteventdescription = StringField()
    lasteventclock = StringField()
    lasteventcreatedat = DateTimeField()
    lasteventdeleted = BooleanField()
    lasteventid = StringField()
    lasteventsequence = DecimalField()
    lasteventsource = StringField()
    lasteventtype = StringField()
    lasteventupdatedat = DateTimeField()
    lasteventwallclock = DateTimeField()

class location(EmbeddedDocument):
    currentsituationlocationteamalias = StringField()
    currentsituationlocationteamteamid = UUIDField()
    currentsituationlocationteammarket = StringField()
    currentsituationlocationteamname = StringField()
    currentsituationlocationteamsrid = StringField()
    currentsituationlocationteamyardline = IntField()
    currentsituationpossessionteamalias = StringField()

class possession(EmbeddedDocument):
    currentsituationpossessionteamid = StringField()
    currentsituationpossessionteammarket = StringField()
    currentsituationpossessionteamname = StringField()
    currentsituationpossessionteamsrid = StringField()


class official(EmbeddedDocument):
    officialsassignment = StringField()
    officialsfullname = StringField()
    officialsnumber = IntField()


class BoxscoreInfo(Document):
    gamebs = EmbeddedDocumentField(gamebs)
    overtimes = EmbeddedDocumentListField(overtime)
    quarters = EmbeddedDocumentListField(quarter)
    coin_toss = EmbeddedDocumentField(coin_toss)
    challenges = EmbeddedDocumentField(challenges)
    timeouts = EmbeddedDocumentField(timeouts)
    situation = EmbeddedDocumentField(situation)
    event = EmbeddedDocumentField(event)
    location = EmbeddedDocumentField(location)
    possession = EmbeddedDocumentField(possession)
    official = EmbeddedDocumentListField(official)
    id = StringField(primary_key=True)

    meta = {"collection": "BoxscoreInfo"}

    def __str__(self):
        return "BoxscoreInfo: "

    def save(self, *args, **kwargs):
        self.id = self.gamebs.id
        super(BoxscoreInfo, self).save(*args, **kwargs)
