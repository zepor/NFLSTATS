from mongoengine import EmbeddedDocumentField, DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
class FranchiseInfo(Document):
    id = StringField(primary_key=True, db_field='_id')
    teamid = StringField()
    name = StringField()
    alias = StringField()
    # other fields

    meta = {"collection": "FranchiseInfo"}  # Specify the collection name

    def __str__(self):
        return f"FranchiseInfo: {self.alias}, {self.id}, {self.name}"
    
    def save(self, *args, **kwargs):
        self.id = self.id  # or any other logic you want
        super(FranchiseInfo, self).save(*args, **kwargs)

