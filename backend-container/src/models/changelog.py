from mongoengine import Document, DateTimeField, DictField, StringField


class ChangelogEntry(Document):
    entity_id = StringField(required=True)  # ID of the entity being updated
    # Type of the entity (e.g., VenueInfo, LeagueInfo, etc.)
    entity_type = StringField(required=True)
    changes = DictField(required=True)  # Dictionary to store field changes
    timestamp = DateTimeField(required=True)  # Timestamp of the change

    meta = {
        "collection": "changelog"  # Collection name in the database
    }
