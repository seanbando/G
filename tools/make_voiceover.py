"""Build a voice-over recording sheet from a script file.

Usage: python3 tools/make_voiceover.py <script.md> <output.md>

Script format: first paragraph is the title; paragraphs are separated by a
blank line; character lines start with "ROLE NAME:"; drawing cues are
"[DRAW: ...]" or "[VISUAL NOTE: ...]" paragraphs, and silent beats are
"[PAUSE: ...]" paragraphs. Everything else is NARRATOR. Each spoken
paragraph is one whiteboard scene.
"""
import re
import sys

CAST = {
    "NARRATOR": ("Main host. Warm, clear, conversational, like explaining money to a friend. Steady pace, about 160 words per minute.", "The whole story"),
    "YOU": ("The viewer's inner voice. Curious and a little surprised. Younger and more casual than the narrator. Must sound clearly different from the narrator.", "Asks the questions the audience is thinking"),
    "THE APP": ("The investing app, personified. Upbeat, efficient, slightly robotic customer-service tone.", "Confirms the order"),
    "THE MARKET MAKER": ("A trading firm, personified. Relaxed, confident, a little salesy, like a currency-booth clerk. Not shady.", "Quotes the buy and sell prices (stop two)"),
    "THE EXCHANGE": ("The stock exchange, personified. Calm, official, matter-of-fact, like an announcer or matchmaker.", "Matches buyer and seller (stop three)"),
    "THE SELLER": ("A retired teacher in Arizona. Warm, friendly, unhurried.", "The stranger who gets your dollar (stop four)"),
    "THE CLEARINGHOUSE": ("The D-T-C-C, personified. Steady, wise, a bit strict, like a referee.", "Makes the trade official (stop five)"),
    "MAYA": ("A young investor. Bright, a little proud of her savings.", "Buys ten shares"),
    "JORDAN": ("A young buyer. Relaxed and upbeat.", "Buys Maya's shares for more"),
}
DRAW = {
    "YOU": "a stick-figure viewer holding a phone",
    "THE APP": "a phone with a face",
    "THE MARKET MAKER": "a currency-booth clerk behind a window with two price signs",
    "THE EXCHANGE": "a building with a face",
    "THE SELLER": "a retired teacher holding a roofing estimate",
    "THE CLEARINGHOUSE": "a referee standing between two buildings",
    "MAYA": "a young woman holding ten share certificates",
    "JORDAN": "a young buyer holding cash",
}


def parse(path):
    paras = open(path).read().strip().split("\n\n")
    title, lines, cues = paras[0].strip(), [], []
    role_re = re.compile(r"^(%s):\s*(.*)$" % "|".join(re.escape(r) for r in CAST if r != "NARRATOR"), re.S)
    for p in paras[1:]:
        p = p.strip()
        for tag in ("[VISUAL NOTE:", "[DRAW:"):
            if p.startswith(tag):
                cues.append("🎨 Draw: " + p[len(tag):].rstrip("]").strip())
                break
        else:
            tag = None
        if tag:
            continue
        if p.startswith("[PAUSE:"):
            cues.append("⏸ PAUSE " + p[len("[PAUSE:"):].rstrip("]").strip())
            continue
        m = role_re.match(p)
        voice, text = (m.group(1), m.group(2)) if m else ("NARRATOR", p)
        lines.append((f"VO-{len(lines) + 1:02d}", voice, text, cues))
        cues = []
    return title, lines


def words(t):
    return len(t.split())


WPM = 180  # measured pace of the narrator voice


def secs(t):
    return round(words(t) / WPM * 60)


ASSETS = [
    "**The dollar:** a dollar bill with a simple face. It's the hero and appears in almost every scene.",
    "**The road map:** five stops left to right (1 Your App, 2 Market Maker, 3 Exchange, 4 Seller, 5 Clearinghouse). Draw it once and reuse it between stops, adding a check mark each time.",
    "**The \"OWNER: ???\" paper:** set up in the opening and paid off at Stop 5, where the question marks become \"Cede & Co.\"",
    "**Pizza:** used for the share-price trap and for \"one bite\" of a share.",
    "**The stopwatch:** \"less than 1 second.\" Used after Stop 5 and at the end.",
    "**Characters:** draw each one once and reuse the drawing every time they speak.",
]


