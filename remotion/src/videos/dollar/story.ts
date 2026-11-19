// Timeline of the $1 short (shorts/one-dollar/voice/words.json, 69.0 s). The bridge physics below stay only so the
// town's bridge can stand (always intact); the story here is the doubling dollar.
// (bridge-short header follows)
// story physics (column position, march phase, deck bounce, collapse) and the camera grammar measured in the
// reference study: continuous slow push-ins; symmetric ease-in-out moves ~23 f (10 in / 10 out), peak ~15 px/f at 720p;
// big reframes are cuts; impacts are 7-frame kicks that flip sign every frame; no hand-held float.
export const FPS = 30;
export const TOTAL = 2070;
export const D0 = 6.0; // bank top + deck height (m)
export const HALF = 27; // towers at z = +-27, span 54 m
export const FILES = [-1.65, -0.55, 0.55, 1.65];
export const ROW_GAP = 1.3;
export const COUNT = 74;
export const PARK: V3 = [70, D0, -75]; // swing pivot base (x, ground y, z)
export type V3 = [number, number, number];

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;
const lin = (pts: [number, number][], x: number) => {
  if (x <= pts[0][0]) return pts[0][1];
  for (let i = 1; i < pts.length; i++) if (x <= pts[i][0]) {
    const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
    return y0 + ((y1 - y0) * (x - x0)) / (x1 - x0);
  }
  return pts[pts.length - 1][1];
};

// ---------------- story physics (tau = story time in seconds) ----------------
export const front = (tau: number) => 26 - 1.6 * (tau - 4.4); // z of the front row, marching toward -z
export const marchPhase = (tau: number) => ((tau % 1) + 1) % 1; // 1 Hz cycle = 2 steps/s, footfalls at 0 and 0.5
export const SNAP = 34.62, DROP0 = 36.35, DROP1 = 36.95;
export const amp = (tau: number) =>
  lin([[14.85, 0], [17.8, 0.07], [21.4, 0.13], [27.4, 0.26], [33.0, 0.46], [SNAP, 0.55], [SNAP + 0.35, 0.0]], tau);
export const stomp = (tau: number) => lin([[21.4, 1.0], [27.4, 1.35], [33, 1.5]], tau); // "a little harder every step"
export const shapeZ = (z: number) => (Math.abs(z) < HALF ? Math.cos((Math.PI * z) / (2 * HALF)) : 0);
export const dropW = (z: number) => smooth((20 - z) / 26); // 1 on the near half, 0 at the far tower
export const dropU = (tau: number) => (tau < DROP0 ? 0 : Math.min(1, ((tau - DROP0) / (DROP1 - DROP0)) ** 2));
export const DROP_H = 6.6;

export type BridgeState = { bounce: number; drop: number; snap: number; collapsed: boolean };
export const deckY = (z: number, b: BridgeState) => D0 + b.bounce * shapeZ(z) - b.drop * DROP_H * dropW(z);

// ---------------- places (near bank, main street x -6..6 running toward -z) ----------------
/** the owner's kitchen table, out on the street in front of the owner's house (first house on the left of the main street) */
export const TABLE: V3 = [-3.6, D0, -51];
export const TABLE_TOP = 0.78;
export const OWNER: V3 = [-2.55, D0, -51.75];
/** money heaps: centre (x, z), half-extents (ax, az), peak height H, flat = plateau (0) .. peak (1) */
export type HeapDef = { x: number; z: number; ax: number; az: number; H: number; peak: number; seed: number };
export const HEAPS: Record<string, HeapDef> = {
  house: { x: -6.5, z: -51, ax: 5.0, az: 6.5, H: 1.9, peak: 0.6, seed: 1 },
  street: { x: 0, z: -96, ax: 6.4, az: 58, H: 1.35, peak: 0.0, seed: 2 },
  hill: { x: 0, z: -84, ax: 21, az: 21, H: 24, peak: 1, seed: 3 },
  rich: { x: 31, z: -64, ax: 15, az: 15, H: 19, peak: 1, seed: 4 },
  near: { x: 0, z: -132, ax: 190, az: 104, H: 44, peak: 1, seed: 5 },
  far: { x: 0, z: 132, ax: 190, az: 104, H: 44, peak: 1, seed: 6 },
};
export const SUMMIT: V3 = [0, D0 + 44, -132];

