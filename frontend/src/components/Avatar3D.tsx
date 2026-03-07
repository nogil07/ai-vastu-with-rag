import React, { Suspense, useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useGLTF, Html } from '@react-three/drei';
import * as THREE from 'three';

const Loading = () => (
  <Html center>
    <div className="w-8 h-8 border-4 border-arch-accent border-t-transparent rounded-full animate-spin" />
  </Html>
);

function Model({ flipKey = 0, idle = true, walking = false }: { flipKey?: number; idle?: boolean; walking?: boolean }) {
  const group = useRef<THREE.Group | null>(null);
  const { scene } = useGLTF('/crab.glb') as any;

  // flip state
  const flipRef = useRef({ active: false, start: 0, duration: 0.8, fromX: 0, fromY: 0 });
  const prevFlip = useRef(flipKey);

  useEffect(() => {
    if (flipKey !== prevFlip.current) {
      prevFlip.current = flipKey;
      flipRef.current.active = true;
      flipRef.current.start = -1; // marker; set on next frame
      flipRef.current.fromX = group.current ? group.current.rotation.x : 0;
      flipRef.current.fromY = group.current ? group.current.rotation.y : 0;
    }
  }, [flipKey]);

  // attempt to locate skeleton/bones for walking animation
  const bonesRef = useRef<any>({ leftArm: null, rightArm: null, leftLeg: null, rightLeg: null, meshArms: [], meshLegs: [] });
  useEffect(() => {
    const meshCandidates: any[] = [];
    const skinned: any[] = [];

    scene.traverse((c: any) => {
      const name = (c.name || '').toLowerCase();
      if (c.isSkinnedMesh) {
        skinned.push(c);
      }
      if (c.isBone) {
        // try to find bones by name
        if (name.includes('arm') || name.includes('hand') || name.includes('paw') || name.includes('upperarm') || name.includes('shoulder') || name.includes('forearm')) {
          if (!bonesRef.current.leftArm) bonesRef.current.leftArm = c;
          else if (!bonesRef.current.rightArm) bonesRef.current.rightArm = c;
        }
        if (name.includes('leg') || name.includes('thigh') || name.includes('calf') || name.includes('foot')) {
          if (!bonesRef.current.leftLeg) bonesRef.current.leftLeg = c;
          else if (!bonesRef.current.rightLeg) bonesRef.current.rightLeg = c;
        }
      }
      if (c.isMesh) meshCandidates.push(c);
    });

    // If any skinned mesh exists, inspect their skeleton bones for named arm/leg bones
    if (skinned.length) {
      for (const s of skinned) {
        const bones = s.skeleton?.bones || [];
        bones.forEach((b: any) => {
          const n = (b.name || '').toLowerCase();
          if (n.includes('arm') || n.includes('hand') || n.includes('paw') || n.includes('upperarm') || n.includes('shoulder') || n.includes('forearm')) {
            if (!bonesRef.current.leftArm) bonesRef.current.leftArm = b;
            else if (!bonesRef.current.rightArm) bonesRef.current.rightArm = b;
          }
          if (n.includes('leg') || n.includes('thigh') || n.includes('calf') || n.includes('foot')) {
            if (!bonesRef.current.leftLeg) bonesRef.current.leftLeg = b;
            else if (!bonesRef.current.rightLeg) bonesRef.current.rightLeg = b;
          }
        });
      }
    }

    // if no bones found, attempt mesh-based heuristic by name first, then by position
    if (!bonesRef.current.leftArm && !bonesRef.current.rightArm) {
      const armMeshes = meshCandidates.filter((m) => {
        const n = (m.name || '').toLowerCase();
        return n.includes('arm') || n.includes('hand') || n.includes('paw') || n.includes('upperarm') || n.includes('shoulder') || n.includes('forearm');
      });
      if (armMeshes.length) bonesRef.current.meshArms = armMeshes.slice(0, 2);
      else if (meshCandidates.length) {
        const withPos = meshCandidates.map((m) => {
          const pos = new THREE.Vector3();
          m.getWorldPosition(pos);
          return { mesh: m, y: pos.y };
        }).sort((a, b) => b.y - a.y);
        bonesRef.current.meshArms = withPos.slice(0, 2).map((p) => p.mesh);
      }
    }

    // Detect explicit crab leg segment naming (leg<number>.<segment>.<side>) and hands
    const legsMap: Record<string, { L: Array<any>, R: Array<any> }> = {};
    const hands: Array<any> = [];
    meshCandidates.forEach((m) => {
      const nm = (m.name || '');
      const legMatch = nm.match(/^leg(\d+)\.(\d+)\.(l|r)$/i);
      if (legMatch) {
        const li = legMatch[1];
        const seg = parseInt(legMatch[2], 10);
        const side = legMatch[3].toUpperCase();
        legsMap[li] = legsMap[li] || { L: [], R: [] };
        legsMap[li][side].push({ seg, mesh: m });
      }
      if (/^Hand\./i.test(nm)) hands.push(m);
    });

    // sort segments by segment index
    const legOrder = Object.keys(legsMap).sort((a, b) => parseInt(a) - parseInt(b));
    legOrder.forEach((li) => {
      ['L', 'R'].forEach((side) => {
        legsMap[li][side].sort((a: any, b: any) => a.seg - b.seg);
        legsMap[li][side] = legsMap[li][side].map((p: any) => p.mesh);
      });
    });

    if (legOrder.length) {
      bonesRef.current.legs = legsMap;
      bonesRef.current.legOrder = legOrder;
      bonesRef.current.hands = hands;
    }

    if (!bonesRef.current.leftLeg && !bonesRef.current.rightLeg) {
      // Broaden heuristics for crab-style models: include claws/pincers and appendages
      const legNameCandidates = ['leg', 'thigh', 'calf', 'foot', 'claw', 'pincer', 'chela', 'appendage', 'pereopod', 'pedipalp'];
      const legMeshes = meshCandidates.filter((m) => {
        const n = (m.name || '').toLowerCase();
        return legNameCandidates.some((s) => n.includes(s));
      });

      if (legMeshes.length) {
        // keep all leg-like meshes (crabs have many legs). store full list for wave animation
        bonesRef.current.meshLegs = legMeshes.slice();
        // compute phase offsets for staggered leg movement based on X position
        try {
          const positions = bonesRef.current.meshLegs.map((m: any, i: number) => {
            const p = new THREE.Vector3();
            m.getWorldPosition(p);
            return { mesh: m, x: p.x, idx: i };
          }).sort((a: any, b: any) => a.x - b.x);
          bonesRef.current.legPhases = positions.map((p: any, i: number) => (i / Math.max(1, positions.length)) * Math.PI);
        } catch (e) {
          bonesRef.current.legPhases = (bonesRef.current.meshLegs || []).map((_: any, i: number) => i * 0.4);
        }
      } else if (meshCandidates.length) {
        // fallback: pick lowest meshes as legs
        const withPos = meshCandidates.map((m) => {
          const pos = new THREE.Vector3();
          m.getWorldPosition(pos);
          return { mesh: m, y: pos.y };
        }).sort((a, b) => a.y - b.y); // bottom first
        bonesRef.current.meshLegs = withPos.slice(0, Math.min(6, withPos.length)).map((p) => p.mesh);
        bonesRef.current.legPhases = bonesRef.current.meshLegs.map((_: any, i: number) => i * 0.4);
      }
    }

    // Debug: log findings to browser console to help identify why limbs aren't animating
    try {
      const nodeNames: string[] = [];
      scene.traverse((c: any) => nodeNames.push(`${c.type}:${c.name || '<anon>'}`));
      console.debug('[Avatar3D] scene node count:', nodeNames.length);
      console.debug('[Avatar3D] nodes sample:', nodeNames.slice(0, 80));
      console.debug('[Avatar3D] skinned meshes:', skinned.map(s => s.name || '<anon>'));
      console.debug('[Avatar3D] bones found:', {
        leftArm: bonesRef.current.leftArm?.name || null,
        rightArm: bonesRef.current.rightArm?.name || null,
        leftLeg: bonesRef.current.leftLeg?.name || null,
        rightLeg: bonesRef.current.rightLeg?.name || null,
        meshArms: (bonesRef.current.meshArms || []).map((m: any) => m.name || '<anon>'),
        meshLegs: (bonesRef.current.meshLegs || []).map((m: any) => m.name || '<anon>')
      });
    } catch (err) {
      console.debug('[Avatar3D] debug log failed', err);
    }
  }, [scene]);

  // Gentle idle rotation + float + flip animation when triggered
  useFrame((state, delta) => {
    if (!group.current) return;

    const time = state.clock.elapsedTime;

    if (flipRef.current.active) {
      if (flipRef.current.start < 0) flipRef.current.start = time;
      const t = (time - flipRef.current.start) / flipRef.current.duration;
      if (t >= 1) {
        group.current.rotation.x = flipRef.current.fromX + Math.PI * 2;
        group.current.rotation.y = flipRef.current.fromY + Math.PI * 2;
        flipRef.current.active = false;
      } else {
        const eased = 0.5 - 0.5 * Math.cos(Math.min(1, Math.max(0, t)) * Math.PI);
        group.current.rotation.x = flipRef.current.fromX + eased * Math.PI * 2;
        group.current.rotation.y = flipRef.current.fromY + eased * Math.PI * 2;
      }
    } else {
      if (walking) {
        // walking limb swing
        const walkSpeed = 6; // speed multiplier for limb swing
        const swing = Math.sin(time * walkSpeed) * 0.6;
        const armAngle = swing * 0.6;
        const legAngle = -swing * 0.9;
        if (bonesRef.current.leftArm) bonesRef.current.leftArm.rotation.x = armAngle;
        if (bonesRef.current.rightArm) bonesRef.current.rightArm.rotation.x = -armAngle;
        if (bonesRef.current.leftLeg) bonesRef.current.leftLeg.rotation.x = legAngle;
        if (bonesRef.current.rightLeg) bonesRef.current.rightLeg.rotation.x = -legAngle;
        // mesh-based fallback
        if (bonesRef.current.meshArms && bonesRef.current.meshArms.length) {
          bonesRef.current.meshArms.forEach((m: any, i: number) => {
            m.rotation.x = (i % 2 === 0 ? armAngle : -armAngle);
          });
        }

        // Crab-specific: animate detected leg segments by explicit leg IDs if available
        const legsMap = bonesRef.current.legs;
        const legOrder = bonesRef.current.legOrder || [];
        if (legsMap && legOrder.length) {
          const freq = walking ? 6 : 3.5;
          const amp = walking ? 0.9 : 0.6;
          legOrder.forEach((li: string, legIdx: number) => {
            const phasesBase = (legIdx / Math.max(1, legOrder.length)) * Math.PI * 2;
            ['L', 'R'].forEach((side, sIdx) => {
              const segs = (legsMap[li] && legsMap[li][side]) || [];
              segs.forEach((m: any, segIdx: number) => {
                try {
                  if (!m.userData._origRot) m.userData._origRot = { x: m.rotation.x, y: m.rotation.y, z: m.rotation.z };
                  const phase = phasesBase + (sIdx * Math.PI) + segIdx * 0.35;
                  const decay = 1 - segIdx * 0.09; // outer segments move slightly less
                  const theta = Math.sin(time * freq + phase) * amp * decay;
                  // main crab leg swing around Z (sideways)
                  m.rotation.z = m.userData._origRot.z + theta * 0.9;
                  // small X rotation for lifting/lowering motion
                  m.rotation.x = m.userData._origRot.x + Math.cos(time * freq + phase) * (amp * 0.18) * decay;
                } catch (err) {
                  // ignore single mesh errors
                }
              });
            });
          });
        } else if (bonesRef.current.meshLegs && bonesRef.current.meshLegs.length) {
          const phases = bonesRef.current.legPhases || [];
          bonesRef.current.meshLegs.forEach((m: any, i: number) => {
            try {
              if (m.userData._origRotX === undefined) m.userData._origRotX = m.rotation.x || 0;
              const phase = phases[i] ?? (i * 0.4);
              const amp = walking ? 0.9 : 0.35;
              const freq = walking ? 6 : 2.2;
              const theta = Math.sin(time * freq + phase) * amp;
              m.rotation.x = m.userData._origRotX + theta * 0.6;
              m.rotation.z = (m.userData._origRotZ ?? 0) + Math.cos(time * freq + phase) * (amp * 0.25);
            } catch (err) {
              // ignore per-mesh failures
            }
          });
        }
        // subtle bob
        group.current.position.y = Math.sin(time * 6) * 0.02;
      } else if (idle) {
        // idle spin
        group.current.rotation.y += delta * 0.6;
        // subtle float
        const floatY = Math.sin(time * 1.2) * 0.04;
        group.current.position.y = floatY;
        group.current.rotation.z = Math.sin(time * 0.6) * 0.02;

        // Also animate legs subtly while idle so crab appears alive
        const idleFreq = 2.2;
        const idleAmp = 0.35;
        if (bonesRef.current.leftLeg) bonesRef.current.leftLeg.rotation.x = Math.sin(time * idleFreq) * idleAmp;
        if (bonesRef.current.rightLeg) bonesRef.current.rightLeg.rotation.x = -Math.sin(time * idleFreq) * idleAmp;

        if (bonesRef.current.meshArms && bonesRef.current.meshArms.length) {
          bonesRef.current.meshArms.forEach((m: any, i: number) => {
            const a = Math.sin(time * idleFreq + i) * (idleAmp * 0.6);
            m.rotation.x = (m.userData._origRotX ?? 0) + a;
          });
        }

        if (bonesRef.current.meshLegs && bonesRef.current.meshLegs.length) {
          const phases = bonesRef.current.legPhases || [];
          bonesRef.current.meshLegs.forEach((m: any, i: number) => {
            try {
              if (m.userData._origRotX === undefined) m.userData._origRotX = m.rotation.x || 0;
              if (m.userData._origRotZ === undefined) m.userData._origRotZ = m.rotation.z || 0;
              const phase = phases[i] ?? (i * 0.4);
              const theta = Math.sin(time * idleFreq + phase) * idleAmp;
              m.rotation.x = m.userData._origRotX + theta * 0.6;
              m.rotation.z = m.userData._origRotZ + Math.cos(time * idleFreq + phase) * (idleAmp * 0.25);
            } catch (err) {
              // ignore
            }
          });
        }
      }
    }
  });

  // Ensure materials are non-reflective and consistent with site theme
  scene.traverse((child: any) => {
    if (child.isMesh && child.material) {
      const m = Array.isArray(child.material) ? child.material : [child.material];
      m.forEach((mat: any) => {
        if (mat && mat.isMaterial) {
          mat.roughness = Math.max(0.8, mat.roughness ?? 1);
          mat.metalness = 0;
          if (mat.color) mat.color.convertSRGBToLinear && mat.color.convertSRGBToLinear();
          // Preserve alpha by using material opacity when provided
          if ('opacity' in mat) {
            mat.transparent = mat.opacity < 1;
          }
        }
      });
    }
  });

  // Auto-fit: compute bounding box and normalize scale/position so model is visible
  useEffect(() => {
    try {
      scene.updateMatrixWorld(true);
      const box = new THREE.Box3().setFromObject(scene);
      const size = new THREE.Vector3();
      box.getSize(size);
      const center = new THREE.Vector3();
      box.getCenter(center);
      const maxDim = Math.max(size.x, size.y, size.z);
      // desired size in world units (approximate) to fit in camera frustum
      const desired = 1.8;
      const scale = maxDim > 0 ? desired / maxDim : 1;
      // apply scaling to group (which contains the scene)
      if (group.current) {
        group.current.scale.setScalar(scale);
        // translate so model center is near origin (with slight downward offset)
        group.current.position.set(-center.x * scale, -center.y * scale - 0.2, -center.z * scale);
      }
      console.debug('[Avatar3D] bbox size', size.toArray(), 'center', center.toArray(), 'scale', scale);
    } catch (err) {
      console.debug('[Avatar3D] autofit failed', err);
    }
  }, [scene]);

  return (
    <group ref={group} dispose={null}>
      <primitive object={scene} scale={2} position={[0, -0.2, 0]} />
    </group>
  );
}

export default function Avatar3D({ flipKey = 0, idle = true, walking = false }: { flipKey?: number; idle?: boolean; walking?: boolean }) {
  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [0, 1.1, 3], fov: 30 }}
        shadows={false}
        gl={{ alpha: true }}
        dpr={[1, 1.5]}
        onCreated={({ gl }) => { try { gl.shadowMap.type = THREE.PCFShadowMap; } catch(e){} }}
      >
        <ambientLight intensity={0.8} />
        <directionalLight intensity={0.8} position={[2, 2, 2]} />
        <Suspense fallback={<Loading />}>
          <Model flipKey={flipKey} idle={idle} walking={walking} />
        </Suspense>
      </Canvas>
    </div>
  );
}

useGLTF.preload('/crab.glb');

class CanvasErrorBoundary extends React.Component<{children: React.ReactNode}, {hasError: boolean}> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(err: any) { console.warn('Avatar Canvas error:', err); }
  render() {
    if (this.state.hasError) return <div style={{width: '100%', height: '100%'}} />;
    return this.props.children as any;
  }
}
