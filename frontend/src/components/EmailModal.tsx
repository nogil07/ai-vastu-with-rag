import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, Send, CheckCircle } from 'lucide-react';

interface EmailModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const EmailModal: React.FC<EmailModalProps> = ({ isOpen, onClose }) => {
    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!fullName || !email) return;

        setLoading(true);
        setErrorMsg('');

        try {
            const response = await fetch('https://ai-vastu-with-rag.onrender.com/api/email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fullName, email }),
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess(true);
                setTimeout(() => {
                    onClose();
                    setSuccess(false);
                    setFullName('');
                    setEmail('');
                }, 2500);
            } else {
                setErrorMsg(data.detail || 'Failed to send email.');
            }
        } catch (err) {
            setErrorMsg('Network error. Could not connect to the server.');
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-[150] flex items-center justify-center p-4 sm:p-6"
            >
                <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />

                <motion.div
                    initial={{ scale: 0.95, opacity: 0, y: 20 }}
                    animate={{ scale: 1, opacity: 1, y: 0 }}
                    exit={{ scale: 0.95, opacity: 0, y: 20 }}
                    className="relative w-full max-w-md glass-card bg-bg-surface/90 backdrop-blur-2xl rounded-[2.5rem] shadow-2xl overflow-hidden border border-border-main/50"
                >
                    <div className="p-8 sm:p-10">
                        <div className="flex justify-between items-center mb-8">
                            <h3 className="text-3xl font-serif font-bold text-text-main tracking-tight">Email Report</h3>
                            <button
                                onClick={onClose}
                                className="p-2.5 rounded-2xl bg-bg-main/50 hover:bg-bg-main transition-all text-text-muted hover:text-text-main active:scale-90"
                            >
                                <X size={22} />
                            </button>
                        </div>

                        {success ? (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="flex flex-col items-center justify-center py-10 text-center"
                            >
                                <div className="w-20 h-20 bg-emerald-500/10 rounded-3xl flex items-center justify-center text-emerald-500 mb-6 shadow-inner">
                                    <CheckCircle size={40} />
                                </div>
                                <h4 className="text-2xl font-serif font-bold text-text-main mb-3">Sent Successfully!</h4>
                                <p className="text-text-muted text-base">Your Vastu report has been emailed.</p>
                            </motion.div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-6">
                                <div className="space-y-2.5">
                                    <label className="text-[10px] font-black uppercase tracking-[0.2em] text-primary-accent ml-1.5">Full Name</label>
                                    <input
                                        type="text"
                                        required
                                        value={fullName}
                                        onChange={(e) => setFullName(e.target.value)}
                                        className="w-full bg-bg-main/50 border border-border-main rounded-2xl px-5 py-4 text-text-main focus:border-primary-accent focus:ring-4 focus:ring-primary-accent/10 outline-none transition-all placeholder:text-text-muted/30 font-medium"
                                        placeholder="John Doe"
                                    />
                                </div>
                                <div className="space-y-2.5">
                                    <label className="text-[10px] font-black uppercase tracking-[0.2em] text-primary-accent ml-1.5">Email Address</label>
                                    <input
                                        type="email"
                                        required
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full bg-bg-main/50 border border-border-main rounded-2xl px-5 py-4 text-text-main focus:border-primary-accent focus:ring-4 focus:ring-primary-accent/10 outline-none transition-all placeholder:text-text-muted/30 font-medium"
                                        placeholder="john@example.com"
                                    />
                                </div>

                                {errorMsg && (
                                    <motion.div
                                        initial={{ opacity: 0, y: -10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="p-4 bg-red-500/5 border border-red-500/20 rounded-2xl text-red-500 text-sm font-bold flex items-center gap-2"
                                    >
                                        <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                                        {errorMsg}
                                    </motion.div>
                                )}

                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full flex items-center justify-center gap-3 bg-primary-accent text-btn-text px-6 py-5 rounded-2xl font-bold hover:opacity-90 transition-all shadow-xl shadow-primary-accent/20 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed mt-4"
                                >
                                    {loading ? (
                                        <div className="w-6 h-6 border-2 border-btn-text/30 border-t-btn-text rounded-full animate-spin" />
                                    ) : (
                                        <>
                                            <Send size={20} />
                                            Send PDF Report
                                        </>
                                    )}
                                </button>
                            </form>
                        )}
                    </div>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};
