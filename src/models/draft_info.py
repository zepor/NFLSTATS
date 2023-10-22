from mongoengine import DecimalField,DateField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
class team(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    direction = StringField()
    name = StringField()
    sr_id = StringField()
    market = StringField()
class item(EmbeddedDocument):
    amount = IntField()
    id = UUIDField()
    type = StringField()
class pick(EmbeddedDocument):
    id = UUIDField()
    number = IntField()
    compensatory = BooleanField()
    overall = IntField()
    supplemental = BooleanField()
    traded = BooleanField()
class trade(EmbeddedDocument):
    id = UUIDField()
    complete = BooleanField()
    sequence = IntField()
class transaction(EmbeddedDocument):
    id = UUIDField()
class draft(EmbeddedDocument):
    id = UUIDField()
    number = IntField()
    end_date = DateTimeField()
    status = StringField()
    round = IntField()
    year = IntField()
    start_date = DateTimeField()
class round(EmbeddedDocument):
    id = UUIDField()
    number = IntField()
    end_date = DateField()
    status = StringField()
    start_date = DateField()
class future_pick(EmbeddedDocument):
    round = IntField()
    year = IntField()
class DraftInfo(Document):
    team = EmbeddedDocumentListField(team)
    item = EmbeddedDocumentListField(item)
    pick = EmbeddedDocumentListField(pick)
    trade = EmbeddedDocumentListField(trade)
    transaction = EmbeddedDocumentListField(transaction)
    draft = EmbeddedDocumentListField(draft)
    round = EmbeddedDocumentListField(round)
    future_pick = EmbeddedDocumentListField(future_pick)


    meta = {"collection": "DraftInfo"}  # Specify the collection name

    # Define methods or properties if needed

    def __str__(self):
        return f"DraftInfo: {self.teamalias}, {self.teamname}, {self.draftid}"
