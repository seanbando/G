// Our cast as lit flat sprites in the 3D world. Each frame every character asks for a drawing (a key + a draw call);
// the pool keeps one canvas per distinct drawing, so soldiers marching in step share canvases (7 head shapes x 4
// outfits). Characters are yaw-only billboards shaded by cardShade() (scene tint, bright floor, side gradient toward
// the sun, painted crescent in the drawing); standing ones get a soft multiply contact blob. Effects are unlit cards.
// Cards, effects and blobs live on the NOINK layer so the world ink pass never outlines their quads.
import * as THREE from "three";
import {
  Pen, bodyFront, bodySide, swingKid, soldier, townsfolk, OFFICER, KID, PARENT, fxNote, fxBurst, fxSplash, fxStars, fxCreak, fxRing, fxBlob, fxShadow, fxContact, fxPlank, fxDrum,
  Outfit, Expr, FrontOpts, SideOpts, SKINS, INK,
} from "./toon";
import {
  FPS, D0, FILES, ROW_GAP, COUNT, PARK, SHOTS, SNAP, DROP0, DROP1, DROP_H, V3, front, marchPhase, stomp, deckY, dropW, dropU, shapeZ,
  smooth, clamp01, BridgeState, OWNER, SUMMIT, HEAPS, TABLE, Scene, growAt,
} from "./story";
import { heapH } from "./money";
import { LIGHTS } from "./lights";
import { NOINK } from "./ink";
import { cardShade, blobMaterial, CARD_K } from "./cardshade";

// ---------------- canvas pool ----------------
type Entry = { cv: HTMLCanvasElement; tex: THREE.CanvasTexture; w: number; h: number };
export type Req = { key: string; w: number; h: number; k: number; draw: (p: Pen) => void; tex?: THREE.CanvasTexture };
const makeEntry = (w: number, h: number): Entry => {
  const cv = document.createElement("canvas");
  cv.width = w; cv.height = h;
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  return { cv, tex, w, h };
};
export class Pool {
  private live = new Map<string, Entry>();
  private free: Entry[] = [];
  private reqs: Req[] = [];
  req(key: string, w: number, h: number, k: number, draw: (p: Pen) => void) {
    const r: Req = { key: `${w}x${h}|${key}`, w, h, k, draw };
    this.reqs.push(r);
    return r;
  }
  flush() {
    const want = new Map<string, Req[]>();
    for (const r of this.reqs) { const l = want.get(r.key); if (l) l.push(r); else want.set(r.key, [r]); }
    for (const [key, e] of this.live) if (!want.has(key)) { this.live.delete(key); this.free.push(e); }
    for (const [key, rs] of want) {
      let e = this.live.get(key);
      if (!e) {
        const r = rs[0], i = this.free.findIndex((x) => x.w === r.w && x.h === r.h);
        e = i >= 0 ? this.free.splice(i, 1)[0] : makeEntry(r.w, r.h);
        const g = e.cv.getContext("2d")!;
        g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, e.w, e.h); g.setTransform(r.k, 0, 0, r.k, 0, 0);
        r.draw(new Pen(g));
        e.tex.needsUpdate = true;
        this.live.set(key, e);
      }
      for (const r of rs) r.tex = e.tex;
    }
    this.reqs = [];
  }
}

// ---------------- sprite meshes ----------------
const blank = (() => { const c = document.createElement("canvas"); c.width = c.height = 2; return new THREE.CanvasTexture(c); })();
export const SU = 0.00216; // metres per design unit: 1000 units = 2.16 m
export const SU_SWING = 2.3 / 1830; // swing canvas: rope of 1830 units = 2.3 m
const BODY = (() => { const g = new THREE.PlaneGeometry(600 * SU, 1000 * SU); g.translate(0, (975 - 500) * SU, 0); return g; })();
const CARD = new THREE.PlaneGeometry(1, 1);
/** world roots that hold actors (to find the scene's sun when world.ts does not pass it) */
const ROOTS = new Set<THREE.Object3D>();

/** lit flat character: cardShade() material, receives shadows (dims to the bright floor only), casts its silhouette
 *  when world.ts says so (golden). Drawn after the contact blobs (renderOrder 1). */
