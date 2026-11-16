"""Clay diorama: the mountains of far western North Carolina (schematic, not survey-accurate).
Clay ridges on a slab; MURPHY in the west valley, TOPTON to the northeast (they are ~20 miles apart), and the
Nantahala National Forest spreading east of them. Pins land on "Topton and Murphy" (2.26 s), the forest label on
"right on the edge of the Nantahala National Forest" (3.7 s). Night, moonlit clay, amber is the only colour.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import blender_kit as kit
import clay

a = kit.args()
end = a.frames
PINS, FOREST = kit.f(2.26), kit.f(3.7)
kit.setup(world="#050506", view="Standard", bloom=0.3)
kit.backdrop("#050506", center="#161B26", distance=60)
m = clay.mats()

# terrain: subdivided slab displaced by a cloud texture (ridges), with a valley carved along the river line
bpy.ops.mesh.primitive_grid_add(x_subdivisions=220, y_subdivisions=160, size=1, location=(0, 0, 0))
terr = bpy.context.active_object
terr.scale = (24, 16, 1)
bpy.ops.object.transform_apply(scale=True)
tex = bpy.data.textures.new("Ridges", "CLOUDS")
tex.noise_scale, tex.noise_depth, tex.noise_basis = 2.6, 3, "ORIGINAL_PERLIN"
disp = terr.modifiers.new("Disp", "DISPLACE")
disp.texture, disp.strength, disp.mid_level = tex, 4.2, 0.5
sm = terr.modifiers.new("Smooth", "SMOOTH")
sm.factor, sm.iterations = 1.0, 6
kit.assign(terr, m["clay"])
bpy.ops.object.shade_smooth()
clay.box(24.4, 16.4, 1.2, (0, 0, -1.4), m["clay_d"], "Base")

def ground_z(x, y):
    """Height of the displaced terrain under (x, y), via a downward ray."""
    dg = bpy.context.evaluated_depsgraph_get()
    ok, loc, *_ = bpy.context.scene.ray_cast(dg, (x, y, 30), (0, 0, -1))
    return loc.z if ok else 0.0

def pin(x, y, label, t0, side=1):
    z = ground_z(x, y)
    post = clay.cyl(0.04, 1.6, (x, y, z + 0.8), m["amber"], "PinPost")
    head = clay.sphere(0.16, (x, y, z + 1.65), kit.emission(clay.AMBER, 2.0, "PinHead"), "PinHead")
    for ob, zz in ((post, z + 0.8), (head, z + 1.65)):
        kit.key(ob, "location", [(t0 - 6, (x, y, zz + 2.5)), (t0 + 4, (x, y, zz))], ease="expo")
        kit.fade(ob, [(t0 - 6, 0.0), (t0, 1.0)])
    tx = kit.text(label, font="Montserrat-Bold", size=0.7, spacing=1.15, color="#F4F1EA", strength=1.4,
                  align="LEFT" if side > 0 else "RIGHT", loc=(x + 0.3 * side, y, z + 1.95), rot=(70, 0, 0), name=label)
    kit.fade(tx, [(t0 + 2, 0.0), (t0 + 10, 1.0)])
    tx.visible_shadow = False

pin(-6.5, -2.5, "MURPHY", PINS, side=-1)
pin(4.0, 3.0, "TOPTON", PINS + 4, side=1)

# the forest: an amber light washing over the eastern ridges + label
fl = kit.light("SPOT", (7.0, 2.0, 14.0), (7.0, 2.0, 0.0), power=0, color="#E0A040", size=2.0, name="ForestLight")
fl.data.spot_size, fl.data.spot_blend = math.radians(48), 0.6
kit.key(fl.data, "energy", [(FOREST, 0.0), (FOREST + 14, 9000.0)], ease="out")
nf = kit.text("NANTAHALA NATIONAL FOREST", font="Montserrat-Bold", size=0.8, spacing=1.2, color=clay.AMBER, strength=1.4,
              loc=(6.8, 3.6, 4.0), rot=(70, 0, 0), name="ForestLabel")
kit.fade(nf, [(FOREST + 2, 0.0), (FOREST + 12, 1.0)])
nf.visible_shadow = False
clay.night_light(moon=1.4, key=2600)

cam = kit.camera((-4.0, -24.0, 15.0), look_at=(0, 0.5, 0), lens=40)
kit.key(cam, "location", [(1, (-4.0, -24.0, 15.0)), (end, (-1.0, -27.0, 17.5))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (-1.5, 0.0, 0.5)), (end, (0.8, 0.8, 0.8))], ease="in_out")
kit.shake(cam, strength=0.008, speed=40)
kit.depth_of_field(cam, focus=28.0, fstop=1.2)
kit.post(bloom=0.35, vignette=0.65, grain=0.04)
