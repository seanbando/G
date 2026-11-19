// The money of the $1 short: painted bills, growing heaps of bills, the owner's kitchen table with its stacks,
// the money snowball and the 350-year tree. Everything is lit by the same two-tone shading as the town (lam()),
// textures are painted on canvases with their seams as dark tints (no captions or numbers anywhere).
import * as THREE from "three";
import { lam, V } from "./build";
import { ctex, rng } from "./paint";
import { D0, HEAPS, HeapDef, TABLE, TABLE_TOP, V3, heapsAt, tableBills, snowball, growAt, clamp01 } from "./story";

// ---------------- paint ----------------
const PAPER = "#d9e4c6", PAPER_D = "#c4d3ae", INKG = "#3f6a45", INKG_D = "#2c4f35", SEAM = "rgba(30,52,36,0.55)";
/** one bill, front face: pale green paper, dark green ornate border, central oval, corner rosettes (no lettering) */
const drawBill = (g: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, rot: number, tone = 1) => {
  g.save(); g.translate(x, y); g.rotate(rot);
  const k = (c: string) => { const col = new THREE.Color(c).multiplyScalar(tone); return "#" + col.getHexString(); };
  g.fillStyle = SEAM; g.fillRect(-w / 2 - 2, -h / 2 - 2, w + 4, h + 4); // the seam under the bill edge
  g.fillStyle = k(PAPER); g.fillRect(-w / 2, -h / 2, w, h);
  g.strokeStyle = k(INKG); g.lineWidth = h * 0.07; g.strokeRect(-w / 2 + h * 0.09, -h / 2 + h * 0.09, w - h * 0.18, h - h * 0.18);
  g.lineWidth = h * 0.025; g.strokeRect(-w / 2 + h * 0.17, -h / 2 + h * 0.17, w - h * 0.34, h - h * 0.34);
  g.fillStyle = k(PAPER_D); g.beginPath(); g.ellipse(0, 0, h * 0.3, h * 0.36, 0, 0, Math.PI * 2); g.fill();
  g.strokeStyle = k(INKG_D); g.lineWidth = h * 0.05; g.stroke();
  g.fillStyle = k(INKG); g.beginPath(); g.ellipse(0, h * 0.06, h * 0.13, h * 0.17, 0, 0, Math.PI * 2); g.fill(); // portrait silhouette
  for (const sx of [-1, 1]) for (const sy of [-1, 1]) {
    g.beginPath(); g.arc(sx * (w / 2 - h * 0.3), sy * (h / 2 - h * 0.3), h * 0.1, 0, Math.PI * 2); g.fillStyle = k(INKG); g.fill();
  }
  for (const sx of [-1, 1]) { g.beginPath(); g.arc(sx * w * 0.27, 0, h * 0.16, 0, Math.PI * 2); g.strokeStyle = k(INKG); g.lineWidth = h * 0.035; g.stroke(); }
  g.restore();
};
export const billTex = () => ctex("bill", 512, 220, (g) => drawBill(g, 256, 110, 504, 212, 0));
/** a tile of heaped bills: hundreds of overlapping bills at random angles, darker deeper down, wrapping seamlessly */
export const heapTex = () => ctex("moneyHeap", 1024, 1024, (g, r) => {
  g.fillStyle = "#6f9365"; g.fillRect(0, 0, 1024, 1024);
  for (let layer = 0; layer < 3; layer++) for (let i = 0; i < 260; i++) {
    const x = r() * 1024, y = r() * 1024, w = 150 + r() * 30, rot = r() * Math.PI, tone = 0.72 + 0.12 * layer + 0.12 * r();
    for (const ox of [-1024, 0, 1024]) for (const oy of [-1024, 0, 1024]) {
      if (x + ox < -120 || x + ox > 1144 || y + oy < -120 || y + oy > 1144) continue;
      drawBill(g, x + ox, y + oy, w, w * 0.43, rot, tone);
    }
  }
});
const clothTex = () => ctex("tablecloth", 256, 256, (g) => {
  g.fillStyle = "#f4efe4"; g.fillRect(0, 0, 256, 256);
  g.fillStyle = "rgba(196,58,58,0.55)";
  for (let i = 0; i < 8; i++) { g.fillRect(i * 32, 0, 16, 256); g.fillRect(0, i * 32, 256, 16); }
  g.fillStyle = "rgba(160,40,44,0.35)";
  for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) g.fillRect(i * 32, j * 32, 16, 16);
});

