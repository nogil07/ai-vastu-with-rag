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
            const response = await fetch('http://localhost:8080/api/email', {
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
                    className="relative w-full max-w-md bg-white dark:bg-zinc-900 rounded-[2rem] shadow-2xl overflow-hidden border border-border-main"
                >
                    <div className="p-6 sm:p-8">
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="text-2xl font-serif font-bold text-text-main">Email Report</h3>
                            <button
                                onClick={onClose}
                                className="p-2 rounded-full hover:bg-bg-surface transition-colors text-text-muted hover:text-text-main"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        {success ? (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="flex flex-col items-center justify-center py-8 text-center"
                            >
                                <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center text-green-500 mb-4">
                                    <CheckCircle size={32} />
                                </div>
                                <h4 className="text-xl font-bold text-text-main mb-2">Sent Successfully!</h4>
                                <p className="text-text-muted text-sm">Your Vastu report has been emailed.</p>
                            </motion.div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div className="space-y-2">
                                    <label className="text-[10px] font-black uppercase tracking-[0.2em] text-text-muted ml-1">Full Name</label>
                                    <input
                                        type="text"
                                        required
                                        value={fullName}
                                        onChange={(e) => setFullName(e.target.value)}
                                        className="w-full bg-bg-surface border border-border-main rounded-xl px-4 py-3 text-text-main focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all placeholder:text-text-muted/50"
                                        placeholder="John Doe"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-[10px] font-black uppercase tracking-[0.2em] text-text-muted ml-1">Email Address</label>
                                    <input
                                        type="email"
                                        required
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full bg-bg-surface border border-border-main rounded-xl px-4 py-3 text-text-main focus:ring-2 focus:ring-primary-accent/50 outline-none transition-all placeholder:text-text-muted/50"
                                        placeholder="john@example.com"
                                    />
                                </div>

                                {errorMsg && (
                                    <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-500 text-sm font-medium">
                                        {errorMsg}
                                    </div>
                                )}

                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full flex items-center justify-center gap-2 bg-primary-accent text-btn-text px-6 py-4 rounded-xl font-bold hover:opacity-90 transition-all shadow-lg shadow-primary-accent/20 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed mt-2"
                                >
                                    {loading ? (
                                        <div className="w-5 h-5 border-2 border-btn-text/30 border-t-btn-text rounded-full animate-spin" />
                                    ) : (
                                        <>
                                            <Send size={18} />
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
