import React, { useEffect, useRef, useState } from 'react';

export default function AvatarWidget() {
  const ref = useRef<HTMLDivElement | null>(null);
  const dragging = useRef(false);
  const pointerId = useRef<number | null>(null);
  const start = useRef({ x: 0, y: 0, ox: 0, oy: 0 });

  // Initial position at bottom-right
  const [pos, setPos] = useState({
    x: window.innerWidth - 180,
    y: window.innerHeight - 180
  });

  // Update position on window resize to keep it in the bottom right
  useEffect(() => {
    const handleResize = () => {
      if (!dragging.current) {
        setPos({
          x: window.innerWidth - 180,
          y: window.innerHeight - 180
        });
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  function onPointerDown(e: React.PointerEvent) {
    const el = ref.current!;
    try { el.setPointerCapture(e.pointerId); } catch { }
    dragging.current = true;
    pointerId.current = e.pointerId;
    start.current = { x: e.clientX, y: e.clientY, ox: pos.x, oy: pos.y };
  }

  function onPointerMove(e: React.PointerEvent) {
    if (!dragging.current || pointerId.current !== e.pointerId) return;
    const dx = e.clientX - start.current.x;
    const dy = e.clientY - start.current.y;
    const nx = start.current.ox + dx;
    const ny = start.current.oy + dy;

    const clampedX = Math.max(10, Math.min(window.innerWidth - 170, nx));
    const clampedY = Math.max(10, Math.min(window.innerHeight - 170, ny));

    setPos({ x: clampedX, y: clampedY });
  }

  function onPointerUp(e: React.PointerEvent) {
    const el = ref.current!;
    try { el.releasePointerCapture(e.pointerId); } catch { }
    dragging.current = false;
    pointerId.current = null;
  }

  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(err => {
        console.warn("Video autoplay failed:", err);
      });
    }
  }, []);

  return (
    <div
      ref={ref}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={onPointerUp}
      style={{ left: pos.x, top: pos.y }}
      className="fixed z-50 w-40 h-40 touch-none select-none cursor-grab active:cursor-grabbing transition-shadow"
    >
      <div className="relative w-full h-full group">
        <div className="absolute inset-0 rounded-full overflow-hidden shadow-2xl border-4 border-primary-accent/30 bg-transparent">
          <video
            ref={videoRef}
            src="/vasuttan2.mp4"
            autoPlay
            loop
            muted
            playsInline
            onEnded={() => {
              if (videoRef.current) videoRef.current.play();
            }}
            className="w-full h-full object-cover scale-110 translate-y-2"
          />
        </div>
        {/* Subtle glow effect */}
        <div className="absolute -inset-2 bg-primary-accent/10 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
      </div>
    </div>
  );
}
