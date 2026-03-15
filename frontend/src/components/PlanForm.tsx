import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, ChevronRight, ChevronLeft, Check, Info, RotateCcw, Loader2 } from 'lucide-react';

interface PlanFormProps {
  isOpen: boolean;
  onClose: () => void;
  onGenerationComplete?: () => void;
}

const steps = [
  { id: 1, title: 'Plot Details' },
  { id: 2, title: 'Configuration' },
  { id: 3, title: 'Requirements' },
  { id: 4, title: 'Preferences' },
];

const initialFormData = {
  // Step 1: Plot Details
  plotLength: '40',
  plotWidth: '30',
  plotShape: 'Rectangle',
  plotFacing: 'East',
  // Step 2: Building Configuration
  floors: 'G+1',
  builtUpArea: '1200',
  buildingType: 'Independent house',
  // Step 3: Room Requirements
  bedrooms: '3',
  bathrooms: '3',
  kitchen: true,
  livingRoom: true,
  diningArea: true,
  poojaRoom: true,
  studyRoom: false,
  parking: true,
  groundFloorBedroom: false,
  // Step 4: Vastu & Style
  vastuLevel: 'High',
  layoutPrefs: 'Open Kitchen, Internal Stairs',
  archStyle: 'Modern',
  outputFormat: '2D Floor Plan',
};

