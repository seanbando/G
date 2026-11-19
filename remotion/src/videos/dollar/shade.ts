// Stylised two-tone lighting for every world material (lighting.md 9.2, world part): albedo x mix(shadeCol, litCol,
// sunTerm), sunTerm = real shadow-map visibility x a soft N.L terminator. The sun visibility is captured inside three's
// own light loop (LFB), so nothing is computed twice. Character cards (cardShade) live in the CHAR agent's file and
// can import LFB / CHAR from here; world.ts sets every uniform below once per frame from LIGHTS.
import * as THREE from "three";

export const TONE = {
  uLitCol: { value: new THREE.Vector3(1.5, 1.44, 1.32) }, uShadeCol: { value: new THREE.Vector3(0.6, 0.58, 0.86) },
  uShadeLift: { value: new THREE.Vector3() }, uLambert: { value: 0.35 }, uSideK: { value: 0.84 }, uTerm: { value: 0.2 },
  uBounce: { value: new THREE.Vector3() }, // warm bounce on shaded faces turned to the camera (golden only; day = 0)
  uSat: { value: 1 }, // world albedo saturation around its luminance (characters are not twoTone, so unaffected)
};
/** character-card uniforms (lighting.md 9.2 cardShade); world.ts keeps them in sync with LIGHTS for cardshade.ts */
export const CHAR = {
  uCharTint: { value: new THREE.Vector3(1, 0.94, 0.92) }, uCharShade: { value: 0.86 }, uGrad: { value: 0.07 },
  uBodyGrad: { value: 0.2 }, uSideTint: { value: new THREE.Vector3(0.92, 0.9, 0.96) },
};

// directional light 0 = the sun = the only shadow caster (three sorts shadow-casting lights first). Only the
// UNROLLED index 0 compiles the shadow block, so sunVis is written once.
export const LFB = THREE.ShaderChunk.lights_fragment_begin
  .replace("directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ]",
    "sunVis = ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ]")
  .replace("vDirectionalShadowCoord[ i ] ) : 1.0;", "vDirectionalShadowCoord[ i ] ) : 1.0;\n\t\tdirectLight.color *= sunVis;");
if (!LFB.includes("directLight.color *= sunVis")) throw new Error("shade.ts: three lights_fragment_begin changed");

const TWO_TONE = /* glsl */ `
#if NUM_DIR_LIGHTS > 0
{
  vec3 sunV = directionalLights[ 0 ].direction;                               // view space, towards the sun
  vec3 upV = normalize( ( viewMatrix * vec4( 0.0, 1.0, 0.0, 0.0 ) ).xyz );
  float ndl = max( dot( geometryNormal, sunV ), 0.0 );
  float sunTerm = sunVis * smoothstep( 0.0, uTerm, ndl );                     // 0 = cast/form shadow, 1 = lit
  float skyK = mix( uSideK, 1.0, 0.5 + 0.5 * dot( geometryNormal, upV ) );    // up-facing a bit brighter
  vec3 lit = uLitCol * mix( 1.0, ndl, uLambert );                             // keep some cosine modelling
  float facing = max( dot( geometryNormal, geometryViewDir ), 0.0 );        // 1 = faces the lens
  vec3 alb = max( mix( vec3( dot( diffuseColor.rgb, vec3( 0.2126, 0.7152, 0.0722 ) ) ), diffuseColor.rgb, uSat ), 0.0 );
  reflectedLight.directDiffuse = alb * ( mix( uShadeCol, lit, sunTerm ) * skyK + uBounce * facing * clamp( 1.0 - dot( geometryNormal, upV ), 0.0, 1.0 ) * ( 1.0 - sunTerm ) )
    + uShadeLift * LIFT_K * ( 1.0 - sunTerm );
  reflectedLight.indirectDiffuse = vec3( 0.0 );                               // hemisphere/fill no longer used here
}
#endif
`;
const DECL = "#include <common>\nuniform vec3 uLitCol; uniform vec3 uShadeCol; uniform vec3 uShadeLift; uniform float uLambert; uniform float uSideK; uniform float uTerm; uniform vec3 uBounce; uniform float uSat;";

/** Lambert (or Phong: its specular term is kept, masked by the shadow) -> two-tone. Call once per material. */
export function twoTone<T extends THREE.MeshLambertMaterial | THREE.MeshPhongMaterial>(m: T, liftK = 1): T {
  m.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, TONE);
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", DECL + `\n#define LIFT_K ${liftK.toFixed(3)}`)
      .replace("#include <lights_fragment_begin>", "float sunVis = 1.0;\n" + LFB)
      .replace("#include <lights_fragment_end>", "#include <lights_fragment_end>\n" + TWO_TONE);
  };
  m.customProgramCacheKey = () => "twoTone5_" + liftK.toFixed(3);
  return m;
}