// ---------------- heaps ----------------
const N = 120;
const hash = (i: number, j: number, s: number) => { const v = Math.sin(i * 127.1 + j * 311.7 + s * 74.7) * 43758.5453; return v - Math.floor(v); };
/** smooth value noise (lumps of bills) in heap-local units */
const noise = (x: number, z: number, s: number) => {
  const xi = Math.floor(x), zi = Math.floor(z), fx = x - xi, fz = z - zi;
  const u = fx * fx * (3 - 2 * fx), v = fz * fz * (3 - 2 * fz);
  const a = hash(xi, zi, s), b = hash(xi + 1, zi, s), c = hash(xi, zi + 1, s), d = hash(xi + 1, zi + 1, s);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
};
/** height above the ground of heap `h` grown to k (0..1) at world (x, z); <= 0 outside */
export const heapH = (h: HeapDef, k: number, x: number, z: number) => {
  if (k <= 0) return 0;
  const s = 0.55 + 0.45 * k, ax = h.ax * s, az = h.az * s, H = h.H * k;
  const dx = (x - h.x) / ax, dz = (z - h.z) / az;
  const d = Math.pow(Math.abs(dx) ** 4 + Math.abs(dz) ** 4, 0.25) * (1 - h.peak) + Math.hypot(dx, dz) * h.peak;
  if (d >= 1.04) return -1;
  const plateau = 1 - THREE.MathUtils.smoothstep(d, 0.72, 1.04);
  const peak = Math.max(0, 1 - d * d) ** 0.75;
  const base = plateau * (1 - h.peak) + peak * h.peak;
  const sc = Math.max(1.2, Math.min(ax, az) * 0.22);
  const lump = (noise(x / sc, z / sc, h.seed) - 0.5) * 0.5 + (noise(x / (sc * 0.37), z / (sc * 0.37), h.seed + 9) - 0.5) * 0.22;
  return H * base + Math.min(H * 0.12, 0.35 + H * 0.06) * lump * Math.min(1, d * 3) * (base > 0.02 ? 1 : 0);
};

class Heap {
  mesh: THREE.Mesh; private k = -1;
  constructor(public def: HeapDef, parent: THREE.Object3D, mat: THREE.Material) {
    const g = new THREE.BufferGeometry(), n = (N + 1) * (N + 1);
    g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(n * 3), 3));
    g.setAttribute("normal", new THREE.BufferAttribute(new Float32Array(n * 3), 3));
    g.setAttribute("uv", new THREE.BufferAttribute(new Float32Array(n * 2), 2));
    const idx: number[] = [];
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
      const a = j * (N + 1) + i, b = a + 1, c = a + N + 1, d = c + 1;
      idx.push(a, c, b, b, c, d);
    }
    g.setIndex(idx);
    this.mesh = new THREE.Mesh(g, mat);
    this.mesh.castShadow = true; this.mesh.receiveShadow = true; this.mesh.frustumCulled = false; this.mesh.visible = false;
    parent.add(this.mesh);
  }
  pose(k: number) {
    this.mesh.visible = k > 0;
    if (k <= 0 || Math.abs(k - this.k) < 1e-4) return;
    this.k = k;
    const h = this.def, s = 0.55 + 0.45 * k, ex = h.ax * s * 1.06, ez = h.az * s * 1.06, tile = Math.max(2.4, Math.min(h.ax, h.az) * 0.12);
    const pos = this.mesh.geometry.attributes.position.array as Float32Array, uv = this.mesh.geometry.attributes.uv.array as Float32Array;
    for (let j = 0; j <= N; j++) for (let i = 0; i <= N; i++) {
      const x = h.x - ex + (2 * ex * i) / N, z = h.z - ez + (2 * ez * j) / N, y = heapH(h, k, x, z);
      const o = j * (N + 1) + i;
      pos[o * 3] = x; pos[o * 3 + 1] = y > 0 ? D0 + y : D0 - 0.4; pos[o * 3 + 2] = z;
      uv[o * 2] = x / tile; uv[o * 2 + 1] = z / tile;
    }
    const g = this.mesh.geometry;
    g.attributes.position.needsUpdate = true; g.attributes.uv.needsUpdate = true;
    g.computeVertexNormals(); g.computeBoundingSphere();
  }
}