// ---------------- shots ----------------
export type Light = "day" | "golden";
/** what the shot shows: which heaps stand (with a growth 0..1), who is there */
export type Scene = "table" | "wallet" | "house" | "street" | "hill" | "rich" | "half" | "full" | "summit" | "snowball" | "slow" | "end";
export type Crowd = Scene;
export type ShotDef = { id: number; a: number; b: number; light: Light; crowd: Scene; tau: (t: number) => number; towns?: boolean };
const id_ = (t: number) => t;
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: 75, light: "day", crowd: "table", tau: id_ },     // hook: one bill, doubling on the table
  { id: 2, a: 75, b: 154, light: "day", crowd: "full", tau: id_ },     // "outgrows all the personal wealth on Earth"
  { id: 3, a: 154, b: 209, light: "day", crowd: "summit", tau: id_ },  // "Guess how many days it takes?"
  { id: 4, a: 209, b: 326, light: "day", crowd: "table", tau: id_ },   // Day zero, kitchen table
  { id: 5, a: 326, b: 458, light: "day", crowd: "wallet", tau: id_ },  // Day ten, a wallet
  { id: 6, a: 458, b: 584, light: "day", crowd: "house", tau: id_ },   // Day twenty, the whole house
  { id: 7, a: 584, b: 717, light: "day", crowd: "street", tau: id_ },  // Day thirty, the street
  { id: 8, a: 717, b: 817, light: "day", crowd: "hill", tau: id_ },    // Day forty, 1.1 trillion
  { id: 9, a: 817, b: 882, light: "day", crowd: "rich", tau: id_ },    // the richest person alive
  { id: 10, a: 882, b: 1150, light: "day", crowd: "half", tau: id_ },  // Day forty-eight: half
  { id: 11, a: 1150, b: 1292, light: "day", crowd: "full", tau: id_ }, // one more doubling, day forty-nine
  { id: 12, a: 1292, b: 1362, light: "golden", crowd: "summit", tau: id_ }, // bigger than everyone
  { id: 13, a: 1362, b: 1527, light: "day", crowd: "table", tau: id_ }, // Luckily / Unluckily
  { id: 14, a: 1527, b: 1604, light: "day", crowd: "snowball", tau: id_ }, // the snowball
  { id: 15, a: 1604, b: 1709, light: "day", crowd: "full", tau: id_ }, // the last day = the 48 before it
  { id: 16, a: 1709, b: 1897, light: "day", crowd: "slow", tau: id_ },  // 350 years at 10 %
  { id: 17, a: 1897, b: 1978, light: "day", crowd: "full", tau: id_ }, // forty-nine days
  { id: 18, a: 1978, b: TOTAL, light: "golden", crowd: "end", tau: id_ }, // or 350 years: keep the dollar
];
/** crossfades (frames) at place/time changes; a white 4-frame flash after the hook */
export const XFADE: Record<number, number> = { 12: 8, 13: 8, 16: 8, 17: 8 };
export const FLASH_AT = 205;

export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
export const layersAt = (f: number): { id: number; alpha: number }[] => {
  for (const s of SHOTS) {
    const x = XFADE[s.id];
    if (x && f >= s.a - x / 2 && f < s.a + x / 2) return [{ id: s.id - 1, alpha: 1 }, { id: s.id, alpha: (f - (s.a - x / 2) + 1) / (x + 1) }];
  }
  return [{ id: shotAt(f).id, alpha: 1 }];
};

/** the town's bridge never moves in this story */
export const bridgeState = (_id: number, _t: number): BridgeState => ({ bounce: 0, drop: 0, snap: 0, collapsed: false });