def build(title, lines):
    first_you = next(l[0] for l in lines if l[1] == "YOU")
    total = sum(words(l[2]) for l in lines)
    out = [
        f"# Voice-Over Script: {title}\n",
        "Recording sheet for the whiteboard video. Every spoken line is numbered (VO-01, VO-02 …) so audio files can be named to match and dropped onto the timeline in order.\n",
        "**All numbers, dollar amounts, dates, times and abbreviations are written out in words**, so read them exactly as written.\n",
        f"## Cast: {len(CAST)} voices\n",
        "| # | Voice | Lines | Words | Character direction | Role in the story |",
        "|---|---|---|---|---|---|",
    ]
    for i, (v, (direction, role)) in enumerate(CAST.items(), 1):
        ls = [l for l in lines if l[1] == v]
        out.append(f"| {i} | **{v}** | {len(ls)} | {sum(words(l[2]) for l in ls)} | {direction} | {role} |")
    out += [
        "",
        f"**Total:** {len(lines)} lines (one scene each) · {total} spoken words · about {total / WPM:.1f} minutes of audio at the narrator's pace of {WPM} words per minute, before pauses. The longest scene is about {max(secs(l[2]) for l in lines)} seconds.\n",
        "**Pause-and-guess breaks:** the ⏸ cues are silent beats where the question stays on screen so viewers can guess. Hold the drawing for the stated time before the next line.\n",
        "### Recurring drawings (draw once, reuse)",
        *[f"- {a}" for a in ASSETS],
        *[f"- **{k}:** {d}" for k, d in DRAW.items()],
        "",
        "### Recording tips",
        "- **Every character gets its own voice,** so viewers can tell who is talking without seeing the drawing. **YOU** especially must never sound like the narrator.",
        f"- **Name each file after its line ID,** for example `{first_you}_YOU.wav`, so the editor can line the audio up in order.",
        "- **Leave about half a second of silence** at the start and end of each file. Drawing usually takes longer than speaking, so the editor will add gaps.",
        "- **Read every line as a full sentence.** Don't clip character lines into short fragments.",
        "- **Letter-by-letter names:** \"D-T-C-C\" and \"S-I-P-C\" are written with hyphens so they're read one letter at a time, and \"U.S.\" is read \"you-ess\".",
        "",
        "---",
        "",
        "## Part 1: Full script in order",
        "",
        "Each line is one whiteboard scene. 🎨 says what to draw while the line plays, and ⏸ marks a silent \"pause and guess\" break with on-screen text. Neither is read aloud. Times are estimates.",
        "",
    ]
    for id_, v, t, vis in lines:
        for cue in vis:
            out.append(f"> {cue}\n")
        out.append(f"**{id_} · {v}** · ~{secs(t)} s  \n{t}\n")
    out += ["---", "", "## Part 2: Lines by voice (for recording sessions)", ""]
    for v in CAST:
        ls = [l for l in lines if l[1] == v]
        out.append(f"### {v} ({len(ls)} lines)\n")
        out += [f"- **{id_}:** {t}" for id_, _, t, _ in ls]
        out.append("")
    out += ["---", "", "## Part 3: Drawing and pause cues (for the animator and editor)", ""]
    out += [f"- **Before {id_}:** {cue}" for id_, _, _, vis in lines for cue in vis]
    out.append("- **Every character line:** draw the speaker with a speech bubble: " +
               "; ".join(f"{k} = {d}" for k, d in DRAW.items()) + ".")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    title, lines = parse(sys.argv[1])
    open(sys.argv[2], "w").write(build(title, lines))
    print(f"{len(lines)} lines, {sum(words(l[2]) for l in lines)} words")
