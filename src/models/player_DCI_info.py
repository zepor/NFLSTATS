from mongoengine import EmbeddedDocumentField, DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class player(EmbeddedDocument):
    abbrname = StringField()
    age = IntField()
    birthdate = StringField()
    birthplace = StringField()
    id = StringField(primarykey=True)
    college = StringField()
    collegeconf = StringField()
    depth = IntField()
    experience = IntField()
    firstname = StringField()
    fullname = StringField()
    height = IntField()
    highschool = StringField()
    srid = StringField()
    ingamestatus = StringField()
    jersey = StringField()
    lastmodified = DateTimeField()
    lastname = StringField()
    status = StringField()
    namesuffix = StringField()
    position = StringField()
    preferredname = StringField()
    role = StringField()
    sourceid = StringField()
    weight = DecimalField()
    draftyear = IntField()
    draftround = IntField()
    draftnumber = IntField()
    draftteamid = StringField()
    draftteamname = StringField()
    draftteamalias = StringField()
    draftteamsrid = StringField()
    draftteammarket = StringField()


class prospect(EmbeddedDocument):
    birthplace = StringField()
    id = StringField()
    name = StringField()
    experience = StringField()
    firstname = StringField()
    height = IntField()
    lastname = StringField()
    leagueid = StringField()
    position = StringField()
    publishable = BooleanField()
    sourceid = StringField()
    teamname = StringField()
    topprospect = BooleanField()
    weight = IntField()


class primary(EmbeddedDocument):
    Description = StringField()


class position(EmbeddedDocument):
    name = StringField()


class practice(EmbeddedDocument):
    status = StringField()


class injury(EmbeddedDocument):
    status = StringField()
    statusdate = DateTimeField()


class PlayerDCIinfo(Document):
    playerinfo = EmbeddedDocumentField(player)
    prospectinfo = EmbeddedDocumentField(prospect)
    primaryposition = EmbeddedDocumentField(primary)
    positioninfo = EmbeddedDocumentField(position)
    practiceinfo = EmbeddedDocumentField(practice)
    injuryinfo = EmbeddedDocumentField(injury)
    id = StringField(primary_key=True, db_field='_id')

    meta = {"collection": "PlayerDCIinfo"}  # Specify the collection name

    def __str__(self):
        return "PlayerDCIinfo: " + str({
            "playerinfo": self.playerinfo,
            "prospectinfo": self.prospectinfo,
            "primaryposition": self.primaryposition,
            "positioninfo": self.positioninfo,
            "practiceinfo": self.practiceinfo,
            "injuryinfo": self.injuryinfo,
        })

    def save(self, *args, **kwargs):
        self.id = self.playerinfo.id
        super(PlayerDCIinfo, self).save(*args, **kwargs)