// ---------------- the money layer ----------------
const BILL_W = 0.32, BILL_D = 0.14, BILL_T = 0.006; // cartoon bills, about twice real size so they read on the table
export class Money {
  root = new THREE.Group();
  private heaps: Record<string, Heap> = {};
  private stack: THREE.InstancedMesh;
  private ball: THREE.Mesh;
  private tree = new THREE.Group();
  private m4 = new THREE.Matrix4(); private q = new THREE.Quaternion(); private e = new THREE.Euler();
  constructor(parent: THREE.Object3D) {
    const R = this.root; parent.add(R);
    const ht = heapTex(); ht.anisotropy = 16;
    const heapM = lam("moneyHeapM", () => ({ map: ht }));
    for (const [name, def] of Object.entries(HEAPS)) this.heaps[name] = new Heap(def, R, heapM);
    // kitchen table + two chairs (wood, checked cloth)
    const wood = lam("tableWood", () => ({ color: "#a8724a" })), cloth = lam("tableCloth", () => ({ map: clothTex() }));
    const [tx, , tz] = TABLE, top = D0 + TABLE_TOP;
    const box = (w: number, h: number, d: number, x: number, y: number, z: number, m: THREE.Material) => {
      const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; R.add(o); return o;
    };
    box(1.3, 0.05, 0.9, tx, top - 0.025, tz, cloth);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) box(0.07, TABLE_TOP - 0.05, 0.07, tx + sx * 0.56, D0 + (TABLE_TOP - 0.05) / 2, tz + sz * 0.36, wood);
    for (const sx of [-1, 1]) {
      const cx = tx + sx * 1.0;
      box(0.45, 0.05, 0.45, cx, D0 + 0.46, tz, wood);
      for (const a of [-1, 1]) for (const b of [-1, 1]) box(0.05, 0.46, 0.05, cx + a * 0.19, D0 + 0.23, tz + b * 0.19, wood);
      box(0.05, 0.55, 0.45, cx + sx * 0.2, D0 + 0.76, tz, wood);
    }
    // bills on the table: one instanced box per bill, stacked in neat piles
    const billM = [lam("billEdge", () => ({ color: "#c9d6b4" })), lam("billEdge", () => ({ color: "#c9d6b4" })),
      lam("billFace", () => ({ map: billTex() })), lam("billFace", () => ({ map: billTex() })), lam("billEdge", () => ({ color: "#c9d6b4" })), lam("billEdge", () => ({ color: "#c9d6b4" }))];
    this.stack = new THREE.InstancedMesh(new THREE.BoxGeometry(BILL_W, BILL_T, BILL_D), billM, 300);
    this.stack.castShadow = true; this.stack.receiveShadow = true; this.stack.frustumCulled = false; R.add(this.stack);
    // the money snowball
    const bt = heapTex().clone(); bt.repeat.set(3, 1.5); bt.needsUpdate = true;
    this.ball = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 24), lam("moneyBall", () => ({ map: bt })));
    this.ball.castShadow = true; this.ball.visible = false; R.add(this.ball);
    // the 350-year tree beside the table: tapered trunk + clustered round canopy, grown by scale
    const bark = lam("barkHD", () => ({ color: "#8f5d3b" })), leaf = lam("treeLeaf", () => ({ color: "#5aa83c" })), leaf2 = lam("treeLeaf2", () => ({ color: "#4c9a37" }));
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.3, 3.2, 10).translate(0, 1.6, 0), bark);
    this.tree.add(trunk);
    const r = rng(77);
    for (let i = 0; i < 7; i++) {
      const a = (i / 7) * Math.PI * 2, rr = i ? 1.0 : 0;
      const s = new THREE.Mesh(new THREE.SphereGeometry(i ? 1.15 : 1.5, 24, 14), i % 2 ? leaf2 : leaf);
      s.position.set(Math.cos(a) * rr, 4.0 + (i ? 0.3 * r() - 0.3 : 0.5), Math.sin(a) * rr);
      this.tree.add(s);
    }
    this.tree.traverse((o) => { o.castShadow = true; o.receiveShadow = true; });
    this.tree.position.set(tx - 1.2, D0, tz + 2.1);
    R.add(this.tree);
  }
  /** surface height of the near mountain (for the snowball) */
  nearY(x: number, z: number) { return D0 + Math.max(0, heapH(HEAPS.near, 1, x, z)); }

  update(id: number, f: number) {
    const hs = heapsAt(id, f);
    for (const [name, h] of Object.entries(this.heaps)) h.pose(hs[name] ?? 0);
    // bills on the table
    const n = tableBills(id, f), [tx, , tz] = TABLE, top = D0 + TABLE_TOP;
    const piles: [number, number][] = [[0, 0], [0.34, 0.16], [-0.34, 0.16], [0.34, -0.16], [-0.34, -0.16], [0, 0.32], [0, -0.32], [0.68, 0], [-0.68, 0]];
    const per = Math.max(1, Math.ceil(n / piles.length));
    for (let i = 0; i < n; i++) {
      const p = n <= 2 ? i : Math.floor(i / per), level = n <= 2 ? 0 : i % per, [px, pz] = piles[Math.min(piles.length - 1, p)];
      const jx = (hash(i, 1, 3) - 0.5) * 0.03, jz = (hash(i, 2, 3) - 0.5) * 0.03, yaw = (hash(i, 3, 3) - 0.5) * (n <= 2 ? 0.5 : 0.18) + (n <= 2 && i ? 0.7 : 0);
      this.q.setFromEuler(this.e.set(0, yaw, 0));
      this.m4.compose(V(tx + px + jx + (n <= 2 && i ? 0.06 : 0), top + BILL_T * (0.5 + level) + (n <= 2 && i ? BILL_T : 0), tz + pz + jz), this.q, V(1, 1, 1));
      this.stack.setMatrixAt(i, this.m4);
    }
    this.stack.count = n; this.stack.visible = n > 0; this.stack.instanceMatrix.needsUpdate = true;
    // the snowball
    this.ball.visible = id === 14;
    if (this.ball.visible) {
      const s = snowball(f), y = this.nearY(s.x, s.z);
      this.ball.position.set(s.x, y + s.r * 0.9, s.z); this.ball.scale.setScalar(s.r); this.ball.rotation.set(s.roll / Math.max(0.6, s.r), 0, 0);
    }
    // the tree: a sapling at the start of the 350 years, full grown by the end of the shot
    this.tree.visible = id === 16;
    const g = 0.12 + 0.88 * clamp01(growAt(f)) ** 0.8;
    this.tree.scale.set(g, g, g);
  }
}
export type { V3 };
