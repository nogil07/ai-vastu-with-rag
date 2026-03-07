import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, ArrowRight, Home, Map, Layers, Settings2 } from 'lucide-react';

interface PlanInputFormProps {
    onSuccess: () => void;
}

export default function PlanInputForm({ onSuccess }: PlanInputFormProps) {
    const [formData, setFormData] = useState({
        plotLength: 40,
        plotWidth: 30,
        plotShape: 'Rectangle',
        facing: 'East',
        floors: 'G+1',
        builtUpArea: 1000,
        buildingType: 'Independent house',
        bedrooms: 3,
        bathrooms: 2,
        kitchen: true,
        livingRoom: true,
        diningArea: true,
        poojaRoom: true,
        studyRoom: false,
        parking: true,
        vastuCompliance: 'High',
        layoutPreferences: 'Open Kitchen, Internal Stairs',
        style: 'Modern',
        outputFormat: '2D Floor Plan'
    });

    const [isGenerating, setIsGenerating] = useState(false);
    const [loadingText, setLoadingText] = useState("Initializing Vastu Engine...");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsGenerating(true);

        // Animate text states
        setTimeout(() => { setLoadingText("Running Strict RAG Agent..."); }, 2000);
        setTimeout(() => { setLoadingText("Drawing Architectural Blueprint..."); }, 10000);
        setTimeout(() => { setLoadingText("Compiling KPBR Report..."); }, 22000);

        try {
            const res = await fetch('http://127.0.0.1:5000/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await res.json();
            if (data.success) {
                onSuccess();
            } else {
                alert("Generation Error: " + data.error);
                setIsGenerating(false);
            }
        } catch (err) {
            alert("Network Error: Could not connect to Vasuttan Backend.");
            setIsGenerating(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const target = e.target as HTMLInputElement;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        setFormData({ ...formData, [target.name]: value });
    };

    const inputClasses = "w-full bg-bg-main/50 text-text-main border border-border-main/40 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-accent/50 focus:border-primary-accent transition-all hover:border-primary-accent/30";
    const labelClasses = "block text-xs font-bold text-text-muted uppercase tracking-wider mb-2";
    const sectionClasses = "bg-bg-surface/50 backdrop-blur-md p-6 md:p-8 rounded-3xl border border-white/5 dark:border-white/5 shadow-xl hover:shadow-2xl transition-all duration-500 group relative overflow-hidden";
    const sectionHeaderClasses = "flex items-center gap-3 border-b border-border-main/30 pb-4 mb-6 relative z-10";
    const checkboxLabelClasses = "flex items-center gap-3 cursor-pointer p-3 rounded-xl hover:bg-bg-main/30 transition-colors border border-transparent hover:border-border-main/20";

    return (
        <div className="relative w-full max-w-6xl mx-auto px-4 sm:px-6 z-10">

            <AnimatePresence>
                {isGenerating && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="fixed inset-0 z-[100] bg-bg-main/90 backdrop-blur-2xl flex flex-col items-center justify-center border border-border-main shadow-2xl"
                    >
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ repeat: Infinity, ease: "linear", duration: 3 }}
                            className="relative"
                        >
                            <div className="absolute inset-0 rounded-full blur-2xl bg-primary-accent/30 scale-150 animate-pulse"></div>
                            <Loader2 size={80} className="text-primary-accent relative z-10" />
                        </motion.div>
                        <h2 className="mt-8 text-3xl font-serif font-bold text-text-main tracking-tight animate-pulse text-center px-4">{loadingText}</h2>
                        <p className="mt-4 text-text-muted font-medium text-center px-4 max-w-md">Our AI is analyzing KPBR regulations and strict Vastu Shastra principles to generate your custom blueprint. Please wait approximately 30-45 seconds.</p>
                    </motion.div>
                )}
            </AnimatePresence>

            <form onSubmit={handleSubmit} className="glass-card rounded-[3rem] p-6 sm:p-10 md:p-14 shadow-2xl relative overflow-hidden border border-border-main/40">
                <div className="absolute inset-0 blueprint-grid opacity-10 pointer-events-none" />
                <div className="absolute top-0 right-0 w-96 h-96 bg-primary-accent/5 blur-[120px] rounded-full pointer-events-none" />
                <div className="absolute bottom-0 left-0 w-96 h-96 bg-ui-highlight/5 blur-[120px] rounded-full pointer-events-none" />

                <div className="relative z-10 mb-12 text-center max-w-2xl mx-auto">
                    <span className="inline-block px-4 py-1.5 rounded-full bg-bg-surface text-primary-accent text-[10px] font-bold tracking-[0.2em] uppercase mb-4 border border-border-main/50 shadow-sm">
                        AI Generator
                    </span>
                    <h2 className="text-4xl md:text-5xl font-serif font-bold text-text-main tracking-tight">Architectural Configuration</h2>
                    <p className="mt-4 text-text-muted">Define your plot, spatial requirements, and Vastu compliance preferences to instantly generate a professional-grade presentation board.</p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative z-10">

                    {/* Plot & Site Details */}
                    <div className={sectionClasses}>
                        <div className="absolute -right-10 -top-10 text-primary-accent/5 rotate-12 group-hover:rotate-0 transition-transform duration-700 pointer-events-none">
                            <Map size={160} />
                        </div>
                        <div className={sectionHeaderClasses}>
                            <div className="w-10 h-10 rounded-xl accent-gradient flex items-center justify-center text-text-inverse shadow-lg shadow-primary-accent/20">
                                <Map size={18} />
                            </div>
                            <h3 className="font-serif font-bold text-2xl text-text-main tracking-tight">Plot & Site Details</h3>
                        </div>

                        <div className="space-y-5 relative z-10">
                            <div className="flex flex-col sm:flex-row gap-5">
                                <div className="flex-1">
                                    <label className={labelClasses}>Length (ft/m)</label>
                                    <input required type="number" name="plotLength" value={formData.plotLength} onChange={handleChange} className={inputClasses} />
                                </div>
                                <div className="flex-1">
                                    <label className={labelClasses}>Width (ft/m)</label>
                                    <input required type="number" name="plotWidth" value={formData.plotWidth} onChange={handleChange} className={inputClasses} />
                                </div>
                            </div>
                            <div className="flex flex-col sm:flex-row gap-5">
                                <div className="flex-1">
                                    <label className={labelClasses}>Plot Shape</label>
                                    <select required name="plotShape" value={formData.plotShape} onChange={handleChange} className={inputClasses}>
                                        <option>Square</option>
                                        <option>Rectangle</option>
                                        <option>Irregular</option>
                                    </select>
                                </div>
                                <div className="flex-1">
                                    <label className={labelClasses}>Facing Direction</label>
                                    <select required name="facing" value={formData.facing} onChange={handleChange} className={inputClasses}>
                                        <option>East</option>
                                        <option>West</option>
                                        <option>North</option>
                                        <option>South</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Building Configuration */}
                    <div className={sectionClasses}>
                        <div className="absolute -right-10 -top-10 text-primary-accent/5 -rotate-12 group-hover:rotate-0 transition-transform duration-700 pointer-events-none">
                            <Home size={160} />
                        </div>
                        <div className={sectionHeaderClasses}>
                            <div className="w-10 h-10 rounded-xl accent-gradient flex items-center justify-center text-text-inverse shadow-lg shadow-primary-accent/20">
                                <Home size={18} />
                            </div>
                            <h3 className="font-serif font-bold text-2xl text-text-main tracking-tight">Building Profile</h3>
                        </div>

                        <div className="space-y-5 relative z-10">
                            <div className="flex flex-col sm:flex-row gap-5">
                                <div className="flex-1">
                                    <label className={labelClasses}>Number of Floors</label>
                                    <select required name="floors" value={formData.floors} onChange={handleChange} className={inputClasses}>
                                        <option>Ground</option>
                                        <option>G+1</option>
                                        <option>G+2</option>
                                    </select>
                                </div>
                                <div className="flex-1">
                                    <label className={labelClasses}>Built-up Area (sqft)</label>
                                    <input type="number" name="builtUpArea" value={formData.builtUpArea} onChange={handleChange} className={inputClasses} />
                                </div>
                            </div>
                            <div>
                                <label className={labelClasses}>Building Typology</label>
                                <select required name="buildingType" value={formData.buildingType} onChange={handleChange} className={inputClasses}>
                                    <option>Independent house</option>
                                    <option>Villa</option>
                                    <option>Duplex</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Room Requirements */}
                    <div className={sectionClasses}>
                        <div className="absolute -right-10 -top-10 text-primary-accent/5 rotate-12 group-hover:rotate-0 transition-transform duration-700 pointer-events-none">
                            <Layers size={160} />
                        </div>
                        <div className={sectionHeaderClasses}>
                            <div className="w-10 h-10 rounded-xl accent-gradient flex items-center justify-center text-text-inverse shadow-lg shadow-primary-accent/20">
                                <Layers size={18} />
                            </div>
                            <h3 className="font-serif font-bold text-2xl text-text-main tracking-tight">Spatial Program</h3>
                        </div>

                        <div className="space-y-6 relative z-10">
                            <div className="flex gap-5">
                                <div className="flex-1">
                                    <label className={labelClasses}>Bedrooms</label>
                                    <input required type="number" name="bedrooms" value={formData.bedrooms} onChange={handleChange} className={inputClasses} />
                                </div>
                                <div className="flex-1">
                                    <label className={labelClasses}>Bathrooms</label>
                                    <input required type="number" name="bathrooms" value={formData.bathrooms} onChange={handleChange} className={inputClasses} />
                                </div>
                            </div>

                            <div className="pt-2 border-t border-border-main/20">
                                <label className={labelClasses + " mb-3"}>Include Rooms</label>
                                <div className="grid grid-cols-2 gap-x-2 gap-y-1">
                                    <label className={checkboxLabelClasses}>
                                        <input type="checkbox" name="kitchen" checked={formData.kitchen} onChange={handleChange} className="w-4 h-4 rounded text-primary-accent bg-bg-main border-border-main focus:ring-primary-accent/50" />
                                        <span className="text-sm font-semibold text-text-main">Kitchen</span>
                                    </label>
                                    <label className={checkboxLabelClasses}>
                                        <input type="checkbox" name="livingRoom" checked={formData.livingRoom} onChange={handleChange} className="w-4 h-4 rounded text-primary-accent bg-bg-main border-border-main focus:ring-primary-accent/50" />
                                        <span className="text-sm font-semibold text-text-main">Living Room</span>
                                    </label>
                                    <label className={checkboxLabelClasses}>
                                        <input type="checkbox" name="diningArea" checked={formData.diningArea} onChange={handleChange} className="w-4 h-4 rounded text-primary-accent bg-bg-main border-border-main focus:ring-primary-accent/50" />
                                        <span className="text-sm font-semibold text-text-main">Dining Area</span>
                                    </label>
                                    <label className={checkboxLabelClasses}>
                                        <input type="checkbox" name="poojaRoom" checked={formData.poojaRoom} onChange={handleChange} className="w-4 h-4 rounded text-primary-accent bg-bg-main border-border-main focus:ring-primary-accent/50" />
                                        <span className="text-sm font-semibold text-text-main">Pooja Room</span>
                                    </label>
                                    <label className={checkboxLabelClasses}>
                                        <input type="checkbox" name="studyRoom" checked={formData.studyRoom} onChange={handleChange} className="w-4 h-4 rounded text-primary-accent bg-bg-main border-border-main focus:ring-primary-accent/50" />
                                        <span className="text-sm font-semibold text-text-main">Study / Office</span>
                                    </label>
                                    <label className={checkboxLabelClasses}>
                                        <input type="checkbox" name="parking" checked={formData.parking} onChange={handleChange} className="w-4 h-4 rounded text-primary-accent bg-bg-main border-border-main focus:ring-primary-accent/50" />
                                        <span className="text-sm font-semibold text-text-main">Parking / Garage</span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Vastu & Style */}
                    <div className={sectionClasses}>
                        <div className="absolute -right-10 -top-10 text-primary-accent/5 -rotate-12 group-hover:rotate-0 transition-transform duration-700 pointer-events-none">
                            <Settings2 size={160} />
                        </div>
                        <div className={sectionHeaderClasses}>
                            <div className="w-10 h-10 rounded-xl accent-gradient flex items-center justify-center text-text-inverse shadow-lg shadow-primary-accent/20">
                                <Settings2 size={18} />
                            </div>
                            <h3 className="font-serif font-bold text-2xl text-text-main tracking-tight">Design & Rules</h3>
                        </div>

                        <div className="space-y-5 relative z-10">
                            <div className="flex flex-col sm:flex-row gap-5">
                                <div className="flex-1">
                                    <label className={labelClasses}>Vastu Compliance</label>
                                    <select required name="vastuCompliance" value={formData.vastuCompliance} onChange={handleChange} className={inputClasses}>
                                        <option>High (Strict)</option>
                                        <option>Medium (Flexible)</option>
                                        <option>Low (Basic)</option>
                                    </select>
                                </div>
                                <div className="flex-1">
                                    <label className={labelClasses}>Architecture Style</label>
                                    <select required name="style" value={formData.style} onChange={handleChange} className={inputClasses}>
                                        <option>Modern Architecture</option>
                                        <option>Traditional / Heritage</option>
                                        <option>Minimalist Tropical</option>
                                    </select>
                                </div>
                            </div>
                            <div>
                                <label className={labelClasses}>Output Presentation</label>
                                <select required name="outputFormat" value={formData.outputFormat} onChange={handleChange} className={inputClasses}>
                                    <option>2D Architectural Floor Plan</option>
                                    <option>3D Aerial View</option>
                                </select>
                            </div>
                            <div>
                                <label className={labelClasses}>Specific Layout Preferences</label>
                                <textarea name="layoutPreferences" value={formData.layoutPreferences} onChange={handleChange} rows={2} className={`${inputClasses} resize-none mb-1`} placeholder="e.g. Open Kitchen, Double-height living..."></textarea>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="mt-14 flex justify-center relative z-20">
                    <button
                        type="submit"
                        disabled={isGenerating}
                        className="group relative px-10 py-5 accent-gradient text-text-inverse font-bold text-lg rounded-full shadow-2xl hover:-translate-y-1 active:scale-95 transition-all duration-300 overflow-hidden flex items-center gap-4 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                        <span className="relative z-10 tracking-wide uppercase text-sm">Synthesize Architectural Plan</span>
                        <ArrowRight className="relative z-10 group-hover:translate-x-1 transition-transform" strokeWidth={2.5} size={20} />
                    </button>
                </div>
            </form>
        </div>
    );
}
