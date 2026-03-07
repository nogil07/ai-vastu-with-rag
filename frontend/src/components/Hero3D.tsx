import React, { useRef, useState, useMemo, Suspense } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Float, MeshDistortMaterial, Grid, AdaptiveDpr, AdaptiveEvents, Preload, Bvh, Center, Html, ContactShadows } from '@react-three/drei';
import * as THREE from 'three';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { MotionValue } from 'motion/react';

const HouseModel = React.memo(({ scrollProgress, houseColor }: { scrollProgress?: MotionValue<number>, houseColor: string }) => {
  const meshRef = useRef<THREE.Group>(null);
  
  // Load the OBJ model
  const obj = useLoader(OBJLoader, '/Bambo_House.obj');

  // Process the model to add shadows and default materials if needed
  const model = useMemo(() => {
    if (!obj) return null;
    const clone = obj.clone();
    clone.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true;
        child.receiveShadow = true;
        
        // Identify common parts by group/mesh name
        const name = child.name.toLowerCase();
        const isWall = name.includes('plaster_white') || name.includes('body_house');
        const isRoof = name.includes('roof') || name.includes('tile');
        const isWood = name.includes('wood') || name.includes('timber') || name.includes('beam');

        // If material is missing or basic, upgrade it to Standard for better lighting
        if (child.material) {
          const materials = Array.isArray(child.material) ? child.material : [child.material];
          const newMaterials = materials.map(m => {
            const newM = new THREE.MeshStandardMaterial().copy(m as any);
            newM.roughness = 1.0;
            newM.metalness = 0.0;
            newM.envMapIntensity = 0.0; // Disable environment reflections

            if (isWall) {
              newM.color.set(houseColor);
            } else if (isRoof) {
              newM.color.set('#502700'); // dark roof
            } else if (isWood) {
              newM.color.set('#5d4037'); // brown wood
            } else {
              // Non-painted / detail parts -> set to black for contrast
              newM.color.set('#fff1c8');
              newM.roughness = 0.95;
              newM.metalness = 0.0;
            }

            return newM;
          });
          child.material = Array.isArray(child.material) ? newMaterials : newMaterials[0];
        } else {
          // If no material existed, assign a clear default depending on part type
          let defaultColor = "#000000";
          if (isWall) defaultColor = houseColor;
          else if (isRoof) defaultColor = '#502700';
          else if (isWood) defaultColor = '#5d4037';

          child.material = new THREE.MeshStandardMaterial({
            color: defaultColor,
            roughness: 1.0,
            metalness: 0.0,
            envMapIntensity: 0.0
          });
        }
      }
    });
    return clone;
  }, [obj, houseColor]);
  
  useFrame((state) => {
    const time = state.clock.getElapsedTime();
    
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.0004;
      
      if (scrollProgress) {
        const scroll = scrollProgress.get() || 0;
        meshRef.current.rotation.y = scroll * Math.PI * 0.3 + time * 0.02;
        meshRef.current.position.y = -scroll * 1.3 + 3; // Added 0.5 offset to move it up
      } else {
        meshRef.current.position.y = 10; // Base offset
      }
    }
  });

  return (
    <Bvh firstHitOnly>
      <group ref={meshRef}>
        <Center bottom>
          <primitive object={model} scale={0.7} />
        </Center>

        {/* Subtle Ground Circle instead of large box */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
          <circleGeometry args={[10, 64]} />
          <meshStandardMaterial color="#f0f0f0" roughness={1} metalness={0} transparent opacity={0} />
        </mesh>
      </group>
    </Bvh>
  );
});

const LoadingModel = () => (
  <Html center>
    <div className="flex flex-col items-center gap-4">
      <div className="w-12 h-12 border-4 border-arch-accent border-t-transparent rounded-full animate-spin" />
      <div className="text-subtle font-bold uppercase tracking-widest text-[10px]">Loading 3D Model</div>
    </div>
  </Html>
);

