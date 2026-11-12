"""Check a script against the CashleyFinance script system (docs/script-system.md).

Usage: python3 tools/check_script.py <script.md>

Reads the spoken lines (drawing notes and pauses are skipped) and reports
what breaks the Part 3 humanization and text-to-speech rules. Each spoken
paragraph counts as a paragraph. Character lines are checked too, but rules
written for the narrator (rhythm per paragraph) only apply to paragraphs of
three or more sentences.
"""
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_voiceover import parse  # noqa: E402

BANNED = {
    "AI transition": ["furthermore", "moreover", "in conclusion", "consequently", "in summary", "as such",
                      "hence", "thus", "therefore", "accordingly", "additionally"],
    "hedge": ["it may seem", "on the other hand", "it remains to be seen", "while it is true",
              "some might argue", "it is important to note", "it's important to note", "it could be argued",
              "some experts believe", "it is generally accepted", "perhaps", "potentially", "possibly",
              "it's worth noting", "it is worth noting", "interestingly enough"],
    "buzzword": ["delve", "crucial", "comprehensive", "robust", "landscape", "paradigm", "leverage",
                 "innovative", "cutting-edge", "game-changer", "groundbreaking", "transformative",
                 "holistic", "seamless", "dynamic", "multifaceted", "pivotal", "optimize", "synergy"],
    "filler": ["in today's world", "in the realm of", "at the end of the day", "the fact of the matter is",
               "it goes without saying", "needless to say", "a testament to", "without further ado",
               "in the world of", "digital age"],
    "overused descriptor": ["plethora", "myriad", "paramount", "invaluable", "remarkable", "significant",
                            "substantial", "profound", "essential", "vital"],
}
WEAK_STARTS = ("But", "And", "So", "Then", "After that")
GENERIC_VERBS = ["was", "were", "had", "made", "got", "went", "said"]


def sentences(text):
    parts = re.split(r"(?<=[.?!])\s+(?=[\"'A-Z])", text.strip())
    return [p for p in parts if p]


def words(s):
    return len(re.findall(r"[A-Za-z0-9'’-]+", s))


def main(path):
    _, lines = parse(path)
    problems, notes = [], []
    all_sents = []

    for line_id, voice, text, _ in lines:
        sents = sentences(text)
        lens = [words(s) for s in sents]
        all_sents += [(line_id, s, n) for s, n in zip(sents, lens)]
        tag = f"{line_id} ({voice})"

        for s, n in zip(sents, lens):
            if n <= 2:
                problems.append(f"{tag}: one- or two-word sentence: \"{s}\"")
            if s.startswith(WEAK_STARTS):
                notes.append(f"{tag}: generic transition at the start: \"{s[:50]}\"")
        starts = [s.split()[0].strip(",").lower() for s in sents if s.split()]
        for w in set(starts):
            if starts.count(w) > 2:
                problems.append(f"{tag}: {starts.count(w)} sentences start with \"{w}\"")
        if len(lens) >= 3 and not (min(lens) < 15 and max(lens) > 25):
            notes.append(f"{tag}: paragraph lacks both a sentence under 15 words and one over 25 ({lens})")
        if "—" in text or " - " in text or "--" in text:
            notes.append(f"{tag}: em-dash (minimize)")
        if "..." in text or "…" in text:
            problems.append(f"{tag}: ellipsis")
        if re.search(r"[0-9$%&]", text):
            problems.append(f"{tag}: number or symbol not written out for the voice: \"{text[:60]}\"")

    text = " ".join(l[2] for l in lines)
    for kind, phrases in BANNED.items():
        for p in phrases:
            n = len(re.findall(r"\b" + re.escape(p) + r"\b", text, re.I))
            if n:
                problems.append(f"{kind}: \"{p}\" x{n}")

    # Runs of more than three consecutive sentences within 5 words of each other.
    lens = [n for _, _, n in all_sents]
    run_start = 0
    for i in range(1, len(lens) + 1):
        if i == len(lens) or max(lens[run_start:i + 1]) - min(lens[run_start:i + 1]) > 5:
            if i - run_start > 3:
                ids = sorted({all_sents[k][0] for k in range(run_start, i)})
                notes.append(f"{i - run_start} similar-length sentences in a row ({', '.join(ids)})")
            run_start = i

    questions = [(lid, s) for lid, s, _ in all_sents if s.endswith("?")]
    generic = sum(len(re.findall(r"\b" + v + r"\b", text, re.I)) for v in GENERIC_VERBS)
    outside = sum(1 for n in lens if n < 10 or n > 30)

    print(f"Sentences: {len(lens)}, {min(lens)} to {max(lens)} words, average {st.mean(lens):.1f}, "
          f"variation {st.pstdev(lens) / st.mean(lens):.2f}")
    print(f"Outside the 10-30 word range: {outside} of {len(lens)}")
    print(f"Generic verbs (was/were/had/made/got/went/said): {generic}")
    print(f"Questions: {len(questions)} (rhetorical questions are banned; guess-the-number questions "
          f"that the video answers are the open exception)")
    for lid, s in questions:
        print(f"    {lid}: {s}")
    print(f"\nMUST FIX ({len(problems)}):" if problems else "\nMUST FIX: none")
    for p in problems:
        print(f"  - {p}")
    print(f"\nREVIEW ({len(notes)}):" if notes else "\nREVIEW: none")
    for n in notes:
        print(f"  - {n}")


if __name__ == "__main__":
    main(sys.argv[1])