export const PlanForm: React.FC<PlanFormProps> = ({ isOpen, onClose, onGenerationComplete }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState(initialFormData);
  const [isLoading, setIsLoading] = useState(false);
  const [hoveredVastu, setHoveredVastu] = useState<string | null>(null);

  const vastuDescriptions: Record<string, string> = {
    Low: "Basic layout with minimal Vastu considerations. Focuses on space efficiency.",
    Medium: "Balanced approach. Key rooms like Kitchen and Master Bedroom follow Vastu.",
    High: "Strict adherence to Vastu principles for all rooms, entrances, and energy flow."
  };

  const resetForm = useCallback(() => {
    setFormData(initialFormData);
    setCurrentStep(1);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const nextStep = () => setCurrentStep(prev => Math.min(prev + 1, steps.length));
  const prevStep = () => setCurrentStep(prev => Math.max(prev - 1, 1));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch('https://ai-vastu-with-rag.onrender.com/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to generate plan');
      }

      onClose();
      if (onGenerationComplete) {
        onGenerationComplete();
      }
    } catch (error) {
      console.error('Error generating plan:', error);
      alert('Error: Could not connect to the generation server. Is it running?');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 overflow-hidden"
      >
        {/* Liquid Glass Backdrop */}
        <div className="absolute inset-0 bg-black/40 backdrop-blur-[40px]" onClick={onClose} />

        {/* Animated Background Blobs for Liquid Effect */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-30">
          <motion.div
            animate={{
              x: [0, 100, 0],
              y: [0, -50, 0],
              scale: [1, 1.2, 1]
            }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary-accent/20 rounded-full blur-[120px]"
          />
          <motion.div
            animate={{
              x: [0, -80, 0],
              y: [0, 100, 0],
              scale: [1, 1.1, 1]
            }}
            transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
            className="absolute bottom-[-10%] right-[-10%] w-[60%] h-[60%] bg-blue-500/10 rounded-full blur-[120px]"
          />
        </div>

        {/* Modal Container - Liquid Glass Styling */}
        <motion.div
          initial={{ scale: 0.95, opacity: 0, y: 30 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.95, opacity: 0, y: 30 }}
          className="relative w-full max-w-4xl bg-white/5 dark:bg-black/20 backdrop-blur-3xl rounded-[3rem] shadow-[0_0_80px_rgba(0,0,0,0.2)] overflow-hidden border border-white/20 flex flex-col max-h-[90vh] ring-1 ring-white/10"
        >
          {/* Header */}
          <div className="p-8 flex items-center justify-between bg-white/5">
            <div>
              <h2 className="text-3xl font-serif font-bold text-white tracking-tight">Architectural Blueprint</h2>
              <p className="text-sm text-white/60 font-medium">Define your vision for the perfect Vastu home.</p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={resetForm}
                className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 transition-all text-white/70 hover:text-white text-xs font-bold uppercase tracking-widest"
                title="Reset Form"
              >
                <RotateCcw size={14} />
                <span className="hidden sm:inline">Reset</span>
              </button>
              <button
                onClick={onClose}
                className="p-3 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 transition-all text-white/70 hover:text-white"
              >
                <X size={20} />
              </button>
            </div>
          </div>

          {/* Stepper */}
          {!isLoading && (
            <div className="px-8 py-6 bg-white/5 flex justify-between items-center">
              {steps.map((step) => (
                <div key={step.id} className="flex items-center gap-3">
                  <motion.div
                    animate={{
                      backgroundColor: currentStep >= step.id ? 'var(--color-primary-accent, #C7A15E)' : 'rgba(255,255,255,0.05)',
                      borderColor: currentStep >= step.id ? 'transparent' : 'rgba(255,255,255,0.1)'
                    }}
                    className={`w-10 h-10 rounded-2xl flex items-center justify-center text-sm font-bold transition-all border shadow-inner ${currentStep >= step.id ? 'text-black' : 'text-white/40'
                      }`}
                  >
                    {currentStep > step.id ? <Check size={18} strokeWidth={3} /> : step.id}
                  </motion.div>
                  <span className={`text-[10px] font-black uppercase tracking-[0.2em] hidden md:block ${currentStep >= step.id ? 'text-white' : 'text-white/30'
                    }`}>
                    {step.title}
                  </span>
                  {step.id < steps.length && <div className="w-12 h-px bg-white/10 hidden md:block" />}
                </div>
              ))}
            </div>
          )}

          {/* Form Content */}
          <div
            className="flex-1 overflow-y-auto p-10 custom-scrollbar bg-gradient-to-b from-transparent to-white/[0.02]"
            data-lenis-prevent
          >
            <AnimatePresence mode="wait">
              {isLoading ? (
                <motion.div
                  key="processing"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center justify-center min-h-[50vh] text-center space-y-6"
                  style={{ willChange: 'opacity' }}
                >
                  <Loader2 className="w-12 h-12 mx-auto text-primary-accent animate-spin" />
                  <div className="space-y-2">
                    <p className="text-white font-bold tracking-tight">AI RAG Engine Processing</p>
                    <div className="w-48 h-1.5 bg-white/10 rounded-full mx-auto overflow-hidden">
                      <motion.div
                        initial={{ x: '-100%' }}
                        animate={{ x: '100%' }}
                        transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                        className="w-full h-full bg-primary-accent"
                      />
                    </div>
                  </div>
                  <div className="text-[10px] font-mono text-white/50 uppercase tracking-[0.2em] font-bold">
                    Retrieving KPBR Rules • Analyzing Vastu Grids • Optimizing Layout
                  </div>
                </motion.div>
              ) : (
                <motion.form
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  onSubmit={handleSubmit}
                  className="space-y-10"
                >
                  {currentStep === 1 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="grid grid-cols-1 md:grid-cols-2 gap-8"
                    >
                      <div className="space-y-3">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Plot Length (ft)</label>
                        <input
                          type="number" name="plotLength" value={formData.plotLength} onChange={handleChange}
                          className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all placeholder:text-white/20"
                        />
                      </div>
                      <div className="space-y-3">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Plot Width (ft)</label>
                        <input
                          type="number" name="plotWidth" value={formData.plotWidth} onChange={handleChange}
                          className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all placeholder:text-white/20"
                        />
                      </div>
                      <div className="space-y-3">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Plot Shape</label>
                        <select name="plotShape" value={formData.plotShape} onChange={handleChange}
                          className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all appearance-none cursor-pointer"
                        >
                          <option className="bg-zinc-900">Rectangle</option>
                          <option className="bg-zinc-900">Square</option>
                          <option className="bg-zinc-900">Irregular</option>
                        </select>
                      </div>
                      <div className="space-y-3">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Facing Direction</label>
                        <select name="plotFacing" value={formData.plotFacing} onChange={handleChange}
                          className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all appearance-none cursor-pointer"
                        >
                          <option className="bg-zinc-900">North</option>
                          <option className="bg-zinc-900">East</option>
                          <option className="bg-zinc-900">South</option>
                          <option className="bg-zinc-900">West</option>
                        </select>
                      </div>
                    </motion.div>
                  )}

                  {currentStep === 2 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="grid grid-cols-1 md:grid-cols-2 gap-8"
                    >
                      <div className="space-y-3">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Number of Floors</label>
                        <select name="floors" value={formData.floors} onChange={handleChange}
                          className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all appearance-none cursor-pointer"
                        >
                          <option className="bg-zinc-900">Ground</option>
                          <option className="bg-zinc-900">G+1</option>
                          <option className="bg-zinc-900">G+2</option>
                          <option className="bg-zinc-900">G+3</option>
                        </select>
                      </div>
                      <div className="space-y-3">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Built-up Area (sqft)</label>
                        <input
                          type="number" name="builtUpArea" value={formData.builtUpArea} onChange={handleChange}
                          className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all placeholder:text-white/20"
                        />
                      </div>
                      <div className="col-span-full space-y-4">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Type of Building</label>
                        <div className="grid grid-cols-3 gap-4">
                          {['Independent house', 'Villa', 'Duplex'].map(type => (
                            <button
                              key={type}
                              type="button"
                              onClick={() => setFormData(prev => ({ ...prev, buildingType: type }))}
                              className={`px-6 py-4 rounded-2xl border text-xs font-black uppercase tracking-widest transition-all ${formData.buildingType === type
                                ? 'bg-primary-accent border-primary-accent text-black shadow-[0_0_20px_rgba(199,161,94,0.3)]'
                                : 'bg-white/5 border-white/10 text-white/50 hover:border-white/30 hover:text-white'
                                }`}
                            >
                              {type}
                            </button>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {currentStep === 3 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="space-y-10"
                    >
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="space-y-3">
                          <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Bedrooms</label>
                          <input type="number" name="bedrooms" value={formData.bedrooms} onChange={handleChange} className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white" />
                        </div>
                        <div className="space-y-3">
                          <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Bathrooms</label>
                          <input type="number" name="bathrooms" value={formData.bathrooms} onChange={handleChange} className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white" />
                        </div>
                      </div>

                      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                        {[
                          { id: 'kitchen', label: 'Kitchen' },
                          { id: 'livingRoom', label: 'Living' },
                          { id: 'diningArea', label: 'Dining' },
                          { id: 'poojaRoom', label: 'Pooja' },
                          { id: 'studyRoom', label: 'Study' },
                          { id: 'parking', label: 'Parking' },
                        ].map(item => (
                          <label key={item.id} className={`flex items-center justify-between p-5 rounded-2xl border cursor-pointer transition-all ${(formData as any)[item.id] ? 'bg-primary-accent/20 border-primary-accent text-primary-accent shadow-inner' : 'bg-white/5 border-white/10 text-white/30'
                            }`}>
                            <span className="text-[10px] font-black uppercase tracking-widest">{item.label}</span>
                            <div className={`w-5 h-5 rounded-lg border flex items-center justify-center transition-all ${(formData as any)[item.id] ? 'bg-primary-accent border-primary-accent' : 'bg-transparent border-white/20'
                              }`}>
                              {(formData as any)[item.id] && <Check size={12} className="text-black" strokeWidth={4} />}
                            </div>
                            <input
                              type="checkbox"
                              name={item.id}
                              checked={(formData as any)[item.id]}
                              onChange={handleChange}
                              className="hidden"
                            />
                          </label>
                        ))}
                      </div>

                      <div className="p-6 bg-white/5 rounded-[2rem] border border-white/10 flex items-start gap-5">
                        <div className="w-12 h-12 rounded-2xl bg-primary-accent/10 flex items-center justify-center text-primary-accent shrink-0">
                          <Info size={24} />
                        </div>
                        <div className="space-y-3">
                          <p className="text-sm font-bold text-white">Ground Floor Preference</p>
                          <div className="flex items-center gap-8">
                            <label className="flex items-center gap-3 text-xs font-bold text-white/50 cursor-pointer group">
                              <div className={`w-5 h-5 rounded-full border flex items-center justify-center transition-all ${formData.groundFloorBedroom ? 'border-primary-accent bg-primary-accent' : 'border-white/20'}`}>
                                {formData.groundFloorBedroom && <div className="w-2 h-2 bg-black rounded-full" />}
                              </div>
                              <input type="radio" name="groundFloorBedroom" checked={formData.groundFloorBedroom} onChange={() => setFormData(p => ({ ...p, groundFloorBedroom: true }))} className="hidden" />
                              <span className={formData.groundFloorBedroom ? 'text-white' : ''}>Yes, GF Bedrooms</span>
                            </label>
                            <label className="flex items-center gap-3 text-xs font-bold text-white/50 cursor-pointer group">
                              <div className={`w-5 h-5 rounded-full border flex items-center justify-center transition-all ${!formData.groundFloorBedroom ? 'border-primary-accent bg-primary-accent' : 'border-white/20'}`}>
                                {!formData.groundFloorBedroom && <div className="w-2 h-2 bg-black rounded-full" />}
                              </div>
                              <input type="radio" name="groundFloorBedroom" checked={!formData.groundFloorBedroom} onChange={() => setFormData(p => ({ ...p, groundFloorBedroom: false }))} className="hidden" />
                              <span className={!formData.groundFloorBedroom ? 'text-white' : ''}>No</span>
                            </label>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {currentStep === 4 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="space-y-10"
                    >
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                        <div className="space-y-4">
                          <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Vastu Compliance Level</label>
                          <div className="flex gap-2 p-1.5 bg-white/5 rounded-2xl border border-white/10">
                            {['Low', 'Medium', 'High'].map(level => (
                              <button
                                key={level}
                                type="button"
                                onMouseEnter={() => setHoveredVastu(level)}
                                onMouseLeave={() => setHoveredVastu(null)}
                                onClick={() => setFormData(p => ({ ...p, vastuLevel: level }))}
                                className={`flex-1 py-3 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${formData.vastuLevel === level
                                  ? 'bg-primary-accent text-black shadow-lg'
                                  : 'text-white/40 hover:text-white/70'
                                  }`}
                              >
                                {level}
                              </button>
                            ))}
                          </div>
                          <AnimatePresence mode="wait">
                            {(hoveredVastu || formData.vastuLevel) && (
                              <motion.p
                                key={hoveredVastu || formData.vastuLevel}
                                initial={{ opacity: 0, y: -5 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -5 }}
                                className="text-[10px] text-primary-accent/80 font-medium px-2 leading-relaxed"
                              >
                                {vastuDescriptions[hoveredVastu || formData.vastuLevel]}
                              </motion.p>
                            )}
                          </AnimatePresence>
                        </div>

                        <div className="space-y-4">
                          <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Architectural Style</label>
                          <select name="archStyle" value={formData.archStyle} onChange={handleChange} className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white appearance-none cursor-pointer">
                            <option className="bg-zinc-900">Modern</option>
                            <option className="bg-zinc-900">Traditional</option>
                            <option className="bg-zinc-900">Minimal</option>
                          </select>
                        </div>
                      </div>

                      <div className="space-y-4">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Layout Preferences</label>
                        <textarea
                          name="layoutPrefs" value={formData.layoutPrefs} onChange={handleChange}
                          placeholder="e.g., Open kitchen, stairs inside..."
                          className="w-full bg-white/5 border border-white/10 rounded-[2rem] px-8 py-6 text-white h-32 resize-none focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all placeholder:text-white/20"
                        />
                      </div>

                      <div className="space-y-4">
                        <label className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50 ml-1">Output Format</label>
                        <div className="flex gap-6">
                          {['2D Floor Plan', '3D View'].map(format => (
                            <label key={format} className={`flex-1 flex items-center gap-4 p-6 rounded-[2rem] border cursor-pointer transition-all ${formData.outputFormat === format ? 'bg-primary-accent/20 border-primary-accent text-primary-accent' : 'bg-white/5 border-white/10 text-white/30'
                              }`}>
                              <div className={`w-6 h-6 rounded-full border flex items-center justify-center transition-all ${formData.outputFormat === format ? 'border-primary-accent bg-primary-accent' : 'border-white/20'}`}>
                                {formData.outputFormat === format && <div className="w-2.5 h-2.5 bg-black rounded-full" />}
                              </div>
                              <input type="radio" name="outputFormat" checked={formData.outputFormat === format} onChange={() => setFormData(p => ({ ...p, outputFormat: format }))} className="hidden" />
                              <span className="text-sm font-black uppercase tracking-widest">{format}</span>
                            </label>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  )}
                </motion.form>
              )}
            </AnimatePresence>
          </div>

          {/* Footer */}
          {!isLoading && (
            <div className="p-10 bg-white/5 flex items-center justify-between">
              <button
                type="button"
                onClick={prevStep}
                disabled={currentStep === 1}
                className={`flex items-center gap-3 px-8 py-4 rounded-2xl font-black uppercase tracking-widest text-[10px] transition-all ${currentStep === 1 ? 'opacity-0 pointer-events-none' : 'text-white/50 hover:text-white hover:bg-white/5'
                  }`}
              >
                <ChevronLeft size={18} />
                Previous
              </button>

              {currentStep < steps.length ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="flex items-center gap-3 bg-primary-accent text-black px-10 py-4 rounded-2xl font-black uppercase tracking-widest text-[10px] hover:opacity-90 transition-all shadow-[0_0_30px_rgba(199,161,94,0.3)] active:scale-95 group"
                >
                  Next Step
                  <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
                </button>
              ) : (
                <button
                  type="submit"
                  onClick={handleSubmit}
                  disabled={isLoading}
                  className="flex items-center gap-3 bg-primary-accent text-black px-12 py-4 rounded-2xl font-black uppercase tracking-widest text-[10px] hover:opacity-90 transition-all shadow-[0_0_40px_rgba(199,161,94,0.4)] active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      Generate Vision
                      <Check size={18} strokeWidth={3} />
                    </>
                  )}
                </button>
              )}
            </div>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};
