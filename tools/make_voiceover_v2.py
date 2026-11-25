"""Voice-over sheet for scripts in the S001 format (docs/script-format-guide.md).

Usage: python3 tools/make_voiceover_v2.py <script.md> <voiceover.md>

Reads lines like "**S012 · NARRATOR · ~5 s · TAG**" followed by the spoken
sentence, plus "[PAUSE: ...]" beats and "## SECTION" headings. Source tags
and drawing notes are left out: this sheet is only what gets recorded.
"""
import re
import sys

CAST = {
    "NARRATOR": ("Yaboy", "Warm, clear and conversational, like explaining money to a friend."),
    "BUCK": ("Larry", "Cocky dollar bill and the dollar making the trip. Dry, quick, one-sentence gags; never explains."),
    "HAMLET": ("Grampa Werthers", "Grumpy piggy bank the dollar left behind. Lower and slower than Buck; grumbles about spending, warms up to saving."),
}
WPM = 180


def parse(path):
    text = open(path).read()
    title = text.splitlines()[0].lstrip("# ").strip()
    items = []
    for m in re.finditer(r"^## (.+)$|^\*\*(S\d+) · (\w+) · ~\d+ s(?: · ([^*]+))?\*\*\n(.+)$|^\[PAUSE: (.+)\]$",
                         text, re.M):
        if m.group(1):
            items.append(("section", m.group(1)))
        elif m.group(2):
            items.append(("line", m.group(2), m.group(3), (m.group(4) or "").strip(), m.group(5).strip()))
        else:
            items.append(("pause", m.group(6)))
    return title, items


def words(t):
    return len(re.findall(r"[A-Za-z0-9'’-]+", t))


def main(src, dst):
    title, items = parse(src)
    lines = [i for i in items if i[0] == "line"]
    total = sum(words(i[4]) for i in lines)
    out = [f"# Voice-Over Script: {title}", "",
           "Voice-only recording sheet. Every spoken line is numbered (S001, S002 …) and becomes one audio file "
           "with the same number, so the files join back together in order. Sources and drawing notes are in "
           "`script.md`; nothing here except the spoken lines is read aloud.", "",
           "**All numbers, dates and abbreviations are already written out in words.** Read them exactly as written.", "",
           f"## Cast: {len({i[2] for i in lines})} voices", "",
           "| Voice | ElevenLabs voice | Lines | Words | Direction |", "|---|---|---|---|---|"]
    for v, (el, d) in CAST.items():
        ls = [i for i in lines if i[2] == v]
        if ls:
            out.append(f"| **{v}** | {el} | {len(ls)} | {sum(words(i[4]) for i in ls)} | {d} |")
    pauses = [i for i in items if i[0] == "pause"]
    out += ["", f"**Total:** {len(lines)} lines · {total} spoken words · about {total / WPM:.1f} minutes "
            f"at {WPM} words per minute, plus {len(pauses)} silent pause.", "",
            "### Recording notes",
            "- **File names:** name each file after its line, for example `S004_BUCK.mp3`.",
            "- **Silences:** don't worry about silence at the start or end of a file; it's trimmed when the files are joined.",
            "- **The pause** (⏸) is silent and not recorded; it's added when the files are joined.",
            "- **Full sentences:** read every line as one full sentence, including the short Buck and Hamlet gags.",
            "- **Letter by letter:** \"D-T-C-C\" and \"S-I-P-C\" are read one letter at a time; \"U.S.\" is \"you-ess\".",
            "- **After recording:** trim silences and stutters, and check each line before it's used.",
            "", "---", "", "## Part 1: Full script in order", ""]
    for i in items:
        if i[0] == "section":
            out += [f"### {i[1]}", ""]
        elif i[0] == "pause":
            out += [f"> ⏸ PAUSE {i[1]}", ""]
        else:
            tag = f" · {i[3]}" if i[3] else ""
            out += [f"**{i[1]} · {i[2]}**{tag}  ", i[4], ""]
    out += ["---", "", "## Part 2: Lines by voice (for recording sessions)", ""]
    for v in CAST:
        ls = [i for i in lines if i[2] == v]
        if ls:
            out.append(f"### {v} ({len(ls)} lines)\n")
            out += [f"- **{i[1]}:** {i[4]}" for i in ls]
            out.append("")
    open(dst, "w").write("\n".join(out) + "\n")
    print(f"{len(lines)} lines, {total} words, {len(pauses)} pause(s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
