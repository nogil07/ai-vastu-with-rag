import React, { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import ReactMarkdown from 'react-markdown';
import { Download, Mail, ArrowLeft, Loader2 } from 'lucide-react';
import { EmailModal } from './EmailModal';

interface ResultViewProps {
    onBack: () => void;
}

export const ResultView: React.FC<ResultViewProps> = ({ onBack }) => {
    const [reportMarkdown, setReportMarkdown] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [isEmailModalOpen, setIsEmailModalOpen] = useState(false);

    useEffect(() => {
        // Fetch the report
        fetch('http://localhost:8080/api/result/report')
            .then(res => res.json())
            .then(data => {
                setReportMarkdown(data.markdown || '');
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch report:", err);
                setReportMarkdown("Failed to load the report. Please try again or verify the backend server.");
                setLoading(false);
            });
    }, []);

    const handleDownload = () => {
        window.open('http://localhost:8080/api/result/pdf', '_blank');
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center pt-24 pb-12 relative z-10 transition-colors duration-700">
                <div className="flex flex-col items-center gap-4 text-text-main">
                    <Loader2 size={48} className="animate-spin text-primary-accent" />
                    <p className="font-serif font-bold text-xl tracking-tight">Processing your Vastu Plan...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 relative z-10 transition-colors duration-700">
            <div className="max-w-7xl mx-auto">
                <motion.button
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    onClick={onBack}
                    className="flex items-center gap-2 text-text-muted hover:text-text-main transition-colors mb-8 font-bold uppercase tracking-widest text-xs"
                >
                    <ArrowLeft size={16} />
                    Back to Home
                </motion.button>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col md:flex-row items-start justify-between gap-6 mb-12"
                >
                    <div className="max-w-2xl">
                        <div className="flex items-center gap-3 mb-6">
                            <span className="relative flex h-3 w-3">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-accent opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-primary-accent"></span>
                            </span>
                            <span className="text-primary-accent text-[10px] font-black tracking-[0.2em] uppercase">
                                Generation Complete
                            </span>
                        </div>
                        <h1 className="text-5xl sm:text-7xl font-serif font-medium tracking-tight text-text-main leading-tight">
                            Your Vastu <br className="hidden sm:block" />
                            <span className="italic text-text-muted">Blueprint</span>
                        </h1>
                    </div>
                    <div className="flex flex-col sm:flex-row items-center gap-4 w-full md:w-auto mt-6 md:mt-0">
                        <button
                            onClick={handleDownload}
                            className="flex-1 md:flex-none flex items-center justify-center gap-2 bg-bg-surface border border-border-main text-text-main px-6 py-3 rounded-xl font-bold hover:bg-bg-main transition-all shadow-sm active:scale-95"
                        >
                            <Download size={18} />
                            Download PDF
                        </button>
                        <button
                            onClick={() => setIsEmailModalOpen(true)}
                            className="flex-1 md:flex-none flex items-center justify-center gap-2 bg-primary-accent text-btn-text px-6 py-3 rounded-xl font-bold hover:opacity-90 transition-all shadow-lg shadow-primary-accent/20 active:scale-95"
                        >
                            <Mail size={18} />
                            Email Report
                        </button>
                    </div>
                </motion.div>

                <div className="grid lg:grid-cols-12 gap-10 items-start">
                    {/* Left Column: Image */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="lg:col-span-7 sticky top-24"
                    >
                        <div className="glass-card rounded-[2rem] p-2 sm:p-4 overflow-hidden border border-border-main/50 shadow-2xl relative group">
                            <div className="absolute inset-0 bg-primary-accent/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                            <img
                                src="http://localhost:8080/api/result/image"
                                alt="Generated Vastu Plan"
                                className="w-full h-auto rounded-[1.5rem] object-cover shadow-sm bg-white"
                                onError={(e) => {
                                    (e.target as HTMLImageElement).src = 'https://placehold.co/800x600/1a1a1a/cccccc?text=Image+Generating/Unavailable';
                                }}
                            />
                        </div>
                    </motion.div>

                    {/* Right Column: Markdown Report */}
                    <motion.div
                        initial={{ opacity: 0, x: 30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                        className="lg:col-span-5"
                    >
                        <div className="glass-card rounded-[2rem] p-8 sm:p-10 border border-border-main/50 text-text-main leading-relaxed shadow-xl max-w-none hover:shadow-2xl transition-shadow duration-500">
                            <div className="prose prose-slate dark:prose-invert max-w-none 
                prose-h1:font-serif prose-h1:text-4xl prose-h1:font-medium prose-h1:mb-8 prose-h1:text-text-main prose-h1:tracking-tight
                prose-h2:font-serif prose-h2:text-2xl prose-h2:font-medium prose-h2:text-primary-accent prose-h2:border-b-2 prose-h2:border-primary-accent/20 prose-h2:pb-4 prose-h2:mt-12 prose-h2:tracking-wide
                prose-h3:font-sans prose-h3:text-sm prose-h3:uppercase prose-h3:tracking-widest prose-h3:font-bold prose-h3:text-text-main prose-h3:mt-8
                prose-p:text-text-muted prose-p:leading-loose prose-p:text-sm
                prose-ul:text-text-muted prose-ul:text-sm prose-li:marker:text-primary-accent prose-li:leading-relaxed
                prose-strong:text-text-main prose-strong:font-bold
              ">
                                <ReactMarkdown>{reportMarkdown}</ReactMarkdown>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>

            <EmailModal
                isOpen={isEmailModalOpen}
                onClose={() => setIsEmailModalOpen(false)}
            />
        </div>
    );
};
