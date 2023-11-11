from mongoengine import DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class metadata(EmbeddedDocument):
    draft = StringField()
    event_category = StringField()
    event_type = StringField()
    league = StringField()
    locale = StringField()
    match = StringField()
    status = StringField()
    operation = StringField()
    participant = StringField()
    team = StringField()
    version = StringField()


class MetaDataInfo(Document):
    metadata = EmbeddedDocumentListField(metadata)


meta = {"collection": "MetaDataInfo"}


def __str__(self):
    return "MetaDataInfo: "
