from mongoengine import EmbeddedDocumentField, DecimalField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField


class touchdowns(EmbeddedDocument):
    passing = IntField()
    rush = IntField()
    totalreturn = IntField()
    total = IntField()
    fumblereturn = IntField()
    intreturn = IntField()
    kickreturn = IntField()
    other = IntField()
    puntreturn = IntField()


class rushing(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    attempts = IntField()
    avgyards = DecimalField()
    brokentackles = IntField()
    kneeldowns = IntField()
    redzoneattempts = IntField()
    scrambles = IntField()
    tlost = IntField()
    tlostyards = IntField()
    touchdowns = IntField()
    yards = IntField()
    yardsaftercontact = IntField()


class receiving(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    airyards = IntField()
    avgyards = DecimalField()
    brokentackles = IntField()
    catchablepasses = IntField()
    droppedpasses = IntField()
    receptions = IntField()
    redzonetargets = IntField()
    targets = IntField()
    touchdowns = IntField()
    yards = IntField()
    yardsaftercatch = IntField()
    yardsaftercontact = IntField()


class intreturns(EmbeddedDocument):
    longest = IntField()
    longesttouchdown = IntField()
    avgyards = DecimalField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class passing(EmbeddedDocument):
    attempts = IntField()
    completions = IntField()
    comppct = DecimalField()
    interceptions = IntField()
    sackyards = IntField()
    rating = DecimalField()
    touchdowns = IntField()
    avgyards = DecimalField()
    sacks = IntField()
    longest = IntField()
    longesttouchdown = IntField()
    airyards = IntField()
    redzoneattempts = IntField()
    netyards = DecimalField()
    yards = IntField()
    grossyards = IntField()
    inttouchdowns = IntField()
    throwaways = IntField()
    poorthrows = IntField()
    defendedpasses = IntField()
    droppedpasses = IntField()
    spikes = IntField()
    blitzes = IntField()
    hurries = IntField()
    knockdowns = IntField()
    pockettime = IntField()
    battedpasses = IntField()
    ontargetthrows = IntField()


class defense(EmbeddedDocument):
    tackles = IntField()
    assists = IntField()
    combined = IntField()
    sacks = IntField()
    sackyards = IntField()
    interceptions = IntField()
    passesdefended = IntField()
    forcedfumbles = IntField()
    fumblerecoveries = IntField()
    qbhits = IntField()
    tloss = IntField()
    tlossyards = IntField()
    safeties = IntField()
    sptackles = IntField()
    spassists = IntField()
    spforcedfumbles = IntField()
    spfumblerecoveries = IntField()
    spblocks = IntField()
    misctackles = IntField()
    miscassists = IntField()
    miscforcedfumbles = IntField()
    miscfumblerecoveries = IntField()
    deftargets = IntField()
    defcomps = IntField()
    blitzes = IntField()
    hurries = IntField()
    knockdowns = IntField()
    missedtackles = IntField()
    battedpasses = IntField()
    threeandoutsforced = IntField()
    fourthdownstops = IntField()


class thirddown(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class fourthdown(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class goaltogo(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class redzone(EmbeddedDocument):
    attempts = IntField()
    pct = DecimalField()
    successes = IntField()


class kicks(EmbeddedDocument):
    attempts = IntField()
    blocked = IntField()
    made = IntField()
    pct = DecimalField()


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
    netyards = IntField()
    returnyards = IntField()
    touchbacks = IntField()
    yards = IntField()

    yardsaftercontact = IntField()


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


class miscreturns(EmbeddedDocument):
    longesttouchdown = IntField()
    blkfgtouchdowns = IntField()
    blkpunttouchdowns = IntField()
    ezrectouchdowns = IntField()
    fgreturntouchdowns = IntField()
    returns = IntField()
    touchdowns = IntField()
    yards = IntField()


class record(EmbeddedDocument):
    gamesplayed = IntField()


class conversions(EmbeddedDocument):
    defenseattempts = IntField()
    defensesuccesses = IntField()
    passattempts = IntField()
    passsuccesses = IntField()
    rushattempts = IntField()
    rushsuccesses = IntField()
    turnoversuccesses = IntField()


class kickoffs(EmbeddedDocument):
    endzone = IntField()
    inside20 = IntField()
    kickoffs = IntField()
    onsideattempts = IntField()
    onsidesuccesses = IntField()
    outofbounds = IntField()
    returnyards = IntField()
    returned = IntField()
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


class interceptions(EmbeddedDocument):
    interceptions = IntField()
    returnyards = IntField()
    returned = IntField()


class firstdowns(EmbeddedDocument):
    passing = IntField()
    penalty = IntField()
    rush = IntField()
    total = IntField()


class SeasonStatOppo(Document):
    _id = StringField(primary_key=True)
    seasonid = StringField()
    teamid = StringField()
    opponents_played = IntField()
    playernname = StringField()
    intreturns = EmbeddedDocumentField(intreturns)
    passing = EmbeddedDocumentField(passing)
    receiving = EmbeddedDocumentField(receiving)
    defense = EmbeddedDocumentField(defense)
    thirddown = EmbeddedDocumentField(thirddown)
    fourthdown = EmbeddedDocumentField(fourthdown)
    goaltogo = EmbeddedDocumentField(goaltogo)
    redzone = EmbeddedDocumentField(redzone)
    kicks = EmbeddedDocumentField(kicks)
    fieldgoals = EmbeddedDocumentField(fieldgoals)
    punts = EmbeddedDocumentField(punts)
    rushing = EmbeddedDocumentField(rushing)
    kickreturns = EmbeddedDocumentField(kickreturns)
    puntreturns = EmbeddedDocumentField(puntreturns)
    miscreturns = EmbeddedDocumentField(miscreturns)
    record = EmbeddedDocumentField(record)
    conversions = EmbeddedDocumentField(conversions)
    kickoffs = EmbeddedDocumentField(kickoffs)
    fumbles = EmbeddedDocumentField(fumbles)
    penalties = EmbeddedDocumentField(penalties)
    touchdowns = EmbeddedDocumentField(touchdowns)
    interceptions = EmbeddedDocumentField(interceptions)
    firstdowns = EmbeddedDocumentField(firstdowns)

    meta = {"collection": "SeasonStatOppo"}  # Specify the collection name

    def __str__(self):
        return f"SeasonStatOppo: {str(self.tojson())}"

    def save(self, *args, **kwargs):
        if hasattr(self, 'teamid') and hasattr(self, 'seasonid'):
            self._id = f"{self.teamid}_{self.seasonid}"
        super(SeasonStatOppo, self).save(*args, **kwargs)