export class Actor {
  mesh: THREE.Mesh; mat: THREE.MeshLambertMaterial; dmat: THREE.MeshDepthMaterial; r: Req | null = null;
  constructor(parent: THREE.Object3D, geo: THREE.BufferGeometry = BODY) {
    this.mat = cardShade(new THREE.MeshLambertMaterial({ map: blank, alphaTest: 0.5, side: THREE.DoubleSide }));
    this.mat.alphaToCoverage = false; // A2C + MSAA left 1 px sky-depth seams on blurred far cards (POST)
    this.dmat = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: blank, alphaTest: 0.5, side: THREE.DoubleSide });
    this.mesh = new THREE.Mesh(geo, this.mat);
    this.mesh.customDepthMaterial = this.dmat;
    // rim width is in output pixels: tell the card shader the render height (1920 = 1080 x 1920 frame)
    this.mesh.onBeforeRender = (r) => { const rt = r.getRenderTarget(); CARD_K.uPx.value = (rt ? rt.height : r.domElement.height) / 1920; };
    this.mesh.castShadow = false; this.mesh.receiveShadow = true; this.mesh.visible = false;
    this.mesh.rotation.order = "YXZ"; this.mesh.renderOrder = 1; this.mesh.layers.set(NOINK);
    parent.add(this.mesh);
    ROOTS.add(parent);
  }
  bind() { const t = this.r?.tex; if (t) { this.mat.map = t; this.dmat.map = t; } }
}
/** unlit effect card: hard cut-out (ink drawings), soft see-through (dust, mist) or a multiply ground blob */
export class Fx {
  mesh: THREE.Mesh; mat: THREE.MeshBasicMaterial; soft: THREE.MeshBasicMaterial; blob: THREE.MeshBasicMaterial; r: Req | null = null;
  constructor(parent: THREE.Object3D) {
    this.mat = new THREE.MeshBasicMaterial({ map: blank, alphaTest: 0.5, side: THREE.DoubleSide });
    this.mat.alphaToCoverage = false; // A2C + MSAA left 1 px sky-depth seams on blurred far cards (POST)
    this.soft = new THREE.MeshBasicMaterial({ map: blank, transparent: true, depthWrite: false, side: THREE.DoubleSide });
    this.blob = blobMaterial(blank);
    this.mesh = new THREE.Mesh(CARD, this.mat);
    this.mesh.visible = false; this.mesh.layers.set(NOINK);
    parent.add(this.mesh);
  }
  use(soft: boolean) { this.mesh.material = soft ? this.soft : this.mat; }
  bind() {
    const t = this.r?.tex;
    if (!t) return;
    if (this.r!.key.includes("|blob|")) {
      // no mipmaps: at grazing views the mip chain averages the blob with its white surround and it fades out
      if (t.generateMipmaps) { t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; t.needsUpdate = true; }
      this.blob.map = t; this.mesh.material = this.blob; this.mesh.renderOrder = 0.5;
    }
    else { this.mat.map = t; this.soft.map = t; this.mesh.renderOrder = 0; }
  }
}

// ---------------- placements ----------------
export type Place = {
  key: string; draw: (p: Pen) => void; x: number; y: number; z: number;
  scale?: number; mirror?: boolean; yaw?: number; geo?: "body" | "swing"; roll?: number; size?: [number, number, number];
};
export type FxPlace = { key: string; cw: number; ch: number; draw: (p: Pen) => void; x: number; y: number; z: number; w: number; h: number; flat?: boolean; rot?: number; soft?: boolean };
/** sun = world direction TOWARD the sun (optional: when absent the scene's shadow-casting light is used) */
export type CamInfo = { pos: THREE.Vector3; right: THREE.Vector3; sun?: THREE.Vector3 };