// ---------------- the money (pure functions of shot + frame) ----------------
/** bills on the table in the hook: 1, 2, 4 ... doubling every 6 frames from "doubling" (f 32) */
export const tableBills = (id: number, f: number) => {
  if (id === 1) return f < 30 ? 1 : Math.min(256, 2 ** Math.floor((f - 30) / 5 + 1));
  if (id === 4 || id === 13 || id === 18) return 1;
  if (id === 16) return 1 + Math.floor(3 * clamp01((f - 1730) / 160)); // 10 % a year: a pile that barely grows
  return 0;
};
/** heap growth 0..1 per shot (heaps not listed are hidden) */
export const heapsAt = (id: number, f: number): Record<string, number> => {
  const rise = (f0: number, n: number) => easeOut((f - f0) / n);
  switch (id) {
    case 6: return { house: 0.55 + 0.45 * rise(458, 40) };
    case 7: return { house: 1, street: 0.6 + 0.4 * rise(584, 50) };
    case 8: return { street: 1, hill: 0.7 + 0.3 * rise(717, 45) };
    case 9: return { street: 1, hill: 1, rich: 1 };
    case 10: return { near: 0.94 + 0.06 * rise(882, 60) };
    case 11: return { near: 1, far: f < 1150 ? 0 : rise(1152, 38) };
    case 2: case 3: case 12: case 14: case 15: case 17: return { near: 1, far: 1 };
    default: return {};
  }
};
/** the money snowball: rolls down the near mountain toward the river, radius doubling as it goes */
export const SNOW0 = 1529, SNOW1 = 1604;
export const snowball = (f: number) => {
  const u = clamp01((f - SNOW0) / (SNOW1 - SNOW0));
  const z = -112 + 66 * u ** 1.6;
  return { x: 6, z, r: 0.6 * 2 ** (u * 4.2), roll: (66 * u ** 1.6) / 2 };
};
/** 350 years: the sapling grows into a tree and the owner grows a beard */
export const growAt = (f: number) => clamp01((f - 1722) / 150);

// ---------------- camera ----------------
// Grammar (motion.md): symmetric smootherstep glides of 18-40 f, big reframes are cuts, every hold creeps
// 0.15-0.35 %/f (0.6 %/f on punch words), rolls of 4-5 deg, 7-frame flip kicks on impacts, no hand-held float.
export type Cam = { pos: V3; look: V3; fov: number; roll: number };
type Shot = Partial<Cam> & { pos: V3; look: V3 };
type Key = { f: number; dur?: number; cut?: boolean; s: (f: number) => Shot };
export const glide = (u: number) => { const x = clamp01(u); return x * x * x * (x * (6 * x - 15) + 10); };
const mix = (a: Cam, b: Cam, k: number): Cam => ({
  pos: a.pos.map((v, i) => v + (b.pos[i] - v) * k) as V3, look: a.look.map((v, i) => v + (b.look[i] - v) * k) as V3,
  fov: a.fov + (b.fov - a.fov) * k, roll: a.roll + (b.roll - a.roll) * k,
});
const full = (c: Shot): Cam => ({ fov: 40, roll: 0, ...c });
const run = (keys: Key[], f: number) => {
  let cur = full(keys[0].s(f));
  for (let i = 1; i < keys.length; i++) {
    const k = keys[i];
    if (f < k.f) break;
    cur = k.cut ? full(k.s(f)) : mix(cur, full(k.s(f)), glide((f - k.f) / (k.dur ?? 24)));
  }
  return cur;
};
const T = (f: number) => f / FPS;
const pushK = (f: number, f0: number, rate: number, punch = 0, n = 35) => {
  const x = Math.max(0, f - f0);
  let s = rate * x;
  if (punch > rate) for (let i = 0; i < Math.min(x, n); i++) s += (punch - rate) * Math.max(0, Math.min(1, (i + 0.5) / 8, (n - i - 0.5) / 8));
  return Math.exp(-s);
};
const dolly = (pos: V3, look: V3, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos: [look[0] + (pos[0] - look[0]) * k, look[1] + (pos[1] - look[1]) * k, look[2] + (pos[2] - look[2]) * k], look, ...rest });
const zoom = (pos: V3, look: V3, fov: number, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos, look, fov: (360 / Math.PI) * Math.atan(Math.tan((fov * Math.PI) / 360) * k), ...rest });
const rolled = (s: (f: number) => Shot, roll: number) => (f: number): Shot => ({ ...s(f), roll });

