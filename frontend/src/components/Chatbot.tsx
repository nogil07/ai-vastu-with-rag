import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Send, X, MessageSquare, User, Bot, Sparkles, Minimize2, Maximize2 } from 'lucide-react';
import { GoogleGenAI } from "@google/genai";

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export const Chatbot = ({ isDark }: { isDark: boolean }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [showInitialPopup, setShowInitialPopup] = useState(true);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm Vasuttan AI, ready to help with your architectural needs.",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowInitialPopup(false);
    }, 8000);
    return () => clearTimeout(timer);
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await fetch('http://localhost:8080/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response || "I'm sorry, I couldn't process that. Could you rephrase?",
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Chatbot Error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm having trouble connecting right now. Please try again later.",
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="fixed bottom-8 right-8 z-[100] flex flex-col items-end font-outfit">
      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 40, scale: 0.9, rotate: 2 }}
            animate={{ opacity: 1, y: 0, scale: 1, rotate: 0 }}
            exit={{ opacity: 0, y: 40, scale: 0.9, rotate: -2 }}
            className={`mb-6 w-[92vw] sm:w-[320px] h-[480px] max-h-[75vh] rounded-[2rem] overflow-hidden shadow-[0_30px_60px_rgba(0,0,0,0.3)] flex flex-col border border-white/20 relative ${isDark
              ? 'bg-slate-900/30 backdrop-blur-[40px] text-white'
              : 'bg-white/30 backdrop-blur-[40px] text-slate-900'
              }`}
          >
            {/* Liquid Background Blobs */}
            <div className="absolute inset-0 -z-10 overflow-hidden opacity-40 pointer-events-none">
              <motion.div
                animate={{
                  scale: [1, 1.2, 1],
                  x: [0, 20, 0],
                  y: [0, -20, 0]
                }}
                transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
                className="absolute top-[-10%] left-[-10%] w-[70%] h-[70%] rounded-full bg-primary-accent/30 blur-[60px]"
              />
              <motion.div
                animate={{
                  scale: [1, 1.3, 1],
                  x: [0, -30, 0],
                  y: [0, 30, 0]
                }}
                transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                className="absolute bottom-[-10%] right-[-10%] w-[70%] h-[70%] rounded-full bg-blue-500/20 blur-[60px]"
              />
            </div>

            {/* Top Status Bar */}
            <div className={`h-1 w-full ${isDark ? 'bg-white/10' : 'bg-black/10'} flex overflow-hidden`}>
              <motion.div
                animate={{ x: ['-100%', '200%'] }}
                transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                className="w-1/2 h-full bg-gradient-to-r from-transparent via-primary-accent/50 to-transparent"
              />
            </div>

            {/* Header */}
            <div className="p-4 border-b border-white/10 flex items-center justify-between relative z-10 flex-shrink-0">
              <div className="flex items-center gap-3">
                <div className="relative group">
                  <div className="w-14 h-14 rounded-2xl overflow-hidden border border-white/20 shadow-lg transition-transform duration-500 group-hover:scale-110">
                    <video
                      src="/vasuttan2.mp4"
                      autoPlay
                      loop
                      muted
                      playsInline
                      className="w-full h-full object-cover translate-y-2"
                    />
                  </div>
                  <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-500 border-2 border-white/40 shadow-sm" />
                </div>
                <div>
                  <h3 className="text-sm font-bold tracking-tight">Vasuttan AI</h3>
                  <div className="flex items-center gap-1 opacity-60">
                    <span className="text-[8px] font-mono uppercase tracking-widest">Liquid Intelligence</span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className={`p-2 rounded-xl transition-all active:scale-90 ${isDark ? 'hover:bg-white/10' : 'hover:bg-black/10'}`}
              >
                <X size={18} />
              </button>
            </div>

            {/* Messages Area */}
            <div className={`flex-1 overflow-y-auto min-h-0 p-4 space-y-4 custom-scrollbar touch-pan-y relative ${isDark ? 'scrollbar-dark' : 'scrollbar-light'}`}>
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex flex-col gap-1 max-w-[88%] ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                    <div className={`px-3 py-2 rounded-2xl leading-relaxed shadow-sm backdrop-blur-md border text-[10px] font-mono font-bold tracking-[0.2em] ${msg.sender === 'user'
                      ? 'bg-primary-accent/80 text-white rounded-tr-none border-white/20'
                      : isDark
                        ? 'bg-white/10 text-slate-100 rounded-tl-none border-white/10'
                        : 'bg-black/5 text-slate-800 rounded-tl-none border-black/5'
                      }`}>
                      {msg.text}
                    </div>
                  </div>
                </motion.div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="flex gap-1.5 items-center bg-white/10 backdrop-blur-md px-3 py-2 rounded-xl rounded-tl-none border border-white/10">
                    <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 1, repeat: Infinity }} className="w-1.5 h-1.5 bg-primary-accent rounded-full" />
                    <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 1, repeat: Infinity, delay: 0.2 }} className="w-1.5 h-1.5 bg-primary-accent rounded-full" />
                    <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 1, repeat: Infinity, delay: 0.4 }} className="w-1.5 h-1.5 bg-primary-accent rounded-full" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 pt-2 border-t border-white/10 flex-shrink-0">
              <div className={`flex items-center gap-2 p-1 rounded-xl border transition-all focus-within:ring-2 focus-within:ring-primary-accent/30 ${isDark ? 'bg-black/20 border-white/10' : 'bg-white/20 border-black/10'
                }`}>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Ask Vasuttan..."
                  className="flex-1 bg-transparent border-none focus:ring-0 text-xs px-2 py-1.5 outline-none placeholder:opacity-40"
                />
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSend}
                  disabled={!input.trim() || isTyping}
                  className="w-8 h-8 bg-primary-accent text-white rounded-lg flex items-center justify-center shadow-lg disabled:opacity-30 transition-all"
                >
                  <Send size={14} />
                </motion.button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Trigger Button & Popups */}
      <div className="relative">
        {/* Trigger Popup */}
        <AnimatePresence>
          {(showInitialPopup || isHovered) && !isOpen && (
            <motion.div
              initial={{ opacity: 0, x: 20, scale: 0.8, filter: 'blur(10px)' }}
              animate={{ opacity: 1, x: 0, scale: 1, filter: 'blur(0px)' }}
              exit={{ opacity: 0, x: 20, scale: 0.8, filter: 'blur(10px)' }}
              className={`absolute bottom-[110%] right-0 mb-4 p-3 rounded-2xl shadow-2xl border border-white/30 backdrop-blur-2xl whitespace-nowrap overflow-hidden ${isDark ? 'bg-slate-900/40 text-white' : 'bg-white/40 text-slate-900'
                }`}
            >
              {/* Popup Liquid Background */}
              <div className="absolute inset-0 -z-10 opacity-30">
                <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-primary-accent/20 to-blue-500/20 animate-pulse" />
              </div>

              <div className="flex items-center gap-3 relative z-10">
                <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center border border-white/20">
                  <Sparkles size={16} className="text-primary-accent" />
                </div>
                <span className="text-xs font-bold tracking-tight">Hi, I am Vasuttan AI</span>
              </div>
              {/* Triangle pointer */}
              <div className={`absolute bottom-[-6px] right-8 w-3 h-3 rotate-45 border-r border-b border-white/30 ${isDark ? 'bg-slate-900/40' : 'bg-white/40'
                }`} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Video Trigger */}
        <motion.button
          whileHover={{ scale: 1.1, y: -5 }}
          whileTap={{ scale: 0.9 }}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          onClick={() => {
            setIsOpen(!isOpen);
            setShowInitialPopup(false);
          }}
          className={`w-32 h-40 sm:w-36 sm:h-36 rounded-full overflow-hidden border-2 shadow-[0_20px_40px_rgba(0,0,0,0.3)] transition-all duration-500 relative group ${isOpen ? 'border-primary-accent' : 'border-white/40 hover:border-primary-accent'
            }`}
        >
          <video
            ref={videoRef}
            src="/vasuttan2.mp4"
            autoPlay
            loop
            muted
            playsInline
            className="w-full h-full object-cover object-[center_25%] transition-transform duration-700 group-hover:scale-110"
          />

          {/* Hover overlay */}
          <div className="absolute inset-0 bg-white/10 backdrop-blur-[2px] opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex items-center justify-center">
            <MessageSquare size={24} className="text-white drop-shadow-lg" />
          </div>

          {/* Open state overlay */}
          {isOpen && (
            <div className="absolute inset-0 bg-primary-accent/40 backdrop-blur-md flex items-center justify-center">
              <X size={32} className="text-white" />
            </div>
          )}
        </motion.button>
      </div>
    </div>
  );
};
