from mongoengine import DecimalField, Document, DateField, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class from_team(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    name = StringField()
    market = StringField()
    sr_id = UUIDField()


class to_team(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    name = StringField()
    market = StringField()
    sr_id = UUIDField()


class trade(EmbeddedDocument):
    id = UUIDField()
    trade_date = DateTimeField()


class transaction(EmbeddedDocument):
    id = UUIDField()
    desc = StringField()
    effective_date = DateField()
    last_modified = DateTimeField()
    status_after = StringField()
    status_before = StringField()
    transaction_code = StringField()
    transaction_type = StringField()
    transaction_year = IntField()


class transactions(EmbeddedDocument):
    end_time = DateTimeField()
    start_time = DateTimeField()


class TransactionInfo(Document):
    from_team = EmbeddedDocumentListField(from_team)
    to_team = EmbeddedDocumentListField(to_team)
    trade = EmbeddedDocumentListField(trade)
    transaction = EmbeddedDocumentListField(transaction)
    transactions = EmbeddedDocumentListField(transactions)

    meta = {"collection": "TransactionINnfo"}  # Specify the collection name

    def __str__(self):
        # You can customize this string representation
        return "TransactionInfo: " + str(self.id)