const hh = (i: number, s = 0) => { const v = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return v - Math.floor(v); };
const q = (v: number, n = 120) => Math.round(v * n) / n;
const SOLDIER = [0, 1, 2, 3].map((v) => soldier(v));
const BARE = [0, 1, 2, 3].map((v) => soldier(v, { hat: null }));
const FOLK = [0, 1, 2, 3, 4, 5].map((v) => townsfolk(v));
const vOf = (i: number) => (i * 7 + (i >> 2)) % 4;
/** head-shape seed: 7 shapes, so marching soldiers in step still share canvases */
const seedOf = (i: number) => ((i * 5 + 3) % 7) + 1;
/** drawing resolution by distance: [canvas w, h, scale from the 600 x 1000 design]; sized for the 1440 x 2560 final */
const tier = (d: number): [number, number, number] =>
  d < 3.2 ? [1800, 3000, 3.0] : d < 6.5 ? [1080, 1800, 1.8] : d < 16 ? [480, 800, 0.8] : [240, 400, 0.4];

// ---------------- light ----------------
const SUN = new THREE.Vector3(0.5, 0.75, -0.4).normalize();
const tmp = new THREE.Vector3();
let LNAME: "day" | "golden" = "day";
const sunOf = (root: THREE.Object3D) => {
  let s: THREE.DirectionalLight | null = null;
  root.traverse((o) => { if (!s && o instanceof THREE.DirectionalLight && o.castShadow) s = o; });
  return s as THREE.DirectionalLight | null;
};
/** the sun of the world that is calling: the attached root whose sun target sits on this camera's view axis */
const findSun = (cam: CamInfo, out: THREE.Vector3) => {
  if (cam.sun) return out.copy(cam.sun).normalize();
  let best: THREE.DirectionalLight | null = null, err = Infinity;
  for (const r of ROOTS) {
    if (!r.parent) continue;
    const s = sunOf(r);
    if (!s) continue;
    const d = tmp.copy(s.target.position).sub(cam.pos), e = Math.abs(d.dot(cam.right)) / (d.length() || 1);
    if (e < err) { err = e; best = s; }
  }
  return best ? out.copy(best.position).sub(best.target.position).normalize() : out;
};
/** canvas angle the sun comes FROM on an upright card facing the camera, in 45-degree steps (small texture cache) */
const light2D = (cam: CamInfo, mirror: boolean) => {
  const sx = SUN.dot(cam.right) * (mirror ? -1 : 1), sy = -SUN.y;
  return Math.round(Math.atan2(sy, sx) / (Math.PI / 4)) * (Math.PI / 4);
};

/** front / side view and mirroring for someone at (x, z) walking along (dx, dz); fs = foreshortening of the walk */
const viewOf = (cam: CamInfo, x: number, z: number, dx: number, dz: number) => {
  const tx = cam.pos.x - x, tz = cam.pos.z - z, tl = Math.hypot(tx, tz) || 1;
  const c = (tx * dx + tz * dz) / tl;
  return { side: c < 0.57, mirror: dx * cam.right.x + dz * cam.right.z < 0, fs: Math.round(Math.sqrt(Math.max(0, 1 - c * c)) * 20) / 20 };
};

// ---------------- life: blinks and reaction timing ----------------
/** reference expression and action changes land 0-3 f before the word onset */
const LEAD = 2 / FPS;
/** eyelid 0 open .. 1 shut. Reference: gaps 0.5-2.3 s, 4-frame blink half / shut / shut / half, plus a blink across
 *  every expression swap (the shut frames hide the swap) */
const LID = [0.5, 1, 1, 0.5];
const SWAPS: Record<number, number[]> = { 4: [16.17, 17.3], 5: [19.48, 20.6], 6: [21.9, 23.7], 7: [29.4, 30.6], 8: [SNAP] };
const lidAt = (t: number, i: number, swaps: number[] = []) => {
  const f = Math.round(t * FPS);
  for (const ts of swaps) { const k = f - Math.round((ts - LEAD) * FPS) + 1; if (k >= 0 && k < 4) return LID[k]; }
  let s = Math.round(-60 * hh(i, 9));
  for (let n = 0; s <= f && n < 400; n++) {
    const k = f - s;
    if (k >= 0 && k < 4) return LID[k];
    s += Math.round(15 + 54 * hh(i * 31 + n, 13)); // next blink 0.5-2.3 s later
  }
  return 0;
};
const fkey = (o: object) => JSON.stringify(o, (_k, v) => (typeof v === "number" ? q(v) : v));

