#!/usr/bin/env bash
# Set up a Claude Code cloud session (Linux, no GPU) to render the Saylo Blender videos. Run from the repo root:
#   bash saylo/tools/cloud_setup.sh
# Needs network access to PyPI (default) and, for the asset step, api.polyhaven.com + dl.polyhaven.org.
# The Documentary Pro kit zip and the footage come from the creator's Google Drive (see the video's REBUILD.md).
set -e
cd "$(dirname "$0")/../.."

# 1. Blender 5.3 as a Python module (the download site is blocked; PyPI is not), plus OpenCV for stills.py
pip install -q bpy==5.3.0 opencv-python-headless numpy

# 2. A `blender` command backed by that module, so the Documentary Pro runner and `blender -b --python` work
mkdir -p /opt/blender-5.3
cat > /opt/blender-5.3/blender <<'EOF'
#!/usr/bin/env python3
"""Stand-in for the blender executable, backed by the bpy module. Handles the options the Documentary Pro runner
and the Saylo scripts use: -b, --factory-startup, --python-exit-code N, -t N, --python-expr X, -P/--python F, -- args."""
import os, sys, traceback
argv = sys.argv[1:]
if "--" in argv:
    argv = argv[:argv.index("--")]
if argv[:1] == ["--version"]:
    import bpy; print("Blender", bpy.app.version_string); sys.exit(0)
steps, code, threads, blendfile = [], 1, None, None
i = 0
while i < len(argv):
    a = argv[i]
    if a in ("-b", "--background", "--factory-startup", "-noaudio"): pass
    elif a == "--python-exit-code": code = int(argv[i + 1]); i += 1
    elif a in ("-t", "--threads"): threads = int(argv[i + 1]); i += 1
    elif a == "--python-expr": steps.append(("expr", argv[i + 1])); i += 1
    elif a in ("-P", "--python"): steps.append(("file", argv[i + 1])); i += 1
    elif a.endswith(".blend"): blendfile = a
    else: print("blender-shim: ignoring", a, file=sys.stderr)
    i += 1
import bpy
if blendfile: bpy.ops.wm.open_mainfile(filepath=blendfile)
else: bpy.ops.wm.read_factory_settings(use_empty=False)
if threads:
    bpy.context.scene.render.threads_mode = "FIXED"; bpy.context.scene.render.threads = threads
g = {"__name__": "__main__"}
try:
    for kind, x in steps:
        if kind == "expr":
            exec(compile(x, "<expr>", "exec"), g)
        else:
            g["__file__"] = os.path.abspath(x)
            sys.path.insert(0, os.path.dirname(os.path.abspath(x)))
            exec(compile(open(x, encoding="utf-8").read(), x, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
except Exception:
    traceback.print_exc(); sys.exit(code)
EOF
chmod +x /opt/blender-5.3/blender
ln -sf /opt/blender-5.3/blender /usr/local/bin/blender

# 3. Software OpenGL (Mesa llvmpipe) so EEVEE renders without a GPU
DEBIAN_FRONTEND=noninteractive apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libegl1 libegl-mesa0 libgl1-mesa-dri libgles2 mesa-vulkan-drivers libvulkan1 >/dev/null
blender --version

# 4. Free CC0 assets the Retraced sets use (textures, grass, trees, sky), then the tree libraries and the mannequin
if [ "${SKIP_ASSETS:-0}" != "1" ]; then
  python3 saylo/tools/fetch_polyhaven.py textures asphalt_02 blue_metal_plate brick_wall_08 concrete_wall_004 corrugated_iron_02 cracked_concrete forest_ground_04 hangar_concrete_floor
  python3 saylo/tools/fetch_polyhaven.py models grass_medium_01 grass_medium_02 fir_tree_01 pine_tree_01
  python3 - <<'EOF'
import json, os, urllib.request
UA = {"User-Agent": "saylo-kit/1.0"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
u = json.loads(get("https://api.polyhaven.com/files/evening_road_01_puresky"))["hdri"]["2k"]["hdr"]["url"]
p = "_kit/assets/polyhaven/hdri/evening_road_01_puresky.hdr"
os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, "wb").write(get(u)); print("ok sky")
EOF
  blender -b --factory-startup --python saylo/tools/blender/prep_trees.py        # one at a time: 15 GB RAM is tight
  blender -b --factory-startup --python saylo/tools/blender/prep_trees_mid.py
  blender -b --factory-startup --python saylo/tools/blender/make_mannequin.py
fi
echo "cloud setup done"