const [TX, , TZ] = TABLE, TY = D0 + TABLE_TOP, [OX, , OZ] = OWNER, [SX, SY, SZ] = SUMMIT;
// shot 1: close on the bill, pushing in; the stack climbs as it doubles; lift on "outgrows"
const S1a = (f: number) => dolly([TX + 1.5, TY + 0.55, TZ - 1.35], [TX, TY + 0.05, TZ], pushK(f, 0, 0.003), { fov: 36 });
const S1b = (f: number) => dolly([TX + 1.9, TY + 1.0, TZ - 1.9], [TX, TY + 0.35, TZ], pushK(f, 30, 0.0025), { fov: 38, roll: 0.04 });
// shots 2, 17: the aerial over both banks (far bank near the lens, the near-bank mountain behind)
const AER = (f: number, f0: number, rate: number, punch = 0) => zoom([38, 150, 250], [0, 12, -40], 46, pushK(f, f0, rate, punch));
// shot 3 / 12: the owner on the summit
const S3a = (f: number) => dolly([SX + 2.4, SY + 1.45, SZ + 5.2], [SX, SY + 1.15, SZ], pushK(f, 154, 0.003, 0.006, 30), { fov: 38 });
const S12a = (f: number) => dolly([SX - 1.0, SY + 0.9, SZ + 9.5], [SX, SY + 1.6, SZ], pushK(f, 1288, 0.0025), { fov: 40, roll: -0.04 });
// shot 4: MS of the owner at the table (house behind) -> close on the bill on "One crisp dollar bill"
const S4a = (f: number) => dolly([OX + 4.6, D0 + 1.55, OZ - 2.6], [OX - 0.4, D0 + 1.2, OZ + 0.1], pushK(f, 205, 0.0025), { fov: 40 });
const S4b = (f: number) => dolly([TX + 1.1, TY + 0.5, TZ - 1.05], [TX, TY + 0.03, TZ], pushK(f, 245, 0.0025), { fov: 34, roll: -0.035 });
// shot 5: the wallet; closer on "Fits in a wallet"
const S5a = (f: number) => dolly([OX + 3.6, D0 + 1.6, OZ - 2.4], [OX, D0 + 1.3, OZ], pushK(f, 326, 0.0025), { fov: 40 });
const S5b = (f: number) => dolly([OX + 1.9, D0 + 1.45, OZ - 1.2], [OX + 0.15, D0 + 1.25, OZ], pushK(f, 422, 0.002, 0.006, 30), { fov: 36, roll: 0.04 });
// shot 6: the house bursting with money; the owner in front
const S6a = (f: number) => dolly([4.8, D0 + 2.4, -62], [-4.6, D0 + 2.9, -50.5], pushK(f, 456, 0.0025), { fov: 46 });
const S6b = (f: number) => dolly([4.6, D0 + 1.9, -57], [-4.6, D0 + 2.6, -50.5], pushK(f, 534, 0.002, 0.006, 30), { fov: 42, roll: -0.04 });
// shot 7: low in the street, waist-deep neighbours; up over the street on "The street is full of money"
const S7a = (f: number) => dolly([2.2, D0 + 3.3, -39.5], [-0.6, D0 + 2.3, -58], pushK(f, 582, 0.0025), { fov: 42 });
const S7b = (f: number) => dolly([7, D0 + 14, -34], [0, D0 + 1, -86], pushK(f, 657, 0.002), { fov: 44, roll: 0.03 });
// shot 8: the money hill over the rooftops (low, from the quay)
const S8a = (f: number) => zoom([9, D0 + 3.2, -33.2], [0, D0 + 13, -84], 48, pushK(f, 715, 0.0025));
const S8b = (f: number) => zoom([9, D0 + 3.2, -33.2], [0, D0 + 15.5, -84], 42, pushK(f, 750, 0.0015, 0.006, 35));
// shot 9: the richest person on his (smaller) pile, our hill towering beside him
const RH = HEAPS.rich, RT: V3 = [RH.x, D0 + RH.H, RH.z];
const S9a = (f: number) => dolly([RT[0] + 4.6, RT[1] + 2.6, RT[2] + 5.0], [RT[0] - 2.2, RT[1] + 0.6, RT[2] - 2.4], pushK(f, 815, 0.003), { fov: 46, roll: 0.035 });
// shot 10: aerial, near bank buried, far bank untouched; tilt across to the far bank on "Just over half"
const S10a = (f: number) => zoom([30, 175, 205], [0, 14, -70], 46, pushK(f, 880, 0.002));
const S10b = (f: number) => zoom([30, 175, 205], [0, 4, 30], 50, pushK(f, 981, 0.0018));
// shot 11: the far bank fills; pull back on "Five hundred sixty-three trillion"
const S11a = (f: number) => zoom([30, 175, 205], [0, 6, 40], 50, pushK(f, 1148, 0.0015, 0.005, 30));
const S11b = (f: number) => zoom([60, 260, 330], [0, 12, -20], 46, pushK(f, 1226, 0.002));
// shot 13: back at the table, one bill; closer on "Unluckily"
const S13a = (f: number) => dolly([OX + 3.4, D0 + 1.25, OZ - 2.4], [OX - 0.5, D0 + 1.0, OZ + 0.2], pushK(f, 1358, 0.0025), { fov: 40 });
const S13b = (f: number) => dolly([OX + 1.7, D0 + 1.2, OZ - 1.2], [OX - 0.1, D0 + 1.05, OZ], pushK(f, 1457, 0.002, 0.006, 30), { fov: 36, roll: -0.04 });
// shot 14: the money snowball rolling down the mountain (side view, following)
const S14a = (f: number) => { const s = snowball(f); return { pos: [s.x + 46 + 3 * s.r, D0 + 62 + 1.5 * s.r, s.z + 14] as V3, look: [s.x, D0 + 36, s.z + 6] as V3, fov: 44 }; };
// shot 15: the two equal halves, gliding from the near (48 days) to the far (the last day)
const S15a = (f: number) => zoom([40, 240, 310], [0, 20, -125], 48, pushK(f, 1600, 0.0015));
const S15b = (f: number) => zoom([40, 240, 310], [0, 10, 95], 48, pushK(f, 1660, 0.0015));
// shot 16: 350 years at the table: the tree grows, the beard grows; closer on "three hundred fifty years"
const SIT: V3 = [TX - 1.0, D0, TZ + 0.02];
const S16a = (f: number) => dolly([TX + 4.6, D0 + 2.3, TZ - 3.6], [TX - 1.4, D0 + 2.0, TZ + 1.0], pushK(f, 1705, 0.002), { fov: 46 });
const S16b = (f: number) => dolly([SIT[0] + 2.6, D0 + 1.75, SIT[2] - 1.5], [SIT[0], D0 + 1.0, SIT[2]], pushK(f, 1799, 0.002, 0.006, 30), { fov: 40, roll: 0.04 });
// shot 18: golden, the owner keeps the dollar; crane out over the street
const S18a = (f: number) => dolly([OX + 2.4, D0 + 1.45, OZ - 1.9], [OX, D0 + 1.3, OZ], pushK(f, 1976, 0.0025), { fov: 38 });
const S18b = (f: number) => { const a = S18a(2020), u = glide((f - 2020) / 50); return { pos: [a.pos[0] + 3 * u, a.pos[1] + 6 * u, a.pos[2] - 5 * u] as V3, look: [a.look[0], a.look[1] - 0.3 * u, a.look[2]] as V3, fov: 38 + 4 * u, roll: 0 }; };