type Who = { i: number; o: Outfit; okey: string };
/** one character drawing in the 600 x 1000 design space, sized by distance, lit from the scene's sun */
const person = (cam: CamInfo, who: Who, x: number, y: number, z: number, view: { side: boolean; mirror: boolean }, fo: FrontOpts, so: SideOpts, scale = 1): Place & { tierKey: string } => {
  const d = cam.pos.distanceTo(tmp.set(x, y + 1.2, z)) / scale;
  const [w, h, k] = tier(d);
  const mirror = view.side && view.mirror, light = light2D(cam, mirror), seed = seedOf(who.i);
  const f2: FrontOpts = { ...fo, light, seed }, s2: SideOpts = { ...so, light, seed };
  const key = view.side ? `S|${who.okey}|${fkey(s2)}` : `F|${who.okey}|${fkey(f2)}`;
  return {
    key, x, y, z, scale, mirror, tierKey: `${w}`,
    draw: (p) => (view.side ? bodySide(p, who.o, s2) : bodyFront(p, who.o, f2)),
    size: [w, h, k],
  };
};

/** ground shadow under a standing / sitting card (review rounds 2-4), multiply, blue-violet: a TIGHT contact pool right under
 *  the feet (~.5 on screen at the core) so nobody floats, plus by day (cards cast no real shadow) a lighter soft tail
 *  stretched AWAY from the sun, length ~1.6 m / tan(sun elevation), capped. Golden: world.ts casts real card shadows. */
const CONTACT: Record<"day" | "golden", [number, number, number]> = { day: [0.2, 0.21, 0.33], golden: [0.24, 0.2, 0.33] };
const TAIL: [number, number, number] = [0.42, 0.44, 0.62];
const toSrgb = (v: number) => { const c = clamp01(v); return c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055; };
const hexOf = (c: [number, number, number], k: number) => "#" + c.map((v) => Math.round(255 * toSrgb(1 - (1 - v) * k)).toString(16).padStart(2, "0")).join("");
const blob = (out: Stage, x: number, y: number, z: number, sc = 1, k = 1) => {
  const hl = Math.hypot(SUN.x, SUN.z) || 1, ox = -SUN.x / hl, oz = -SUN.z / hl, rot = Math.atan2(-ox, -oz);
  if (LNAME === "day") {
    const el = Math.asin(Math.min(0.99, Math.max(0.1, SUN.y)));
    const len = Math.min(2.4, Math.max(0.5, 1.6 / Math.tan(el))) * sc, h = len + 0.55 * sc, c = 0.3 * h; // feet at v = .2 of the card
    const tc = hexOf(TAIL, k);
    out.fx.push({ key: `blob|shadow|${tc}`, cw: 128, ch: 256, draw: (p) => fxShadow(p, tc), x: x + ox * c, y: y + 0.018, z: z + oz * c,
      w: 0.72 * sc, h, flat: true, rot });
  }
  const cc = hexOf(CONTACT[LNAME], k);
  out.fx.push({ key: `blob|contact|${cc}`, cw: 128, ch: 128, draw: (p) => fxContact(p, cc), x: x + ox * 0.03 * sc, y: y + 0.022, z: z + oz * 0.03 * sc,
    w: 0.52 * sc, h: 0.4 * sc, flat: true, rot });
};

// ---------------- the $1 cast by shot ----------------
export type Stage = { places: Place[]; fx: FxPlace[] };
/** the dollar's owner: mustard jacket, money-green cap; the richest person: dark suit, top hat (a generic character) */
const OWNER_O: Outfit = { jacket: "#e0a02e", pants: "#3b5b9a", boots: "#5a3b2a", hat: "cap", cap: "#2f8a4f", skin: SKINS[1] };
const RICH_O: Outfit = { jacket: "#2b2d3a", pants: "#2b2d3a", boots: INK, hat: "tophat", buttons: "#e8c45a", build: "stout", skin: SKINS[0] };
const after = (t: number, w: number) => t >= w - LEAD;

