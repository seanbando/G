"""Writes the shot plans for chapters 04 to 09 and the outro (shots6.json ... shots9.json). One row per shot:
  (id, end_time, kind, narration line, what it shows, extra fields)
Each shot starts where the one before ends, so the cut times are the END word times from vo-words.json.
  python make_plans.py        -> rewrites shots6.json (and later ones as they are added)"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {
    "A": "Search for alleged cop killer instills fear in Pa. community - CBS Evening News (720p, h264).mp4",
    "B": "Slain cop's cuffs used to arrest Frein - CNN (720p, h264).mp4",
    "D": "Authorities Identify Suspect in Pennsylvania Barracks Shooting - ABC News (720p, h264).mp4",
    "E": "Eric Frein manhunt Suspect may have left letter - CBS Evening News (720p, h264).mp4",
    "F": "Police discovers journal of Pennsylvania cop killer suspect - CBS Mornings (720p, h264).mp4",
    "M": "Pa. breathes easier after capture of Eric Frein - CBS Evening News (720p, h264).mp4",
    "N": "wnep-novak-jeep-screen-recording.mp4",
    "W": "hangar-screen-recording-2026-11-19.mp4",
    "T": "Pike County DA Ray Tonkin responds to Eric Frein's Sentence of Death - Straus News (1080p, h264).mp4",
    "J": "Eric Frein Notice of Execution signed for man responsible for killing PA State Trooper - WTAJ News (1080p, h264).mp4",
}
CROP = {"A": "1102:620:0:0", "E": "1102:620:0:0", "D": "896:504:192:0", "B": "853:480:213:0", "F": "996:560:142:0",
        "N": "1840:1035:40:0", "J": "1422:800:249:0"}
TAG = {"A": "source-cbs-news.png", "E": "source-cbs-news.png", "F": "source-cbs-news.png", "M": "source-cbs-news.png",
       "D": "source-abc-news.png", "B": "source-cnn.png", "N": "source-wnep.png", "W": "source-wnep.png",
       "T": "source-straus-news.png", "J": "source-wtaj.png"}
P = "media/photos/"
OSM = "source-openstreetmap.png"
PSP = "source-pennsylvania-state-police.png"
BARRACKS = {"lat": 41.3871, "lon": -75.1310}
CANADENSIS = {"lat": 41.192, "lon": -75.2513}
AIRFIELD = {"lat": 41.0624, "lon": -75.2534}


def clip(src, t_in, **kw):
    d = {"kind": "clip", "src": src, "in": t_in, "tag": TAG[src], "push": 0.025}
    if src in CROP:
        d["crop"] = CROP[src]
    d.update(kw)
    return d


def still(src, at, **kw):
    d = {"kind": "still", "src": src, "at": at, "tag": TAG[src], "push": 0.05}
    if src in CROP:
        d["crop"] = CROP[src]
    d.update(kw)
    return d


def image(name, tag, **kw):
    d = {"kind": "image", "img": name if name.startswith(("media/", "../")) else P + name, "push": 0.045}
    if tag:
        d["tag"] = tag
    d.update(kw)
    return d


def quote(lines, who, at, **kw):
    c = {"mode": "quote", "lines": lines, "who": who, "at": at}
    c.update(kw)
    return {"kind": "card", "card": c}


def doc(img, marks, tag, **kw):
    c = {"mode": "doc", "img": img if img.startswith("media/") else P + img, "marks": marks}
    c.update(kw)
    return {"kind": "card", "card": c, "tag": tag}


def obj(name, **kw):
    d = {"kind": "obj", "obj": name}
    d.update(kw)
    return d


def write(fn, start, out, dirname, chapter, rows, types):
    shots, t = [], start
    for sid, end, spec, line, what in rows:
        s = {"id": sid, "start": round(t, 2), "end": end, "line": line, "what": what}
        s.update(spec)
        if s["kind"] == "clip":
            s["out"] = round(s["in"] + (end - t), 2)      # real footage plays at its own speed
        shots.append(s)
        t = end
    plan = {"vo": "saylo/videos/02-frein/voiceover-full.mp3", "fps": 30, "start": start, "end": t, "out": out, "dir": dirname,
            "chapter": chapter, "types": types, "src": SRC, "shots": shots}
    io.open(os.path.join(HERE, fn), "w", encoding="utf-8").write(json.dumps(plan, ensure_ascii=False, indent=1))
    print(fn, len(shots), "shots", start, "-", t)


# ------------------------------------------------------------------ 04 The Search + 05 What He Left Behind
ST = "stamp"
rows6 = [
    (401, 328.60, image("33-thecitizensvoice-cruisers-field.jpg", "source-the-times-tribune.png", stamp={"line": "THE SEARCH", "sub": "CHAPTER 04", "at": 326.7}),
     "The search that followed was enormous.", "real photo: State Police cars filling a field; chapter lettering types on"),
    (402, 331.78, image("35-tactical-team-ghows.webp", "source-pocono-record.png"), "Over its seven weeks, more than", "real photo: a tactical team walking up a road"),
    (403, 333.62, image("ca-times-brightspot.jpg", "source-los-angeles-times.png"), "a thousand officers from state police,", "real photo: a line of State Police troopers with rifles (credited to the Los Angeles Times, where the creator's copy was published)"),
    (404, 335.22, image("18b-buzzfeednews-fbi-page.png", "source-fbi.png", fit="contain"), "the FBI,", "the FBI Ten Most Wanted page"),
    (405, 337.12, still("M", 84.3, push=0.07), "the US Marshals,", "real: the marshals team"),
    (406, 338.74, clip("D", 77.2), "and departments across the region took part.", "real: police vehicles along a wooded road"),
    (407, 342.38, clip("E", 36.6), "At one stage, police said their focus was an area of", "real: Bivens briefing reporters in front of a map"),
    (408, 345.54, {"kind": "map2", "tag": OSM, "map": {"center": [41.192, -75.2513], "span": 22, "move": "pull", "pins": [dict(CANADENSIS, label="CANADENSIS", amber=True, at=100)],
                                                       "stamp": "ABOUT 5 SQUARE MILES", "sub": "STEEP, WOODED GROUND", "at": 342.45}},
     "roughly five square miles of steep, wooded ground.", "road map around Canadensis; the figure types on (no boundary drawn: the exact area is not in our sources)"),
    (409, 348.32, image("AP-manhunt-snow-hill-road.jpg", "source-ap-the-times-tribune.png", stamp={"line": "SNOW HILL ROAD", "sub": "PRICE TOWNSHIP  ·  SEPT 30, 2014", "at": 345.7}),
     "Later, a neighborhood called Snow Hill Falls", "real photo: troopers confer on Snow Hill Road; the place types on"),
    (410, 350.66, clip("E", 44.2), "got a lot of attention, though police said they were", "real: troopers walking a road"),
    (411, 352.82, image("36-abcnewsgo.jpg", "source-abc-news.png"), "searching other places too.", "real photo: searchers spread through forest"),
    (412, 356.16, clip("A", 44.5), "For people who lived there, normal life stopped.", "real: a resident talking to CBS"),
    (413, 357.54, image("7Y7YM5UU.jpg", None, push=0.06), "Roads were blocked.", "real photo: two armed troopers at a roadside (outlet unknown: used without a watermark, creator's decision Nov 25, 2026)"),
    (414, 359.24, quote(["SCHOOLS CLOSED"], "POCONO MOUNTAIN SCHOOL DISTRICT", 357.6, size=0.24), "Schools closed at times.", "typed card"),
    (415, 362.70, image("25-canadensis.jpg", "source-bonnachoven-cc0.png"), "Local businesses lost money as visitors stayed away.", "real photo: the empty main road through Canadensis"),
    (416, 365.00, clip("M", 116.7), "And in Barrett Township, door-to-door", "real: a house decorated for Halloween"),
    (417, 367.87, quote(["TRICK-OR-TREATING", "CANCELED"], "BARRETT TOWNSHIP  ·  OCTOBER 2014", 365.1, size=0.22), "trick-or-treating was canceled for Halloween.", "typed card"),
    (418, 370.63, still("M", 117.6, push=0.03), "Remember that. It comes back too.", "real: the Halloween decorations, held"),
    (419, 375.77, clip("F", 42.5), "And at one point, state police said searchers had seen a man they believed was Frein", "real: Bivens at the podium"),
    (420, 380.55, image("26a-bog-forest.jpg", "source-famartin-cc-by-sa-4-0.png", push=0.03, stamp={"line": "75 TO 100 YARDS", "sub": "THROUGH THICK WOODS", "at": 376.0}),
     "somewhere between seventy-five and a hundred yards away through thick woods.", "real photo: dense Pocono woods; the distance types on"),
    (421, 381.97, {"kind": "open", "as": 119}, "They couldn't reach him.", "3D: the amber figure walking away into the trees"),
    (422, 384.69, image("hangar-exterior.jpg", "source-reuters.png", crop="962:541:0:66"), "Here's something to keep in mind through this next part.", "real photo: the hangar"),
    (423, 388.41, quote(["A NOTEBOOK", "AT THE HANGAR"], "FOUND WHEN HE WAS CAUGHT", 385.3, size=0.22), "When they finally caught him, there was a notebook at that hangar.", "typed card (the 3D notebook read badly: creator's note Nov 25, 2026)"),
    (424, 394.35, image("hangar-interior-reuters-abc.jpg", "source-reuters.png", push=0.03), "It's the closest thing we have to hearing what those forty-eight days were like from his side. We'll get to it.", "real photo: inside the hangar, officers with flashlights"),
    (426, 397.79, image("09d-campsite-default.jpg", PSP, stamp={"line": "WHAT HE LEFT BEHIND", "sub": "CHAPTER 05  ·  SEPT 29, 2014", "at": 394.5}),
     "On September twenty-ninth, searchers found a campsite.", "real police photo: the campsite; chapter lettering types on"),
    (427, 399.91, still("E", 56.0), "There was clothing, ammunition,", "real police photo: bags and clothing at the campsite"),
    (428, 401.65, obj("checkbook"), "Frein's checkbook,", "3D object: a chequebook"),
    (429, 403.29, clip("E", 52.3), "and two explosive devices.", "real: Bivens announcing it (the devices are never shown close)"),
    (430, 406.97, quote(["FULLY FUNCTIONAL"], "LT. COL. GEORGE BIVENS, ON THE TWO DEVICES", 404.9, size=0.24), "Bivens described them as fully functional pipe bombs,", "typed card"),
    (431, 411.39, clip("E", 37.5, zoom=1.25, cx=0.5, cy=0.2), "and he said he believed Frein had left them behind because he was under pressure.", "real: Bivens, punched in"),
    (432, 415.25, quote(["A TRASH BAG", "NEAR THE CAMPSITE"], "COLLECTED SEPT 30, 2014", 411.6, size=0.22), "The next day, an agent collected a trash bag near the site.", "typed card (the 3D rubbish bag read badly)"),
    (433, 419.29, obj("pages", rate=0.08), "Inside were three torn notebook pages describing the attack.", "3D object: three torn pages (writing not legible)"),
    (434, 422.37, doc("20-inquirer-headline.png", [[0.615, 0.2, 0.975, 0.4, 420.1], [0.012, 0.42, 0.105, 0.6, 421.3]], "source-the-philadelphia-inquirer.png", wide=True),
     "That's where the line about taking the shot came from.", "the Inquirer headline again, highlighter on the quote"),
    (435, 425.17, clip("F", 96.6, stamp={"line": "OCT 8, 2014", "sub": "FREIN STILL AT LARGE", "at": 422.5}), "On October eighth, with Frein still out there,", "real: Bivens at the podium beside the wanted photos; date types on"),
    (436, 429.39, clip("F", 40.3), "Bivens stood in front of reporters and read from those pages out loud.", "real: Bivens reading the pages"),
    (437, 432.09, clip("E", 28.3), "Then the search went on for three more weeks.", "real: troopers searching along a creek"),
    (438, 436.85, image("33-thecitizensvoice-cruisers-field.jpg", "source-the-times-tribune.png", crop="900:506:120:20", stamp={"line": "$11,000,000", "sub": "STATE POLICE COST", "at": 434.25}),
     "By the end, state police put their own cost at about eleven million dollars.", "real photo: the field of police cars, closer; the figure types on at the words"),
    (439, 439.99, image("34-armored-PPO235.jpg", None), "That doesn't count what the FBI and the Marshals spent.", "real photo: two armoured police vehicles on a wooded road (outlet unknown: used without a watermark, creator's decision Nov 25, 2026)"),
    (440, 443.07, quote(["DAY 48"], "OCT 30, 2014", 440.1, size=0.4), "October thirtieth, day forty-eight.", "typed card"),
]
write("shots6.json", 326.60, "frein_s5_search.mp4", "shots6", "The Search / What He Left Behind", rows6,
      [[326.7, "short"], [342.45, "medium"], [345.7, "medium"], [357.6, "short"], [365.1, "medium"], [376.0, "medium"], [385.3, "medium"], [394.5, "medium"], [404.9, "short"], [411.6, "medium"], [422.5, "short"], [434.25, "short"], [440.1, "short"]])

# ------------------------------------------------------------------ 06 The Hangar (and the night of the arrest)
R2 = "shots2/"
rows7 = [
    (501, 445.41, clip("W", 17.4, crop="1248:702:520:0", stamp={"line": "THE HANGAR", "sub": "CHAPTER 06  ·  OCT 30, 2014", "at": 443.2}),
     "So why were the Marshals at that airfield at all?", "real: helicopter view of the hangar; chapter lettering types on"),
    (502, 447.83, clip("M", 80.6), "They weren't following a tip.", "real: Malkowski at the map on the vehicle"),
    (503, 453.15, {"kind": "map2", "tag": OSM, "map": {"center": [41.225, -75.19], "span": 62, "move": "pull",
                                                       "pins": [dict(BARRACKS, label="BARRACKS", amber=False, at=100), dict(AIRFIELD, label="BIRCHWOOD-POCONO AIRPARK", amber=True, at=451.4)]}},
     "State police had asked them to clear the abandoned resort, the old Birchwood Pocono Airpark", "road map: the airpark pinned as it is named, the barracks to the north"),
    (504, 455.87, {"kind": "reuse", "from": R2 + "S11.mp4", "at": 0.0, "fit": True}, "near Tannersville, and they were working through it.", "3D callback: the line of marshals crossing the field"),
    (505, 457.97, clip("M", 84.6, nametag={"name": "SCOTT MALKOWSKI", "role": "DEPUTY U.S. MARSHAL", "at": 456.0}), "Malkowski said afterward,", "real: Malkowski; name tag types on"),
    (506, 462.25, quote(["“WE JUST HAD A HUNCH", "THAT IF WE WERE ON THE RUN,", "THIS IS A PLACE", "WE WOULD HIDE.”"], "DEPUTY U.S. MARSHAL SCOTT MALKOWSKI", 458.0, size=0.15),
     "\"We just had a hunch that if we were on the run, this is a place we would hide.\"", "typed quote card, line by line"),
    (507, 463.99, {"kind": "reuse", "from": R2 + "S24.mp4", "at": 0.0, "fit": True}, "You know what happened next.", "3D callback: he steps out of the trees"),
    (508, 465.37, {"kind": "reuse", "from": R2 + "S31.mp4", "at": 0.2, "fit": True}, "The black hat,", "3D callback: the black hat"),
    (509, 466.73, {"kind": "reuse", "from": R2 + "S33.mp4", "at": 0.0, "fit": True}, "the order to get down,", "3D callback: he goes to his knees"),
    (510, 467.83, {"kind": "reuse", "from": R2 + "S39.mp4", "at": 0.4, "fit": True}, "his name.", "callback: the FBI photo and his name"),
    (511, 470.61, quote(["TWO ACCOUNTS"], "OF HOW HIS FACE WAS SCRAPED", 467.9, size=0.3), "There's one thing the accounts don't agree on.", "typed card"),
    (512, 474.67, clip("B", 54.6, zoom=1.22, cx=0.15, cy=1.0), "An early public account said nobody was hurt during the capture,", "real: the State Police commissioner at the microphones"),
    (513, 476.45, image("32-ap-perp-walk.jpg", "source-associated-press.png", push=0.0), "but Frein's face was scraped,", "real photo, 1.8 seconds, wide, no zoom: the perp walk"),
    (514, 481.03, {"kind": "open", "as": 38}, "and the Marshals themselves said that happened while he was held face down on the pavement.", "3D: the crane up over him on the ground, marshals around"),
    (515, 484.37, quote(["BOTH VERSIONS", "ARE ON THE RECORD"], "EARLY PUBLIC ACCOUNT  ·  U.S. MARSHALS", 481.1, size=0.22), "Both versions are on the record, so you're getting both.", "typed card"),
    (516, 486.37, image("hangar-exterior.jpg", "source-reuters.png", crop="962:541:0:66", push=0.04), "He wasn't armed in that field.", "real photo: the hangar and the field (the 3D open-hand callback read badly; replaced Nov 25, 2026)"),
    (517, 489.99, image("hangar-interior-reuters-abc.jpg", "source-reuters.png", push=0.05), "There were weapons inside the hangar, and so was the notebook.", "real photo: inside the hangar"),
    (519, 493.35, quote(["THE LONGER JOURNAL"], "NOT THE THREE PAGES FROM THE TRASH BAG", 490.1, size=0.22), "This was the longer journal, not the three pages from the trash bag,", "typed card (the 3D notebook read badly: creator's note Nov 25, 2026)"),
    (520, 497.01, still("E", 68.6, push=0.04, tag=PSP, crop="664:374:307:20"), "and it doesn't read like a soldier on a mission.", "police-released photo: Frein in re-enactor uniform"),
    (521, 502.85, quote(["“SLEPT LIKE A HUMAN", "FIRST TIME IN TWO WEEKS.”"], "ERIC FREIN'S JOURNAL, SEPT 25  ·  COURT RECORD", 498.7, size=0.19),
     "On September twenty-fifth, he wrote that he slept like a human first time in two weeks.", "typed journal quote, amber bar"),
    (522, 509.45, quote(["“THIRTY DAYS.", "A LOT LONGER THAN", "I EXPECTED TO LAST.”"], "ERIC FREIN'S JOURNAL, OCT 11  ·  COURT RECORD", 504.3, size=0.19),
     "On October eleventh, he wrote, \"Thirty days. A lot longer than I expected to last.\"", "typed journal quote, amber bar"),
    (523, 516.07, obj("laptop", head="STORAGE DRIVE  ·  COURT RECORD", head_at=509.7, lines=[["FILE: A LETTER", 510.9], ["ADDRESSED “MOM AND DAD”", 513.3]], rate=0.05, angle=12, elev=16, last=True),
     "Police also recovered a file on a storage drive. It was a letter addressed Mom and Dad,", "3D object: a screen; the file types on as it is described"),
    (524, 521.73, quote(["“THE TIME SEEMS RIGHT", "FOR A SPARK TO IGNITE A FIRE", "IN THE HEARTS OF MEN.”"], "LETTER ADDRESSED “MOM AND DAD”  ·  COURT RECORD", 516.2, size=0.16),
     "and in it, he wrote that, \"The time seems right for a spark to ignite a fire in the hearts of men.\"", "typed quote card"),
    (525, 526.67, quote(["FILE CREATED", "DEC 29, 2013"], "COURT RECORD", 522.5, size=0.24), "The file had been created on December twenty-ninth, twenty-thirteen,", "typed card"),
    (526, 529.13, quote(["LAST ACCESSED", "OCT 6, 2014"], "COURT RECORD", 526.7, size=0.24), "and last accessed on October sixth, twenty-fourteen.", "typed card"),
    (527, 536.15, obj("laptop", head="FILE DATES ONLY", head_at=529.3, lines=[["WHEN IT WAS MADE", 533.0], ["WHEN IT WAS LAST OPENED", 534.7]], rate=0.04, angle=-14, elev=18, last=True),
     "Those dates don't tell us when any particular line was written, only when the file was made and when it was last opened.", "3D object: the screen again; the two things the dates do tell us type on"),
    (528, 539.49, quote(["RECORDED INTERVIEW"], "OCT 30–31, 2014", 536.3, size=0.22), "That night, investigators questioned him on video.", "typed card"),
    (529, 542.29, quote(["“ASSASSINATION”"], "HIS WORD, FROM THE INTERVIEW", 540.6, size=0.24), "He called the killing an assassination,", "typed card"),
    (530, 547.19, quote(["“WAKE PEOPLE UP”"], "FROM THE RECORDED INTERVIEW", 545.0, size=0.24), "and the phrase that came out of that interview was that he'd wanted to wake people up.", "typed card; the words appear when they are said"),
    (531, 550.63, clip("M", 119.6, nametag={"name": "RAY KOWALSKI", "role": "RESIDENT", "at": 547.4}), "Back in Barrett Township, the news spread fast.", "real: a resident the morning after; name tag types on"),
    (532, 553.21, doc("13b-cbs-halloween-headline.png", [[0.02, 0.055, 0.74, 0.145, 551.4]], "source-cbs-news.png"), "The next day was Halloween,", "the CBS/AP article, highlighter on its headline"),
    (533, 556.55, doc("13b-cbs-halloween-headline.png", [[0.535, 0.882, 0.87, 0.915, 553.6], [0.02, 0.925, 0.675, 0.957, 554.4]], "source-cbs-news.png"),
     "and officials told families that trick-or-treating could go ahead after all.", "the same article, highlighter on \"Trick-or-treating is on tomorrow night from 6 to 8 in Barrett Township\""),
]
write("shots7.json", 443.07, "frein_s6_hangar.mp4", "shots7", "The Hangar", rows7,
      [[443.2, "medium"], [451.4, "medium"], [456.0, "medium"], [458.0, "long"], [467.9, "short"], [481.1, "medium"], [490.1, "medium"], [498.7, "medium"], [504.3, "medium"],
       [509.7, "medium"], [516.2, "long"], [522.5, "short"], [526.7, "short"], [529.3, "short"], [536.3, "short"], [540.6, "short"], [545.0, "short"], [547.4, "short"]])

# ------------------------------------------------------------------ 07 The Verdict + 08 The Confession
P28, P29, P1 = "19a-court-opinion-p28.png", "19b-court-opinion-p29.png", "19c-court-opinion-p1-caption.png"
COURT = "source-pa-supreme-court.png"
rows8 = [
    (601, 559.89, image("23-courthouse-milford.jpg", "source-beyond-my-ken-cc-by-sa-4-0.png", stamp={"line": "THE VERDICT", "sub": "CHAPTER 07", "at": 556.7}),
     "Before we go back to that night, here's how this ended in court.", "real photo: Pike County Courthouse, Milford; chapter lettering types on"),
    (602, 563.73, image("41-poconorecord.webp", "source-pocono-record.png", stamp={"line": "APRIL 2017", "sub": "PIKE COUNTY COURTHOUSE, MILFORD", "at": 560.5}),
     "The trial came in April twenty-seventeen in Pike County.", "real photo: the prosecution team walking to court; date types on"),
    (603, 566.21, {"kind": "card", "tag": PSP, "card": {"mode": "portrait", "img": "media/cuts/douglass-portrait.png", "name": "ALEX DOUGLASS", "sub": "TESTIFIED AT THE TRIAL", "size": 0.34, "at": 100}},
     "Alex Douglass testified.", "his official portrait"),
    (604, 569.27, image("14-dailylocal.webp", "source-daily-local-news.png"), "On April nineteenth, the jury convicted Eric Frein on", "real photo: Frein led by a trooper at the trial"),
    (605, 575.45, quote(["GUILTY", "ALL 12 COUNTS"], "APRIL 19, 2017  ·  INCLUDING MURDER AND TERRORISM", 569.3, size=0.3),
     "all twelve counts, including first-degree murder of a law enforcement officer and terrorism.", "typed card"),
    (606, 579.25, image("wnep-a.jpg", "source-wnep.png", crop="1920:700:0:0", fit="contain"), "Then came the penalty phase to decide whether he'd live.", "real: camera crews behind police tape outside court (station caption cropped out)"),
    (607, 586.83, {"kind": "card", "tag": PSP, "card": {"mode": "portrait", "img": "media/cuts/dickson-portrait.png", "name": "BRYON K. DICKSON II", "sub": "HIS WIDOW, TIFFANY DICKSON, TESTIFIED", "size": 0.3, "at": 100,
                                                        "facts": [["APRIL 20, 2017", 579.4]]}},
     "On April twentieth, Bryon Dickson's widow, Tiffany Dickson, testified about raising their two sons without their father.", "Cpl. Dickson's portrait, held (no photos of his family are used)"),
    (608, 590.63, image("23-courthouse-milford.jpg", "source-beyond-my-ken-cc-by-sa-4-0.png", crop="1200:675:360:420", push=0.03), "Frein's parents testified too, asking for his life.", "real photo: the courthouse, closer"),
    (609, 594.35, clip("T", 126.2, nametag={"name": "RAY TONKIN", "role": "PIKE COUNTY DISTRICT ATTORNEY", "at": 590.8}), "On April twenty-sixth, the jury returned a death verdict.", "real: the District Attorney outside the courthouse after the verdict; name tag types on"),
    (610, 597.07, quote(["DEATH"], "APRIL 26, 2017  ·  NO MITIGATING CIRCUMSTANCES FOUND", 594.4, size=0.4), "They found no mitigating circumstances.", "typed card"),
    (611, 600.67, clip("T", 131.0, zoom=1.3, cx=0.55, cy=0.2), "The judge formally imposed the sentence the next day.", "real: Tonkin, punched in"),
    (612, 604.17, quote(["RECORDED STATEMENT"], "CHAPTER 08  ·  THE CONFESSION", 600.8, size=0.22), "Remember that recorded statement from the night of the arrest?", "typed card; chapter lettering"),
    (613, 606.55, image("14-dailylocal.webp", "source-daily-local-news.png", push=0.08), "The jury heard Frein's confession.", "real photo: Frein at the trial, pushing in"),
    (614, 611.45, doc(P1, [[0.27, 0.105, 0.73, 0.128, 608.4], [0.63, 0.502, 0.885, 0.526, 609.6]], COURT), "Two years later, Pennsylvania's highest court said the jury should never have heard it.", "the court opinion: highlighter on the court's name and \"DECIDED: April 26, 2019\""),
    (615, 615.31, doc(P28, [[0.118, 0.481, 0.882, 0.498, 612.8]], COURT), "Frein had repeatedly told investigators he wanted to stop talking.", "opinion p. 28: highlighter on \"unambiguously invoked his right to remain silent on multiple occasions\""),
    (616, 617.05, doc(P28, [[0.118, 0.512, 0.882, 0.529, 615.4]], COURT), "They kept going.", "opinion p. 28: highlighter on \"the officers continued to question Appellant\""),
    (617, 621.79, doc(P29, [[0.50, 0.482, 0.882, 0.499, 617.9], [0.118, 0.513, 0.882, 0.530, 619.2], [0.118, 0.545, 0.882, 0.562, 620.4]], COURT),
     "The rifle from the hangar fired the bullets that killed Dickson and wounded Douglass.", "opinion p. 29: three highlighter sweeps (the bullets, the rifle, the hangar)"),
    (618, 623.77, doc(P29, [[0.70, 0.609, 0.882, 0.626, 622.0], [0.118, 0.640, 0.262, 0.657, 622.6]], COURT), "Frein's DNA was on it.", "opinion p. 29: highlighter on \"Appellant's DNA was on the rifle\""),
    (619, 626.43, obj("pages", angle=-30, rate=0.1), "The handwriting on the torn pages was his.", "3D object: the three torn pages"),
    (620, 629.95, quote(["THE CONFESSION", "DID NOT CHANGE", "THE VERDICT"], "PENNSYLVANIA SUPREME COURT, 2019  ·  “HARMLESS ERROR”", 626.5, size=0.2), "The court ruled that the confession hadn't changed the verdict.", "typed card"),
    (621, 633.37, quote(["CONVICTION: STANDS", "DEATH SENTENCE: STANDS"], "APRIL 26, 2019", 630.0, size=0.2), "The conviction stood, and so did the death sentence.", "typed card"),
    (622, 638.53, quote(["U.S. SUPREME COURT", "DECLINED THE CASE"], "JANUARY 2020", 633.5, size=0.2), "In January twenty-twenty, the US Supreme Court declined to take the case.", "typed card"),
    (623, 642.83, quote(["EXECUTION DATE SET", "JUNE 22, 2020"], "PENNSYLVANIA DEPARTMENT OF CORRECTIONS", 638.7, size=0.22), "Pennsylvania set an execution date for June twenty-second, twenty-twenty.",
     "typed card (the WTAJ clip for this line is a long close-up of his face from the perp walk, so it is not used)"),
    (624, 650.49, quote(["STAYED"], "JUNE 12, 2020  ·  PIKE COUNTY JUDGE", 645.3, size=0.4), "Ten days before it, a Pike County judge put the execution on hold so Frein could continue challenging his conviction and sentence.", "typed card"),
    (625, 655.47, quote(["LAST EXECUTION", "IN PENNSYLVANIA: 1999"], "", 651.1, size=0.22), "Pennsylvania hasn't carried out an execution since nineteen ninety-nine.", "typed card"),
]
write("shots8.json", 556.55, "frein_s7_court.mp4", "shots8", "The Verdict / The Confession", rows8,
      [[556.7, "short"], [560.5, "medium"], [569.3, "medium"], [590.8, "medium"], [594.4, "short"], [600.8, "medium"], [626.5, "medium"], [630.0, "medium"], [633.5, "medium"], [640.3, "medium"], [645.3, "short"], [651.1, "medium"]])

# ------------------------------------------------------------------ 09 The Handoff + outro
rows9 = [
    (701, 658.87, clip("W", 26.6, crop="1248:702:520:0", stamp={"line": "THE HANDOFF", "sub": "CHAPTER 09  ·  OCT 30, 2014", "at": 655.6}),
     "Now go back to October thirtieth, twenty-fourteen.", "real: helicopter view of the hangar (src 26.6-30.0 only: after 32 s the report cuts to a DIFFERENT airport); chapter lettering types on"),
    (702, 660.75, {"kind": "reuse", "from": R2 + "S04.mp4", "at": 0.0, "fit": True}, "The field, the hangar,", "3D callback: the hangar at dusk"),
    (703, 661.97, {"kind": "reuse", "from": R2 + "S31.mp4", "at": 0.2, "fit": True}, "the black hat.", "3D callback: the black hat"),
    (704, 664.75, clip("M", 84.1), "The US Marshals had made the arrest,", "real: the marshals team"),
    (705, 666.91, image("mcall-b.webp", "source-the-morning-call.png"), "but this was a state police case,", "real photo: the Blooming Grove barracks sign"),
    (706, 669.59, {"kind": "card", "tag": PSP, "card": {"mode": "portrait", "img": "media/cuts/dickson-portrait.png", "name": "BRYON K. DICKSON II", "sub": "CORPORAL, PENNSYLVANIA STATE POLICE", "size": 0.3, "at": 100}},
     "and the man they'd caught had killed one of their own.", "Cpl. Dickson's portrait"),
    (707, 673.89, clip("B", 44.3, tag="source-wnep.png"), "So the Marshals handed Eric Frein over to the Pennsylvania State Police,", "real: the arrest night, officers under blue lights"),
    (708, 675.5, clip("B", 38.4, tag="source-wnep.png"), "and the troopers who took him put", "real: officers by a cruiser under red lights, the arrest night"),
    (7081, 678.23, quote(["CORPORAL DICKSON'S", "HANDCUFFS"], "OCT 30, 2014", 675.55, size=0.3), "Corporal Bryon Dickson's handcuffs on him.", "typed card landing on the word handcuffs, music out (the 3D handcuffs looked like a toy; replaced Nov 25, 2026)"),
    (709, 680.37, clip("B", 114.6, tag="source-wnep.png"), "Then they put him in Dickson's patrol car", "real: Frein in the back of the patrol car that night"),
    (710, 682.73, {"kind": "map2", "tag": OSM, "map": {"center": [41.225, -75.19], "span": 62, "move": "push",
                                                       "pins": [dict(AIRFIELD, label="AIRPARK", amber=False, at=100), dict(BARRACKS, label="BLOOMING GROVE BARRACKS", amber=True, at=681.2)],
                                                       "route": [[41.0624, -75.2534], [41.3871, -75.1310]], "route_at": [680.5, 682.3], "stamp": "ABOUT 30 MILES", "sub": "STRAIGHT LINE SHOWN, NOT THE ROAD ROUTE", "at": 680.5}},
     "and drove him back to Blooming Grove.", "road map: an amber line from the airpark to the barracks (a straight line, labelled as such)"),
    (711, 685.71, clip("B", 105.0, nametag={"name": "FRANK NOONAN", "role": "COMMISSIONER, PENNSYLVANIA STATE POLICE", "at": 682.9}), "State Police Commissioner Frank Noonan confirmed it.", "real: Noonan interviewed; name tag types on"),
    (712, 688.93, clip("B", 0.8, zoom=1.22, cx=0.15, cy=1.0, nametag={"name": "TOM CORBETT", "role": "GOVERNOR OF PENNSYLVANIA, 2014", "at": 687.1}), "Pennsylvania's governor at the time, Tom Corbett,", "real: Gov. Corbett at the press conference; name tag types on"),
    (713, 690.95, quote(["“VERY APPROPRIATE”"], "GOV. TOM CORBETT", 689.0, size=0.24), "called it very appropriate.", "typed quote card"),
    (714, 695.65, {"kind": "barracks", "view": "lot", "stamp": {"line": "48 DAYS LATER", "sub": "BLOOMING GROVE BARRACKS", "at": 691.0}, "last": True},
     "Forty-eight days after Corporal Bryon Dickson was killed outside Blooming Grove,", "3D: the barracks lot at night; 48 DAYS LATER types on"),
    (715, 698.35, {"kind": "barracks", "view": "return"}, "his patrol car pulled back into the barracks.", "3D: the cruiser, an amber edge of light on it, turning into the lot (the pay-off of the planted detail)"),
    (716, 704.81, image("11c-phillymag-perp-walk-night.jpg", "source-ap-the-times-tribune.png", push=0.02), "Eric Frein was in the back seat wearing Dickson's handcuffs. So here's my question for you.", "real photo: troopers lead him from the barracks that night; held, slowest push"),
    (718, 709.95, {"kind": "barracks", "view": "cruiser2"}, "The state police chose to bring him back in Dickson's handcuffs in Dickson's car.", "3D: low along the cruiser in its bay"),
    (719, 714.51, quote(["WAS THAT", "THE RIGHT CALL?"], "TELL ME WHAT YOU THINK IN THE COMMENTS", 710.0, size=0.3), "Was that the right call? Tell me what you think in the comments.", "typed question card"),
    (720, 723.85, quote(["WATCH NEXT"], "THE OLYMPIC BOMBER  ·  HIDDEN FOR FIVE YEARS", 714.6, size=0.3),
     "If you want another one about a man who vanished into the woods with the whole country looking for him, watch my video on the Olympic bomber who stayed hidden for five years.", "typed end card, room on the right for YouTube's own end-screen video tile (the old thumbnail is gone: creator's note Nov 25, 2026)"),
    (721, 727.81, quote(["SUBSCRIBE"], "PLENTY MORE COMING", 724.5, size=0.34), "And subscribe if you want more of these. There are plenty more coming.", "typed end card"),
]
write("shots9.json", 655.47, "frein_s8_handoff.mp4", "shots9", "The Handoff / outro", rows9,
      [[655.6, "medium"], [675.55, "medium"], [680.5, "short"], [682.9, "medium"], [687.1, "medium"], [689.0, "medium"], [691.0, "medium"], [710.0, "medium"], [714.6, "medium"], [724.5, "short"]])
