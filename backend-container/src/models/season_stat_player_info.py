from mongoengine import EmbeddedDocumentField,  DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class intreturns(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    avgyards = DecimalField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class passing(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    airyards = IntField()
    attempts = IntField()
    avgpockettime = DecimalField()
    avgyards = DecimalField()
    battedpasses = IntField()
    blitzes = IntField()
    cmppct = DecimalField()
    completions = IntField()
    defendedpasses = IntField()
    droppedpasses = IntField()
    firstdowns = IntField()
    grossyards = IntField()
    hurries = IntField()
    inttouchdowns = IntField()
    interceptions = IntField()
    knockdowns = IntField()
    netyards = DecimalField()
    ontargetthrows = IntField()
    pockettime = IntField()
    poorthrows = IntField()
    rating = DecimalField()
    redzoneattempts = IntField()
    sackyards = IntField()
    sacks = IntField()
    spikes = IntField()
    throwaways = IntField()
    touchdowns = IntField()
    yards = IntField()


class receiving(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    airyards = IntField()
    avgyards = DecimalField()
    brokentackles = IntField()
    catchablepasses = IntField()
    droppedpasses = IntField()
    firstdowns = IntField()
    receptions = IntField()
    redzonetargets = IntField()
    targets = IntField()
    touchdowns = IntField()
    yards = IntField()
    yardsaftercatch = IntField()
    yardsaftercontact = IntField()


class defense(EmbeddedDocument):
    assists = IntField()
    battedpasses = IntField()
    blitzes = IntField()
    combined = IntField()
    defcomps = IntField()
    deftargets = IntField()
    forcedfumbles = IntField()
    fumblerecoveries = IntField()
    hurries = IntField()
    interceptions = IntField()
    knockdowns = IntField()
    miscassists = IntField()
    miscfocedfumbles = IntField()
    miscfumblerecovries = IntField()
    misctackles = IntField()
    missedtackles = IntField()
    passesdefended = IntField()
    qbhits = IntField()
    sackyards = IntField()
    sacks = IntField()
    safeties = IntField()
    spassists = IntField()
    spblocks = IntField()
    spforcedfumbles = IntField()
    spfumblerecoveries = IntField()
    sptackles = IntField()
    tackles = IntField()
    tloss = IntField()
    tlossyards = IntField()


class fieldgoals(EmbeddedDocument):
    longest = IntField()
    attempts = IntField()
    attempts19 = IntField()
    attempts29 = IntField()
    attempts39 = IntField()
    attempts49 = IntField()
    attempts50 = IntField()
    avgyards = DecimalField()
    blocked = IntField()
    made = IntField()
    made19 = IntField()
    made29 = IntField()
    made39 = IntField()
    made49 = IntField()
    made50 = IntField()
    missed = IntField()
    pct = DecimalField()
    yards = IntField()


class punts(EmbeddedDocument):
    longest = IntField()
    attempts = IntField()
    avghangtime = DecimalField()
    avgnetyards = DecimalField()
    avgyards = DecimalField()
    blocked = IntField()
    hangtime = IntField()
    inside20 = IntField()
    netyards = DecimalField()
    returnyards = DecimalField()
    touchbacks = IntField()
    yards = IntField()


class rushing(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    attempts = IntField()
    avgyards = DecimalField()
    brokentackles = IntField()
    firstdowns = IntField()
    kneeldowns = IntField()
    redzoneattempts = IntField()
    scrambles = IntField()
    tlost = IntField()
    tlostyards = IntField()
    touchdowns = IntField()
    yards = IntField()
    yardsaftercontact = IntField()


class extrapoints(EmbeddedDocument):
    attempts = IntField()
    blocked = IntField()
    made = IntField()
    missed = IntField()
    pct = DecimalField()


class kickreturns(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    avgyards = DecimalField()
    faircatches = IntField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class puntreturns(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    avgyards = DecimalField()
    faircatches = IntField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class conversions(EmbeddedDocument):
    defenseattempts = IntField()
    defensesuccesses = IntField()
    passattempts = IntField()
    passsuccesses = IntField()
    receiveattempts = IntField()
    receivesuccesses = IntField()
    rushattempts = IntField()
    rushsuccesses = IntField()


class kickoffs(EmbeddedDocument):
    endzone = IntField()
    inside20 = IntField()
    kickoffs = IntField()
    onsideattempts = IntField()
    onsidesuccesses = IntField()
    outofbounds = IntField()
    returnyards = IntField()
    squibkicks = IntField()
    touchbacks = IntField()
    yards = IntField()


class fumbles(EmbeddedDocument):
    ezrectds = IntField()
    forcedfumbles = IntField()
    fumbles = IntField()
    lostfumbles = IntField()
    opprec = IntField()
    opprectds = IntField()
    opprecyards = IntField()
    outofbounds = IntField()
    ownrec = IntField()
    ownrectds = IntField()
    ownrecyards = IntField()


class penalties(EmbeddedDocument):
    penalties = IntField()
    yards = IntField()
    firstdowns = IntField()


class SeasonStatPlayer(Document):
    _id = StringField(primary_key=True)
    playerid = StringField()
    teamid = StringField()
    seasonid = StringField()
    gamesplayed = IntField()
    gamesstarted = IntField()
    jersey = StringField()
    position = StringField()
    playername = StringField()
    intreturns = EmbeddedDocumentField(intreturns)
    passing = EmbeddedDocumentField(passing)
    receiving = EmbeddedDocumentField(receiving)
    defense = EmbeddedDocumentField(defense)
    fieldgoals = EmbeddedDocumentField(fieldgoals)
    punts = EmbeddedDocumentField(punts)
    rushing = EmbeddedDocumentField(rushing)
    extrapoints = EmbeddedDocumentField(extrapoints)
    kickreturns = EmbeddedDocumentField(kickreturns)
    puntreturns = EmbeddedDocumentField(puntreturns)
    conversions = EmbeddedDocumentField(conversions)
    kickoffs = EmbeddedDocumentField(kickoffs)
    fumbles = EmbeddedDocumentField(fumbles)
    penalties = EmbeddedDocumentField(penalties)

    meta = {"collection": "SeasonStatPlayer"}  # Specify the collection name

    def __str__(self):
        return f"SeasonStatPlayer: {str(self.tojson())}"

    def save(self, *args, **kwargs):
        if all(hasattr(self, attr) for attr in ['playerid', 'teamid', 'seasonid']):
            self._id = f"{self.playerid}_{self.teamid}_{self.seasonid}"
        else:
            raise ValueError(
                "playerid, teamid, and seasonid must all be set before saving.")
        super(SeasonStatPlayer, self).save(*args, **kwargs)
