from mongoengine import DecimalField,EmbeddedDocumentField, Document,DateField, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField

class gamebs(EmbeddedDocument):
    id = StringField(primary_key=True)
    attendance = IntField()
    hometeam = StringField()
    hometeamtotalpoints = IntField()
    awayteam = StringField()
    awayteamtotalpoints = IntField()    

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

class BoxscoreInfo(Document):
    gamebs = EmbeddedDocumentField(gamebs)
    overtimes = EmbeddedDocumentListField(overtime)
    quarters = EmbeddedDocumentListField(quarter)
    id = StringField(primary_key=True)

    meta = {"collection": "BoxscoreInfo"}

    def __str__(self):
        return "BoxscoreInfo: "

    def save(self, *args, **kwargs):
        self.id = self.gamebs.id
        super(BoxscoreInfo, self).save(*args, **kwargs)