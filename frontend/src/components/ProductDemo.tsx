import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Play, CheckCircle2, Loader2 } from 'lucide-react';

export const ProductDemo = React.memo(() => {
  const [step, setStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  const startDemo = useCallback(() => {
    setStep(1);
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setStep(2);
    }, 3000);
  }, []);

  const resetDemo = useCallback(() => {
    setStep(0);
  }, []);

  return (
    <div className="w-full max-w-5xl mx-auto px-4 py-20">
      <div className="glass-card rounded-3xl overflow-hidden shadow-2xl border border-border-main/40">
        <div className="bg-bg-surface px-6 py-3 flex items-center justify-between border-b border-border-main/20">
          <div className="flex gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <div className="w-3 h-3 rounded-full bg-green-500" />
          </div>
          <div className="text-text-muted text-xs font-mono font-bold tracking-widest">AI-VASTU-PLANNER-V1.0</div>
        </div>

        <div className="p-6 md:p-12 grid md:grid-cols-3 gap-8 md:gap-12 bg-bg-main/30 backdrop-blur-md">
          {/* Controls */}
          <div className="space-y-6">
            <h3 className="text-xl font-serif font-bold text-text-main">Input Parameters</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-xs uppercase tracking-wider text-text-muted mb-2 font-bold">Plot Size (sqft)</label>
                <input
                  type="text"
                  disabled={step > 0}
                  placeholder="e.g. 1200"
                  className="w-full px-4 py-2.5 rounded-xl border border-border-main/30 bg-bg-main/50 focus:outline-none focus:ring-2 focus:ring-primary-accent/50 text-sm text-text-main placeholder-text-muted/50"
                />
              </div>
              <div>
                <label className="block text-xs uppercase tracking-wider text-text-muted mb-2 font-bold">Facing Direction</label>
                <select disabled={step > 0} className="w-full px-4 py-2.5 rounded-xl border border-border-main/30 bg-bg-main/50 focus:outline-none focus:ring-2 focus:ring-primary-accent/50 text-sm text-text-main">
                  <option>North</option>
                  <option>East</option>
                  <option>South</option>
                  <option>West</option>
                </select>
              </div>
              <div>
                <label className="block text-xs uppercase tracking-wider text-text-muted mb-2 font-bold">Floors</label>
                <input
                  type="number"
                  disabled={step > 0}
                  defaultValue={1}
                  className="w-full px-4 py-2.5 rounded-xl border border-border-main/30 bg-bg-main/50 focus:outline-none focus:ring-2 focus:ring-primary-accent/50 text-sm text-text-main"
                />
              </div>
              <button
                onClick={startDemo}
                disabled={step > 0}
                className="w-full py-3.5 accent-gradient text-text-inverse rounded-xl font-bold hover:opacity-90 transition-colors flex items-center justify-center gap-2 active:scale-95 shadow-xl shadow-primary-accent/20"
              >
                {step === 0 ? (
                  <>
                    <Play size={16} fill="currentColor" />
                    Generate Plan
                  </>
                ) : (
                  <>
                    <CheckCircle2 size={16} />
                    Processing...
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Visualization Area */}
          <div className="md:col-span-2 relative min-h-[300px] md:min-h-[400px] bg-bg-surface/50 backdrop-blur-sm rounded-3xl border border-dashed border-border-main flex items-center justify-center overflow-hidden shadow-inner">
            <AnimatePresence mode="wait">
              {step === 0 && (
                <motion.div
                  key="idle"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-center space-y-4"
                  style={{ willChange: 'opacity' }}
                >
                  <div className="w-20 h-20 mx-auto border-2 border-dashed border-primary-accent/30 rounded-full flex items-center justify-center">
                    <div className="w-12 h-12 bg-primary-accent/10 rounded-full" />
                  </div>
                  <p className="text-text-muted font-serif italic text-sm">Awaiting architectural parameters...</p>
                </motion.div>
              )}

              {isProcessing && (
                <motion.div
                  key="processing"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-center space-y-6"
                  style={{ willChange: 'opacity' }}
                >
                  <Loader2 className="w-12 h-12 mx-auto text-primary-accent animate-spin" />
                  <div className="space-y-4">
                    <p className="text-text-main font-bold tracking-tight text-lg">AI RAG Engine Processing</p>
                    <div className="w-56 h-1.5 bg-bg-main rounded-full mx-auto overflow-hidden shadow-inner relative border border-border-main/30">
                      <motion.div
                        initial={{ x: '-100%' }}
                        animate={{ x: '100%' }}
                        transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                        className="w-full h-full bg-primary-accent"
                      />
                    </div>
                  </div>
                  <div className="text-[10px] font-mono text-text-muted uppercase tracking-[0.2em] font-bold">
                    Retrieving KPBR Rules • Analyzing Vastu Grids • Optimizing Layout
                  </div>
                </motion.div>
              )}

              {step === 2 && !isProcessing && (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="w-full h-full p-8 flex flex-col items-center justify-center"
                  style={{ willChange: 'opacity, transform' }}
                >
                  <div className="relative w-full max-w-md aspect-square bg-bg-surface shadow-2xl border border-border-main/50 p-6 rounded-2xl">
                    {/* Blueprint Drawing Animation */}
                    <svg viewBox="0 0 100 100" className="w-full h-full text-text-main shadow-sm">
                      {/* Outer Walls */}
                      <motion.rect
                        x="10" y="10" width="80" height="80"
                        fill="none" stroke="currentColor" strokeWidth="1.5"
                        initial={{ pathLength: 0 }}
                        animate={{ pathLength: 1 }}
                        transition={{ duration: 1 }}
                      />
                      {/* Internal Walls */}
                      <motion.line x1="10" y1="40" x2="50" y2="40" stroke="currentColor" strokeWidth="0.8" className="opacity-60" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ delay: 0.5 }} />
                      <motion.line x1="50" y1="10" x2="50" y2="60" stroke="currentColor" strokeWidth="0.8" className="opacity-60" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ delay: 0.7 }} />
                      <motion.line x1="50" y1="60" x2="90" y2="60" stroke="currentColor" strokeWidth="0.8" className="opacity-60" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ delay: 0.9 }} />

                      {/* Labels */}
                      <motion.text x="20" y="30" fontSize="3.5" fontWeight="bold" fill="currentColor" className="opacity-80" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 }}>Living Room</motion.text>
                      <motion.text x="65" y="35" fontSize="3.5" fontWeight="bold" fill="currentColor" className="opacity-80" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.7 }}>Kitchen</motion.text>
                      <motion.text x="25" y="70" fontSize="3.5" fontWeight="bold" fill="currentColor" className="opacity-80" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.9 }}>Master Bedroom</motion.text>
                      <motion.text x="65" y="80" fontSize="3.5" fontWeight="bold" fill="currentColor" className="opacity-80" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.1 }}>Pooja Room</motion.text>
                    </svg>

                    <div className="absolute top-6 right-6 bg-bg-main/80 backdrop-blur-sm text-primary-accent px-4 py-2 rounded-xl text-[10px] font-black border border-primary-accent/30 shadow-md uppercase tracking-widest">
                      VASTU SCORE: 98/100
                    </div>
                  </div>
                  <motion.button
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 2.5 }}
                    onClick={resetDemo}
                    className="mt-8 text-text-muted hover:text-primary-accent text-sm font-bold uppercase tracking-widest transition-colors flex items-center gap-2"
                  >
                    Reset Demo Simulation
                  </motion.button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
});
