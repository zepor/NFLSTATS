from mongoengine import EmbeddedDocumentField, DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class venue1(EmbeddedDocument):
    id = StringField()
    address = StringField()
    capacity = IntField()
    city = StringField()
    country = StringField()
    name = StringField()
    sr_id = StringField()
    roof_type = StringField()
    state = StringField()
    surface = StringField()
    zip = StringField()


class location(EmbeddedDocument):
    lat = DecimalField()
    lng = DecimalField()


class VenueInfo(Document):
    venue1 = EmbeddedDocumentField(venue1)
    location = EmbeddedDocumentField(location)
    id = StringField(primary_key=True)

    meta = {"collection": "VenueInfo"}  # Specify the collection name

    def __str__(self):
        return "VenuInfo: "

    def save(self, *args, **kwargs):
        self.id = self.venue1.id
        super(VenueInfo, self).save(*args, **kwargs)
