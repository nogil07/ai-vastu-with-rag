import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileDown, Mail, Download, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface ReportViewProps {
    onReset: () => void;
}

export default function ReportView({ onReset }: ReportViewProps) {
    const [reportText, setReportText] = useState<string>('Loading report...');
    const [showEmailModal, setShowEmailModal] = useState(false);
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [isSending, setIsSending] = useState(false);

    React.useEffect(() => {
        fetch('http://127.0.0.1:5000/api/report')
            .then(r => r.json())
            .then(d => {
                if (d.content) setReportText(d.content);
                else setReportText('Failed to load report content.');
            })
            .catch(e => setReportText('Network error loading report.'));
    }, []);

    const handleDownload = () => {
        window.location.href = 'http://127.0.0.1:5000/api/download';
    };

    const handleEmailSend = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSending(true);
        try {
            const res = await fetch('http://127.0.0.1:5000/api/email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, name })
            });
            const data = await res.json();
            if (data.success) {
                alert('Email sent successfully!');
                setShowEmailModal(false);
            } else {
                alert('Failed to send email: ' + data.error);
            }
        } catch (err) {
            alert('Error sending email.');
        } finally {
            setIsSending(false);
        }
    };

    return (
        <div className="min-h-screen bg-bg-main pt-20 px-4 md:px-8 pb-12 transition-colors duration-700">
            <div className="max-w-7xl mx-auto space-y-8">

                {/* Header */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <h1 className="text-3xl font-serif font-bold text-text-main">Your Architectural Floor Plan</h1>
                        <p className="text-text-muted mt-1 font-medium">Generated based on strict KPBR & Vastu principles.</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <button onClick={onReset} className="px-5 py-2.5 border border-border-main rounded-xl text-text-main hover:bg-bg-surface transition-all font-bold shadow-sm text-sm active:scale-95">
                            Generate New Plan
                        </button>
                        <button onClick={handleDownload} className="px-5 py-2.5 accent-gradient text-text-inverse rounded-xl hover:opacity-90 transition-all shadow-xl font-bold text-sm flex items-center gap-2 active:scale-95">
                            <FileDown size={18} /> Download PDF
                        </button>
                        <button onClick={() => setShowEmailModal(true)} className="px-5 py-2.5 bg-bg-surface border border-border-main text-text-main rounded-xl hover:bg-border-main/20 transition-all shadow-sm font-bold text-sm flex items-center gap-2 active:scale-95">
                            <Mail size={18} /> Email Report
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Image Panel */}
                    <div className="glass-card rounded-3xl p-8 flex flex-col items-center border border-border-main/50 shadow-2xl">
                        <h2 className="text-2xl font-serif font-bold text-text-main mb-6 w-full border-b border-border-main/30 pb-3">2D Architectural Layout</h2>
                        <div className="relative w-full aspect-square md:aspect-[4/3] bg-bg-surface rounded-2xl overflow-hidden shadow-inner border border-border-main/20 flex items-center justify-center p-2">
                            <img
                                src="http://127.0.0.1:5000/api/image"
                                alt="Generated Floor Plan"
                                className="w-full h-full object-contain drop-shadow-sm rounded-xl"
                                onError={(e) => (e.currentTarget.style.display = 'none')}
                            />
                        </div>
                    </div>

                    {/* Report Panel */}
                    <div className="glass-card rounded-3xl p-8 lg:h-[80vh] flex flex-col border border-border-main/50 shadow-2xl">
                        <h2 className="text-2xl font-serif font-bold text-text-main mb-6 w-full border-b border-border-main/30 pb-3">Compliance Report</h2>
                        <div className="flex-1 overflow-y-auto prose prose-sm md:prose-base prose-headings:text-text-main prose-headings:font-serif prose-p:text-text-muted prose-strong:text-text-main prose-ul:text-text-muted prose-a:text-primary-accent pr-4 font-medium custom-scrollbar">
                            <ReactMarkdown>{reportText}</ReactMarkdown>
                        </div>
                    </div>
                </div>
            </div>

            {/* Email Modal */}
            <AnimatePresence>
                {showEmailModal && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 bg-black/60 backdrop-blur-md flex items-center justify-center p-4"
                    >
                        <motion.div
                            initial={{ scale: 0.95, opacity: 0, y: 20 }}
                            animate={{ scale: 1, opacity: 1, y: 0 }}
                            exit={{ scale: 0.95, opacity: 0, y: 20 }}
                            className="bg-bg-surface w-full max-w-md rounded-3xl shadow-2xl overflow-hidden border border-border-main/50"
                        >
                            <div className="p-6 border-b border-border-main/30 flex justify-between items-center bg-bg-main/50 backdrop-blur-sm">
                                <h3 className="text-xl font-serif font-bold text-text-main flex items-center gap-3"><Mail className="text-primary-accent" size={20} /> Send Report</h3>
                                <button onClick={() => setShowEmailModal(false)} className="text-text-muted hover:text-text-main transition-colors">✕</button>
                            </div>
                            <form onSubmit={handleEmailSend} className="p-6 space-y-5">
                                <div>
                                    <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Full Name</label>
                                    <input required type="text" value={name} onChange={e => setName(e.target.value)} className="w-full bg-bg-main/50 border border-border-main/50 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-accent/50 focus:border-primary-accent text-text-main placeholder-text-muted/50 transition-all shadow-inner" placeholder="John Doe" />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Email Address</label>
                                    <input required type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-bg-main/50 border border-border-main/50 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-accent/50 focus:border-primary-accent text-text-main placeholder-text-muted/50 transition-all shadow-inner" placeholder="john@example.com" />
                                </div>
                                <div className="pt-6 flex justify-end gap-3 border-t border-border-main/20 mt-4">
                                    <button type="button" onClick={() => setShowEmailModal(false)} className="px-5 py-2.5 text-sm font-bold text-text-muted hover:bg-bg-main/50 rounded-xl transition-all">Cancel</button>
                                    <button type="submit" disabled={isSending} className="px-6 py-2.5 text-sm font-bold accent-gradient text-text-inverse rounded-xl shadow-lg hover:opacity-90 flex items-center gap-2 disabled:opacity-50 transition-all active:scale-95">
                                        {isSending ? <><Loader2 size={16} className="animate-spin" /> Sending</> : 'Send via Email'}
                                    </button>
                                </div>
                            </form>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