const PRESET_COLORS = [
  { name: 'Sand', value: '#e8e4d9' },
  { name: 'Slate', value: '#475569' },
  { name: 'Emerald', value: '#065f46' },
  { name: 'Terracotta', value: '#9a3412' },
  { name: 'Midnight', value: '#1e293b' },
];

export const Hero3D = React.memo(({ scrollProgress, isDark }: { scrollProgress?: MotionValue<number>, isDark?: boolean }) => {
  const [houseColor, setHouseColor] = useState('#8c0909');

  return (
    <div className="w-full h-[350px] sm:h-[500px] lg:h-[700px] relative group/canvas">
      {/* Color Picker UI */}
      <div className="absolute top-20 right-4 z-30 flex flex-col gap-3 p-4 glass-card rounded-2xl opacity-0 group-hover/canvas:opacity-100 transition-opacity duration-500">
        <div className="text-[10px] uppercase tracking-widest font-bold text-subtle mb-1">Wall Finish</div>
        <div className="flex gap-2">
          {PRESET_COLORS.map((color) => (
            <button
              key={color.value}
              onClick={() => setHouseColor(color.value)}
              className={`w-6 h-6 rounded-full border-2 transition-all ${
                houseColor === color.value ? 'border-arch-accent scale-110 shadow-lg' : 'border-transparent hover:scale-105'
              }`}
              style={{ backgroundColor: color.value }}
              title={color.name}
            />
          ))}
          <div className="relative w-6 h-6 rounded-full overflow-hidden border-2 border-transparent hover:scale-105 transition-transform">
            <input 
              type="color" 
              value={houseColor}
              onChange={(e) => setHouseColor(e.target.value)}
              className="absolute -inset-2 w-10 h-10 cursor-pointer border-none p-0 bg-transparent"
            />
          </div>
        </div>
      </div>

      <Canvas 
        shadows 
        dpr={[1, 1.2]}
        performance={{ min: 0.5 }}
        camera={{ position: [15, 10, 15], fov: 35 }}
        gl={{ 
          antialias: false, 
          alpha: true, 
          stencil: false,
          depth: true,
          powerPreference: "low-power",
          preserveDrawingBuffer: false
        }}
      >
        <Suspense fallback={<LoadingModel />}>
          <AdaptiveDpr pixelated />
          <AdaptiveEvents />
          <Preload all />
          
          <OrbitControls enableZoom={false} autoRotate={false} />
          
          {/* Photorealistic Architectural Lighting */}
          <ambientLight intensity={0.5} />
          <directionalLight 
            position={[25, 40, 15]} 
            intensity={3} 
            castShadow 
            shadow-mapSize={[1024, 1024]}
            shadow-camera-left={-20}
            shadow-camera-right={20}
            shadow-camera-top={20}
            shadow-camera-bottom={-20}
            shadow-bias={-0.0001}
            color="#FFF9F0" // Warm morning sunlight
          />
          <pointLight position={[-20, 15, -20]} intensity={2} color="#AACCFF" />
          <hemisphereLight intensity={0.6} color="#ffffff" groundColor="#244018" />

          <Float speed={2} rotationIntensity={0.3} floatIntensity={0.5}>
            <HouseModel scrollProgress={scrollProgress} houseColor={houseColor} />
          </Float>

          {/* Environment removed to eliminate reflections */}

          <ContactShadows 
            position={[0, -0.01, 0]} 
            opacity={0.6} 
            scale={20} 
            blur={2.5} 
            far={10} 
            resolution={256}
            color="#000000"
          />

          <Grid 
            infiniteGrid 
            fadeDistance={40} 
            fadeStrength={5} 
            cellSize={1} 
            sectionSize={5} 
            sectionColor={isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(158, 141, 130, 0.3)"} 
            cellColor={isDark ? "rgba(255, 255, 255, 0.05)" : "rgba(203, 213, 225, 0.1)"}
            position={[0, -0.1, 0]}
          />
        </Suspense>
      </Canvas>
    </div>
  );
});