// ---------------- anti-tiling (look fix: repeats read as fake) ----------------
const AT_NOISE = /* glsl */ `
varying vec3 vAtWP;
float atH( vec2 p ) { return fract( sin( dot( p, vec2( 127.1, 311.7 ) ) ) * 43758.5453 ); }
float atNoise( vec2 p ) {
  vec2 i = floor( p ), f = fract( p ); vec2 u = f * f * ( 3.0 - 2.0 * f );
  return mix( mix( atH( i ), atH( i + vec2( 1.0, 0.0 ) ), u.x ), mix( atH( i + vec2( 0.0, 1.0 ) ), atH( i + vec2( 1.0, 1.0 ) ), u.x ), u.y );
}`;
/** Breaks up a repeating map on big ground surfaces: blends the map with a rotated, rescaled copy of itself by a
 *  world-space noise (so the tile grid never lines up), and adds slow light/dark (and warm/dry) patches tens of
 *  metres across, which also keep the far field from mipmapping to one flat colour. Chains after twoTone(). */
export function antiTile<T extends THREE.Material>(m: T, o: { cell: number; macro: number; amp: number; dry?: number }): T {
  const prev = m.onBeforeCompile.bind(m);
  const key = m.customProgramCacheKey.bind(m);
  m.onBeforeCompile = (sh, r) => {
    prev(sh, r);
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vAtWP;")
      .replace("#include <project_vertex>", "#include <project_vertex>\nvAtWP = ( modelMatrix * vec4( transformed, 1.0 ) ).xyz;");
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", "#include <common>\n" + AT_NOISE)
      .replace("#include <map_fragment>", /* glsl */ `
#ifdef USE_MAP
  vec2 atP = vAtWP.xz;
  float atSel = smoothstep( 0.3, 0.7, atNoise( atP / ${o.cell.toFixed(2)} ) );
  vec2 atUv2 = mat2( 0.8, -0.6, 0.6, 0.8 ) * vMapUv * 0.73 + vec2( 0.37, 0.71 );
  vec4 sampledDiffuseColor = mix( texture2D( map, vMapUv ), texture2D( map, atUv2 ), atSel );
  float atMac = 0.6 * atNoise( atP / ${o.macro.toFixed(2)} + 13.1 ) + 0.4 * atNoise( atP / ${(o.macro * 0.31).toFixed(2)} + 4.2 );
  sampledDiffuseColor.rgb *= mix( ${(1 - o.amp).toFixed(3)}, ${(1 + o.amp).toFixed(3)}, atMac );
  float atDry = smoothstep( 0.62, 0.9, atNoise( atP / ${(o.macro * 0.7).toFixed(2)} + 31.7 ) ) * ${(o.dry ?? 0).toFixed(3)};
  sampledDiffuseColor.rgb = mix( sampledDiffuseColor.rgb, sampledDiffuseColor.rgb * vec3( 1.12, 1.02, 0.7 ), atDry );
  diffuseColor *= sampledDiffuseColor;
#endif`);
  };
  m.customProgramCacheKey = () => key() + "_at" + o.cell + "_" + o.macro + "_" + o.amp + "_" + (o.dry ?? 0);
  m.needsUpdate = true;
  return m;
}

// ---------------- tone-map inversion ----------------
// The composer ends in PBR-Neutral tone mapping, so a colour written to the scene buffer is NOT what lands on screen
// (toe: -0.04 linear offset, shoulder above 0.76). Self-lit things whose on-screen colour is a measured target (sky,
// fog, river) are written as untone(target): the linear value that the Neutral curve maps onto the target.
const neutral = (c: number[]) => {
  const x = Math.min(c[0], c[1], c[2]), off = x < 0.08 ? x - 6.25 * x * x : 0.04;
  const v = c.map((k) => k - off), peak = Math.max(v[0], v[1], v[2]), S = 0.76;
  if (peak < S) return v;
  const d = 1 - S, np = 1 - (d * d) / (peak + d - S), g = 1 - 1 / (0.15 * (peak - np) + 1);
  return v.map((k) => (k * np) / peak * (1 - g) + np * g);
};
/** linear input that the Neutral tone map turns into the given on-screen colour (hex or THREE.Color, sRGB target) */
export const untone = (target: THREE.ColorRepresentation, out = new THREE.Color()) => {
  const t = new THREE.Color(target); // linear working space
  const tt = [t.r, t.g, t.b].map((k) => Math.min(k, 0.985));
  let c = tt.slice();
  for (let i = 0; i < 60; i++) { const y = neutral(c); c = c.map((k, j) => Math.max(0, k + (tt[j] - y[j]))); }
  return out.setRGB(c[0], c[1], c[2]);
};