const CAMS: Record<number, Key[]> = {
  1: [{ f: 0, s: S1a }, { f: 30, dur: 40, s: S1b }],
  2: [{ f: 75, s: (f) => AER(f, 75, 0.0025, 0.005) }],
  3: [{ f: 154, s: S3a }],
  4: [{ f: 205, s: S4a }, { f: 245, cut: true, s: S4b }],
  5: [{ f: 326, s: S5a }, { f: 422, cut: true, s: S5b }],
  6: [{ f: 456, s: S6a }, { f: 534, dur: 30, s: S6b }],
  7: [{ f: 582, s: S7a }, { f: 657, cut: true, s: S7b }],
  8: [{ f: 715, s: S8a }, { f: 750, dur: 30, s: S8b }],
  9: [{ f: 815, s: S9a }],
  10: [{ f: 880, s: S10a }, { f: 981, dur: 40, s: S10b }],
  11: [{ f: 1148, s: S11a }, { f: 1226, cut: true, s: S11b }],
  12: [{ f: 1288, s: S12a }],
  13: [{ f: 1358, s: S13a }, { f: 1457, cut: true, s: S13b }],
  14: [{ f: 1527, s: S14a }],
  15: [{ f: 1600, s: S15a }, { f: 1660, dur: 40, s: S15b }],
  16: [{ f: 1705, s: S16a }, { f: 1799, cut: true, s: S16b }],
  17: [{ f: 1893, s: (f) => AER(f, 1893, 0.002) }],
  18: [{ f: 1976, s: S18a }, { f: 2020, cut: true, s: S18b }],
};
void rolled;

