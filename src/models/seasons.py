from mongoengine import DecimalField, EmbeddedDocumentField, Document, DateField, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class SeasonInfo(Document):
    _id = StringField(primary_key=True, db_field='_id')
    year = IntField()
    startdate = DateField()
    enddate = DateField()
    status = StringField()
    type = StringField()
    meta = {"collection": "SeasonInfo"}

    def __str__(self):
        return f"SeasonInfo: Id: {self.id}, Year: {self.year}, Start Date: {self.startdate}, End Date: {self.enddate}, Status: {self.status}, Type: {self.type}"

    def save(self, *args, **kwargs):
        self._id = self._id  # or any other logic you want
        super(SeasonInfo, self).save(*args, **kwargs)
