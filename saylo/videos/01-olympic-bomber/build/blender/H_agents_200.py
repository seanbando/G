"""Hero (cold open, VO 59.64-63.62, 120 frames): "more than 200 federal agents were working out of this corner of the state".
A warm-metal 200+ counts up and lands on the spoken "two hundred" (0.5 s), then FEDERAL AGENTS settles under it.
  --arg land=0.5
"""
import blender_kit as kit

a = kit.args()
land = kit.f(a.get("land", 0.5, float))
end = a.frames
AMBER = "#E0A040"

kit.setup(world="#05070A")
kit.backdrop("#05070A", center="#1F1A12", distance=14)

gold = kit.metal("#F2CD7E", roughness=0.24, name="Gold")
num = kit.text("200+", font="Anton-Regular", size=2.4, extrude=0.16, bevel=0.03, material=gold, loc=(0, 0, 0.25), name="Figure")
kit.number_count(num, 0, 200, 1, land, fmt="{:,.0f}+", ease="out")
kit.key(num, "scale", [(1, (0.9,) * 3), (land, (1.0,) * 3, "back"), (end, (1.025,) * 3)], ease="out")

rule = kit.rect(0.001, 0.035, AMBER, loc=(0, -0.3, -1.15), name="Rule")
kit.key(rule, "scale", [(land, (1, 1, 1)), (land + 12, (4600, 1, 1))], ease="expo")
cap = kit.text("FEDERAL AGENTS", font="Montserrat-Bold", size=0.38, spacing=1.25, color="#E8E4DA", strength=1.5,
               loc=(0, -0.3, -1.55), name="Label")
kit.fade(cap, [(land + 2, 0.0), (land + 14, 1.0)])
kit.key(cap, "location", [(land + 2, (0, -0.3, -1.65)), (land + 14, (0, -0.3, -1.55))], ease="out")

kit.three_point(target=num, power=1.1, distance=9)
kit.light("AREA", (0, -4, 6), num, power=1500, color="#FFE7C4", size=6, name="Top")
dust = kit.motes(count=40, center=(0, -1.0, 0.4), spread=(14, 16, 7), size=0.012, strength=1.5)
kit.key(dust, "location", [(1, (0, -1.0, 0.2)), (end, (0.4, -1.0, 0.6))], ease="linear")

cam = kit.camera((-1.4, -15.0, 1.0), look_at=(0, 0, 0), lens=55)
kit.key(cam, "location", [(1, (-1.4, -15.0, 1.0)), (end, (0.4, -12.8, 0.3))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (0, 0, -0.45)), (end, (0, 0, -0.6))], ease="in_out")
kit.shake(cam, strength=0.015, speed=40)
kit.depth_of_field(cam, focus=num, fstop=1.4)
kit.post(bloom=0.3, vignette=0.4, grain=0.035)