// impact kicks: the image offset flips sign every frame and decays over 7 f
const KICKS: [number, number][] = [[717 / FPS, 0.6], [1190 / FPS, 1.5], [1228 / FPS, 0.6]];
export const kickAt = (t: number) => {
  let a = 0;
  for (const [t0, g] of KICKS) {
    const n = Math.floor((t - t0) * FPS + 1e-6);
    if (n >= 0 && n < 7) a += g * (n % 2 ? -1 : 1) * (1 - n / 7) ** 1.5;
  }
  return a;
};
export const camAt = (id: number, f: number): Cam => {
  const c = run(CAMS[id], f), a = kickAt(T(f));
  if (!a) return c;
  const d: V3 = [c.look[0] - c.pos[0], c.look[1] - c.pos[1], c.look[2] - c.pos[2]];
  const L = Math.hypot(...d), h = Math.hypot(d[0], d[2]) || 1;
  const m = (3 / 640) * Math.tan((c.fov * Math.PI) / 360) * L * a;
  return { ...c, look: [c.look[0] - (d[2] / h) * m, c.look[1] + 0.6 * m, c.look[2] + (d[0] / h) * m], roll: c.roll + a * 0.004 };
};
export const keyEnd = (id: number, f: number) => {
  let e = 0;
  for (const k of CAMS[id]) if (f >= k.f) e = k.f + (k.cut ? 0 : k.dur ?? 24);
  return Math.max(f, e);
};

// ---------------- lens: depth of field + foreground framing ----------------
export type Dof = { f: number; dur?: number; cInf: number; focus?: (f: number) => V3 };
const ownerEyes = (): V3 => [OX, D0 + 1.62, OZ];
const sitEyes = (): V3 => [TX - 1.0, D0 + 1.25, TZ];
const bill = (): V3 => [TX, TY + 0.02, TZ];
export const DOF: Dof[] = [
  { f: 0, cInf: 15, focus: bill },          // hook CU of the bill: the house far behind is soft
  { f: 30, dur: 40, cInf: 12, focus: bill },
  { f: 75, cInf: 0 },                        // aerial
  { f: 154, cInf: 7 },                       // summit MS, focus = look
  { f: 209, cInf: 10, focus: ownerEyes },    // owner MS
  { f: 245, cInf: 15, focus: bill },         // bill CU
  { f: 326, cInf: 11, focus: ownerEyes },    // wallet MS
  { f: 422, cInf: 13, focus: ownerEyes },    // closer
  { f: 458, cInf: 0 },                       // house, street, hill, rich, aerials: readable wides
  { f: 817, cInf: 6 },                       // rich man MS (mild, the hill must read)
  { f: 882, cInf: 0 },
  { f: 1292, cInf: 5 },                      // golden summit
  { f: 1362, cInf: 11, focus: ownerEyes },   // luckily
  { f: 1457, cInf: 13, focus: ownerEyes },   // unluckily
  { f: 1527, cInf: 0 },                      // snowball, halves
  { f: 1709, cInf: 6, focus: sitEyes },      // 350 years (the tree must read)
  { f: 1799, cInf: 12, focus: sitEyes },
  { f: 1897, cInf: 0 },                      // golden aerial
  { f: 1978, cInf: 12, focus: ownerEyes },   // keep the dollar
  { f: 2020, dur: 50, cInf: 0 },             // crane out
];
export const dofAt = (f: number) => {
  let i = 0; while (i + 1 < DOF.length && f >= DOF[i + 1].f) i++;
  const d = DOF[i], p = DOF[Math.max(0, i - 1)];
  const k = d.dur ? Math.min(1, (f - d.f) / d.dur) : 1;
  return { cInf: p.cInf + (d.cInf - p.cInf) * k, focus: d.focus };
};
export const focusAt = (id: number, f: number): V3 => {
  const d = dofAt(f);
  return d.focus ? d.focus(f) : camAt(id, f).look;
};

/** near framing objects (Kenney kit names; the kit is not in the skill download, so only vegetation kinds draw) */
export type Fg = { a: number; b: number; kit: string; pos: V3; s?: number; yaw?: number };
export const FOREGROUND: Fg[] = [
];

// bridge anchorage (the town's bridge geometry still reads these)
export const ANCHOR: V3 = [-2.7, D0 + 0.62, -37];
export const snapEnd = (snap: number): V3 => {
  const u = easeOut(snap);
  return [ANCHOR[0] - 0.6 * u, ANCHOR[1] + 5.5 * u - 2.0 * u * u, ANCHOR[2] + 4.5 * u];
};
