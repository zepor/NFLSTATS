from mongoengine import DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField

class details(EmbeddedDocument):
    category = StringField()
    conversion_type = StringField()
    penalty_type = StringField()
    result = StringField()
    review_type = StringField()
    yards = IntField()
class end_location(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    market = StringField()
    name = StringField()
    sr_id = UUIDField()
    yardline = IntField()

class end_situation(EmbeddedDocument):
    clock = StringField()
    down = IntField()
    play_count = IntField()
    yfd = IntField()

class event_context(EmbeddedDocument):
    id = UUIDField()
    outcome = StringField()
    play_id = UUIDField()
    seconds = IntField()
    
class game_clock(EmbeddedDocument):
    running = BooleanField()
    time = StringField()
      
class location(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    market = StringField()
    name = StringField()
    sr_id = UUIDField()
    yardline = IntField()
      
class period(EmbeddedDocument):
    id = UUIDField()
    number = IntField()
    sequence = IntField()

      
class player(EmbeddedDocument):
    id = UUIDField()
    jersey = StringField()
    name = StringField()
    position = StringField()
    sr_id = UUIDField()
    
class possession(EmbeddedDocument):
    alias = StringField()
    alias = StringField()
    alias = StringField()
    id = UUIDField()
    id = UUIDField()
    id = UUIDField()
    market = StringField()
    market = StringField()
    market = StringField()
    name = StringField()
    name = StringField()
    name = StringField()
    sr_id = UUIDField()
    sr_id = UUIDField()
    sr_id = UUIDField()

class pulse(EmbeddedDocument):
    away_points = IntField()
    clock = StringField()
    created_at = DateTimeField()
    description = StringField()
    down = IntField()
    event_type = StringField()
    home_points = IntField()
    id = UUIDField()
    play_id = UUIDField()
    source = StringField()
    type = StringField()
    updated_at = DateTimeField()
    wall_clock = DateTimeField()
    yfd = IntField()
      
class start_location(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    market = StringField()
    name = StringField()
    sr_id = UUIDField()
    yardline = IntField()    
class start_situation(EmbeddedDocument):
    clock = StringField()
    down = IntField()
    play_count = IntField()
    tfd = IntField() 
class team(EmbeddedDocument):
    alias = StringField()
    id = UUIDField()
    market = StringField()
    name = StringField()
    sr_id = UUIDField()

class PulsePlay(Document):
    details = EmbeddedDocumentListField(details)
    player = EmbeddedDocumentListField(player)
    team = EmbeddedDocumentListField(team)
    location = EmbeddedDocumentListField(location)
    possession = EmbeddedDocumentListField(possession)
    start_location = EmbeddedDocumentListField(start_location)
    end_location = EmbeddedDocumentListField(end_location)
    pulse = EmbeddedDocumentListField(pulse)
    end_situation = EmbeddedDocumentListField(end_situation)
    start_situation = EmbeddedDocumentListField(start_situation)
    period = EmbeddedDocumentListField(period)
    event_context = EmbeddedDocumentListField(event_context)
    game_clock = EmbeddedDocumentListField(game_clock)
    
meta = {"collection": "PulsePlay"}  # Specify the collection name

def __str__(self):
    return "PlayPulse: "