const owner = (cam: CamInfo, t: number, out: Stage, x: number, y: number, z: number, fo: FrontOpts, beard = 0, scale = 1) => {
  const o = beard > 0 ? { ...OWNER_O, beard: q(beard, 30) } : OWNER_O;
  out.places.push(person(cam, { i: 7, o, okey: beard > 0 ? `own${q(beard, 30)}` : "own" }, x, y, z, { side: false, mirror: false },
    { blink: lidAt(t, 7), ...fo }, {}, scale));
  if (fo.mode !== "sit") blob(out, x, y, z, scale);
};
/** a neighbour standing (waist-deep when they stand inside a heap) */
const folk = (cam: CamInfo, t: number, out: Stage, i: number, x: number, y: number, z: number, expr: Expr, wave?: number) => {
  out.places.push(person(cam, { i: 300 + i, o: FOLK[i % 6], okey: `f${i % 6}` }, x, y, z, { side: false, mirror: false },
    { mode: "stand", expr, blink: lidAt(t, 300 + i), wave }, {}));
};
const billFx = (p: Pen) => {
  p.poly([[6, 6], [234, 6], [234, 104], [6, 104]], "#d9e4c6", 5);
  p.poly([[22, 20], [218, 20], [218, 90], [22, 90]], null, 3);
  p.ell(120, 55, 22, 27, "#3f6a45", 3);
};
/** loose bills tumbling (a deterministic swarm): from point a along velocity v, with gravity, spinning */
const bills = (out: Stage, t: number, n: number, seed: number, a: V3, spread: V3, v: V3, life = 1.6, size = 0.36) => {
  for (let i = 0; i < n; i++) {
    const ph = (t / life + hh(i, seed)) % 1, age = ph * life;
    const x = a[0] + (hh(i, seed + 1) - 0.5) * spread[0] + v[0] * age, y = a[1] + (hh(i, seed + 2) - 0.5) * spread[1] + v[1] * age - 2.2 * age * age;
    const z = a[2] + (hh(i, seed + 3) - 0.5) * spread[2] + v[2] * age + 0.3 * Math.sin(age * 5 + i);
    if (y < D0 + 0.02) continue;
    const fade = Math.min(1, ph * 8, (1 - ph) * 6);
    out.fx.push({ key: "billfx", cw: 240, ch: 110, draw: billFx, x, y, z, w: size * fade, h: size * 0.45 * fade, rot: q(age * 4 + i, 12) });
  }
};

