"""Download Poly Haven assets (CC0) into <repo>/_kit/assets/polyhaven/<id>/ as glTF (models) or PBR maps (textures).

    python saylo/tools/fetch_polyhaven.py models rollershutter_door security_light ...
    python saylo/tools/fetch_polyhaven.py textures asphalt_02 concrete_wall_008 ...   [--res 2k]

Poly Haven assets are CC0 (https://polyhaven.com/license). Each folder gets a SOURCE.txt with the asset page.
"""
import json
import os
import sys
import urllib.request

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(REPO, "_kit", "assets", "polyhaven")
UA = {"User-Agent": "saylo-build/1.0"}
MAPS = ("Diffuse", "nor_gl", "Rough", "AO", "Displacement", "arm")


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def save(url, path):
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = get(url)
    with open(path, "wb") as fh:
        fh.write(data)


def fetch(kind, aid, res):
    files = json.loads(get(f"https://api.polyhaven.com/files/{aid}"))
    d = os.path.join(OUT, aid)
    if kind == "models":
        g = files["gltf"].get(res) or next(iter(files["gltf"].values()))
        gl = g["gltf"]
        save(gl["url"], os.path.join(d, os.path.basename(gl["url"])))
        for rel, inc in gl.get("include", {}).items():
            save(inc["url"], os.path.join(d, rel))
    else:
        for m in MAPS:
            if m in files:
                v = files[m].get(res) or next(iter(files[m].values()))
                f = v.get("jpg") or v.get("png")
                save(f["url"], os.path.join(d, os.path.basename(f["url"])))
    with open(os.path.join(d, "SOURCE.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"https://polyhaven.com/a/{aid}  (CC0)\n")
    print("ok", aid)


if __name__ == "__main__":
    args = sys.argv[1:]
    res = "2k"
    if "--res" in args:
        i = args.index("--res")
        res = args[i + 1]
        del args[i:i + 2]
    kind, ids = args[0], args[1:]
    for aid in ids:
        try:
            fetch(kind, aid, res)
        except Exception as e:  # keep going; report at the end
            print("FAILED", aid, e)
