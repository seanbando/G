"""Writes the shot plans for the later chapters (shots6.json ...). One row per shot:
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
    d = {"kind": "image", "img": name if name.startswith("media/") else P + name, "tag": tag, "push": 0.045}
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
    (403, 333.62, image("mcall-a.webp", "source-the-morning-call.png"), "a thousand officers from state police,", "real photo: armed officers on a street"),
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
    (413, 357.54, clip("E", 76.0), "Roads were blocked.", "real: a trooper and cruiser blocking a road"),
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
    (423, 388.41, obj("notebook", rate=0.12), "When they finally caught him, there was a notebook at that hangar.", "3D object: a closed notebook under a lamp, push in"),
    (424, 393.13, image("hangar-interior-reuters-abc.jpg", "source-reuters.png", push=0.03), "It's the closest thing we have to hearing what those forty-eight days were like from his side.", "real photo: inside the hangar, officers with flashlights"),
    (425, 394.35, obj("notebook", angle=-40, rate=0.15), "We'll get to it.", "3D object: the notebook from the other side, closer"),
    (426, 397.79, image("09d-campsite-default.jpg", PSP, stamp={"line": "WHAT HE LEFT BEHIND", "sub": "CHAPTER 05  ·  SEPT 29, 2014", "at": 394.5}),
     "On September twenty-ninth, searchers found a campsite.", "real police photo: the campsite; chapter lettering types on"),
    (427, 399.91, still("E", 56.0), "There was clothing, ammunition,", "real police photo: bags and clothing at the campsite"),
    (428, 401.65, obj("checkbook"), "Frein's checkbook,", "3D object: a chequebook"),
    (429, 403.29, clip("E", 52.3), "and two explosive devices.", "real: Bivens announcing it (the devices are never shown close)"),
    (430, 406.97, quote(["FULLY FUNCTIONAL"], "LT. COL. GEORGE BIVENS, ON THE TWO DEVICES", 404.9, size=0.24), "Bivens described them as fully functional pipe bombs,", "typed card"),
    (431, 411.39, clip("E", 37.5, zoom=1.25, cx=0.5, cy=0.2), "and he said he believed Frein had left them behind because he was under pressure.", "real: Bivens, punched in"),
    (432, 415.25, obj("bag", rate=0.08), "The next day, an agent collected a trash bag near the site.", "3D object: a tied rubbish bag under a lamp"),
    (433, 419.29, obj("pages", rate=0.08), "Inside were three torn notebook pages describing the attack.", "3D object: three torn pages (writing not legible)"),
    (434, 422.37, doc("20-inquirer-headline.png", [[0.615, 0.2, 0.975, 0.4, 420.1], [0.012, 0.42, 0.105, 0.6, 421.3]], "source-the-philadelphia-inquirer.png", wide=True),
     "That's where the line about taking the shot came from.", "the Inquirer headline again, highlighter on the quote"),
    (435, 425.17, clip("F", 96.6, stamp={"line": "OCT 8, 2014", "sub": "FREIN STILL AT LARGE", "at": 422.5}), "On October eighth, with Frein still out there,", "real: Bivens at the podium beside the wanted photos; date types on"),
    (436, 429.39, clip("F", 40.3), "Bivens stood in front of reporters and read from those pages out loud.", "real: Bivens reading the pages"),
    (437, 432.09, clip("E", 28.3), "Then the search went on for three more weeks.", "real: troopers searching along a creek"),
    (438, 436.85, image("33-thecitizensvoice-cruisers-field.jpg", "source-the-times-tribune.png", crop="900:506:120:20", stamp={"line": "$11,000,000", "sub": "STATE POLICE COST", "at": 434.25}),
     "By the end, state police put their own cost at about eleven million dollars.", "real photo: the field of police cars, closer; the figure types on at the words"),
    (439, 439.99, image("TMC-FreinManhunt-troopers-stage.webp", "source-the-morning-call.png"), "That doesn't count what the FBI and the Marshals spent.", "real photo: troopers and armoured trucks staged on a road"),
    (440, 443.07, quote(["DAY 48"], "OCT 30, 2014", 440.1, size=0.4), "October thirtieth, day forty-eight.", "typed card"),
]
write("shots6.json", 326.60, "frein_s5_search.mp4", "shots6", "The Search / What He Left Behind", rows6,
      [[326.7, "short"], [342.45, "medium"], [345.7, "medium"], [357.6, "short"], [365.1, "medium"], [376.0, "medium"], [394.5, "medium"], [404.9, "short"], [422.5, "short"], [434.25, "short"], [440.1, "short"]])