export const stage = (id: number, t: number, _b: BridgeState, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light;
  findSun(cam, SUN);
  const [OX, , OZ] = OWNER, [SX, SY, SZ] = SUMMIT, f = Math.round(t * FPS);
  switch (s.crowd as Scene) {
    case "summit": {
      const golden = s.light === "golden";
      owner(cam, t, out, SX, SY, SZ, { mode: "stand", expr: golden ? "smile_closed" : after(t, 5.2) ? "grin" : "smile", prop: "bill" });
      if (golden) bills(out, t, 14, 40, [SX, SY + 3.5, SZ], [6, 3, 4], [0.3, 0.2, 0.2], 2.6, 0.4);
      break;
    }
    case "table": {
      if (id === 1) break; // the hook is the bill alone
      if (id === 13) owner(cam, t, out, OX, D0, OZ, { mode: "stand", expr: after(t, 48.64) ? "neutral" : "smile_closed", look: after(t, 48.64) ? 0 : 1 });
      else owner(cam, t, out, OX, D0, OZ, { mode: "stand", expr: "smile_closed", facing: -1 });
      break;
    }
    case "wallet":
      owner(cam, t, out, OX, D0, OZ, { mode: "stand", expr: after(t, 14.12) ? "laugh" : after(t, 11.94) ? "grin" : "smile", prop: after(t, 11.94) ? "fatwallet" : "wallet" });
      if (after(t, 11.94)) bills(out, t, 6, 10, [OX + 0.45, D0 + 1.35, OZ - 0.1], [0.2, 0.1, 0.2], [0.3, 1.6, -0.2], 1.1, 0.22);
      break;
    case "house": {
      owner(cam, t, out, -1.6, D0, -55.2, { mode: "stand", expr: after(t, 17.86) ? "shock" : "grin", look: -1 });
      // bills pour out of the windows and the door of the owner's house (front at x = -6)
      for (const [y, z] of [[D0 + 3.6, -48.6], [D0 + 3.6, -53.4], [D0 + 6.4, -48.6], [D0 + 6.4, -53.4], [D0 + 1.4, -51]] as const)
        bills(out, t, 9, Math.round(z * 10 + y), [-5.7, y, z], [0.2, 0.4, 0.9], [2.4, 1.2, 0], 1.3, 0.36);
      break;
    }
    case "street": {
      const st = HEAPS.street, k = 1;
      owner(cam, t, out, -0.8, D0 + Math.max(0, heapH(st, k, -0.8, -50)) - 0.75, -50, { mode: "stand", expr: "laugh", prop: "bill" });
      const spots: [number, number, Expr][] = [[2.6, -47, "shock"], [-3.2, -56, "laugh"], [1.8, -60, "grin"], [-2.4, -66, "shock"], [3.1, -70, "laugh"], [-0.6, -76, "grin"], [2.2, -84, "shock"], [-3.0, -90, "laugh"]];
      spots.forEach(([x, z, e], i) => folk(cam, t, out, i, x, D0 + Math.max(0, heapH(st, k, x, z)) - 0.75, z, e, e === "laugh" ? q(Math.sin(t * 8 + i), 20) : undefined));
      bills(out, t, 30, 77, [0, D0 + 7, -62], [10, 2, 30], [0, -0.5, 0], 2.4, 0.38);
      break;
    }
    case "hill": {
      const hl = HEAPS.hill;
      owner(cam, t, out, hl.x, D0 + hl.H - 0.1, hl.z, { mode: "stand", expr: "laugh", prop: "bill" }, 0, 2.2);
      break;
    }
    case "rich": {
      const rh = HEAPS.rich, hl = HEAPS.hill;
      out.places.push(person(cam, { i: 50, o: RICH_O, okey: "rich" }, rh.x, D0 + rh.H - 0.15, rh.z, { side: false, mirror: false },
        { mode: "stand", expr: f < 832 ? "smile" : "shock", look: f < 832 ? 0 : -1, blink: lidAt(t, 50, [27.3]) }, {}));
      blob(out, rh.x, D0 + rh.H - 0.15, rh.z);
      owner(cam, t, out, hl.x, D0 + hl.H - 0.1, hl.z, { mode: "stand", expr: "laugh", prop: "bill" }, 0, 1.6);
      break;
    }
    case "slow": {
      const g = growAt(f);
      owner(cam, t, out, TABLE[0] + 1.0, D0, TABLE[2] - 0.02, { mode: "sit", expr: g > 0.75 ? "dazed" : "neutral" }, g);
      break;
    }
    case "end":
      owner(cam, t, out, OX, D0, OZ, { mode: "stand", expr: after(t, 67.84) ? "grin" : "smile_closed", prop: "bill" });
      break;
    default: break;
  }
  return out;
};

// ---------------- one-off effects ----------------
export const snapFx = (tau: number, at: V3, out: Stage) => {
  if (tau >= SNAP && tau < SNAP + 0.45) {
    const u = (tau - SNAP) / 0.45;
    out.fx.push({ key: `bigburst${q(u, 30)}`, cw: 500, ch: 500, draw: (p) => fxBurst(p, q(u, 30)), x: at[0], y: at[1] + 0.12, z: at[2] - 0.15, w: 1.5, h: 1.5 });
  }
};
export const splashFx = (tau: number, out: Stage) => {
  const u = (tau - DROP1) / 1.1;
  if (u < 0 || u >= 1) return;
  for (const [x, z, s] of [[-2.9, -24, 1], [2.9, -21, 0.9], [-2.9, -15, 0.85], [2.9, -9, 0.8], [0, -27.5, 1.2], [-2.9, -5, 0.6]] as const)
    out.fx.push({ key: `splash${q(u, 30)}`, cw: 800, ch: 800, draw: (p) => fxSplash(p, q(u, 30)), x, y: 2.6 * s, z, w: 7 * s, h: 7 * s }); // base of the drawing on the water line
};
export const creakFx = (t: number, pts: V3[], out: Stage, size = 0.8) =>
  pts.forEach(([x, y, z], i) => {
    const u = q((t * 1.3 + i * 0.37) % 1, 30);
    out.fx.push({ key: `creak${u}`, cw: 300, ch: 300, draw: (p) => fxCreak(p, u), x, y, z, w: size, h: size, rot: i * 0.6 - 0.6 });
  });
export { FPS };
