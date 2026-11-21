"""Find when a phrase is spoken: python3 saylo/tools/words.py <vo-words.json> "phrase one" "phrase two" ..."""
import json, re, sys

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def find(words, phrase, after=0.0):
    key = [norm(x) for x in phrase.split() if norm(x)]
    ws = [norm(w["w"]) for w in words]
    for i in range(len(ws) - len(key) + 1):
        if words[i]["s"] >= after and ws[i:i + len(key)] == key:
            return words[i]["s"], words[i + len(key) - 1]["e"]
    return None

if __name__ == "__main__":
    words = json.load(open(sys.argv[1])); t = 0.0
    for ph in sys.argv[2:]:
        r = find(words, ph, t)
        print(f"{r[0]:8.2f} {r[1]:8.2f}  {ph}" if r else f"    MISSING  {ph}")
        if r: t = r[0]
