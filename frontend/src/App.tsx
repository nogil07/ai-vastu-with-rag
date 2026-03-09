import React, { useEffect, useRef, useState } from 'react';
import { motion, useScroll, useTransform, useSpring, AnimatePresence } from 'motion/react';
import Lenis from 'lenis';
import {
  Compass,
  ShieldCheck,
  Database,
  Layout,
  BarChart3,
  FileText,
  ArrowRight,
  Menu,
  X,
  Zap,
  Clock,
  CheckCircle2,
  ChevronRight,
  Sun,
  Moon
} from 'lucide-react';
import { Hero3D } from './components/Hero3D';
import { ProductDemo } from './components/ProductDemo';
import { PlanForm } from './components/PlanForm';
import { Chatbot } from './components/Chatbot';
import { ResultView } from './components/ResultView';
import { cn } from './lib/utils';

const Navbar = React.memo(({ isDark, toggleDark, onOpenForm }: { isDark: boolean, toggleDark: () => void, onOpenForm: () => void }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.nav
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 1, ease: [0.21, 0.47, 0.32, 0.98], delay: 0.5 }}
      className="fixed top-0 left-0 w-full z-50 px-4 py-3 md:px-6 md:py-4"
    >
      <div className="max-w-4xl mx-auto flex items-center justify-between glass-card px-5 py-2 md:px-7 md:py-2.5 rounded-xl relative">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 md:w-9 md:h-9 bg-primary-accent rounded-lg flex items-center justify-center text-btn-text font-bold shadow-lg shadow-primary-accent/20">A</div>
          <span className="font-serif font-bold text-lg md:text-xl tracking-tight text-text-main">AI Vastu</span>
        </div>

        <div className="hidden md:flex items-center gap-8 text-xs font-bold uppercase tracking-wider text-text-muted">
          <a href="#features" className="hover:text-primary-accent transition-colors">Features</a>
          <a href="#how-it-works" className="hover:text-primary-accent transition-colors">Process</a>
          <a href="#demo" className="hover:text-primary-accent transition-colors">Demo</a>
          <a href="#benefits" className="hover:text-primary-accent transition-colors">Benefits</a>
        </div>

        <div className="flex items-center gap-3 md:gap-4">
          <button
            onClick={toggleDark}
            className="p-2 rounded-lg hover:bg-bg-surface/10 transition-colors text-text-muted"
          >
            {isDark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
          <button className="hidden sm:block text-xs font-bold text-text-muted hover:text-text-main transition-colors">
            Contact
          </button>
          <button
            onClick={onOpenForm}
            className="bg-primary-accent text-btn-text text-[10px] md:text-xs font-bold px-5 py-2 md:px-6 md:py-2.5 rounded-lg hover:opacity-90 transition-all shadow-lg shadow-primary-accent/20 active:scale-95"
          >
            Get Started
          </button>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-text-muted hover:text-text-main transition-colors"
          >
            {isOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="absolute top-full left-0 right-0 mt-4 glass-card p-6 rounded-2xl flex flex-col gap-4 md:hidden shadow-2xl"
            >
              <a href="#features" onClick={() => setIsOpen(false)} className="text-lg font-serif font-bold py-2 border-b border-border-main text-text-main">Features</a>
              <a href="#how-it-works" onClick={() => setIsOpen(false)} className="text-lg font-serif font-bold py-2 border-b border-border-main text-text-main">Process</a>
              <a href="#demo" onClick={() => setIsOpen(false)} className="text-lg font-serif font-bold py-2 border-b border-border-main text-text-main">Demo</a>
              <a href="#benefits" onClick={() => setIsOpen(false)} className="text-lg font-serif font-bold py-2 text-text-main">Benefits</a>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.nav>
  );
});

const FeatureCard = React.memo(({ icon: Icon, title, description, index }: { icon: any, title: string, description: string, index: number }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{
        duration: 0.8,
        delay: index * 0.05,
        ease: [0.21, 0.47, 0.32, 0.98]
      }}
      className="group glass-card p-10 rounded-[2rem] hover:bg-bg-surface transition-all duration-500 hover:shadow-2xl hover:shadow-primary-accent/5 will-change-transform"
    >
      <div className="w-14 h-14 bg-bg-surface rounded-2xl flex items-center justify-center text-text-main mb-8 group-hover:bg-primary-accent group-hover:text-btn-text transition-all duration-500 shadow-inner">
        <Icon size={28} />
      </div>
      <h3 className="text-2xl font-serif font-bold mb-4 text-text-main">{title}</h3>
      <p className="text-text-muted text-sm leading-relaxed font-medium">{description}</p>
    </motion.div>
  );
});

const Step = React.memo(({ number, title, description, isLast }: { number: string, title: string, description: string, isLast?: boolean }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.8, ease: [0.21, 0.47, 0.32, 0.98] }}
      className="relative flex flex-col items-center text-center group will-change-transform"
    >
      <div className="w-16 h-16 rounded-full bg-bg-surface border-2 border-border-main flex items-center justify-center text-xl font-serif font-bold mb-6 group-hover:border-primary-accent group-hover:bg-bg-main transition-all duration-500 relative z-10 shadow-sm text-text-main">
        {number}
      </div>
      {!isLast && (
        <div className="hidden lg:block absolute top-8 left-[calc(50%+32px)] w-[calc(100%-64px)] h-[2px] bg-border-main/20 overflow-hidden">
          <motion.div
            initial={{ x: '-100%' }}
            whileInView={{ x: '100%' }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-full h-full bg-primary-accent"
          />
        </div>
      )}
      <h4 className="text-lg font-serif font-bold mb-2 text-text-main">{title}</h4>
      <p className="text-text-muted text-xs max-w-[150px] leading-relaxed">{description}</p>
    </motion.div>
  );
});

export default function App() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll();
  const [isDark, setIsDark] = useState(false);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isGenerated, setIsGenerated] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
      infinite: false,
    });

    function raf(time: number) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);

    return () => {
      lenis.destroy();
    };
  }, []);

  const toggleDark = () => setIsDark(!isDark);

  // Smooth out scroll progress for all transforms
  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 50,
    damping: 20,
    restDelta: 0.001
  });

  const scale = useTransform(smoothProgress, [0, 0.2], [1, 0.95]);
  const opacity = useTransform(smoothProgress, [0, 0.2], [1, 0.8]);
  const gridY = useTransform(smoothProgress, [0, 1], [0, -100]);
  const bgY = useTransform(smoothProgress, [0, 1], ["0%", "20%"]);
  const bgScale = useTransform(smoothProgress, [0, 1], [1.1, 1.2]);

  return (
    <div ref={containerRef} className="relative overflow-x-hidden selection:bg-primary-accent selection:text-btn-text transition-colors duration-700">
      {/* Smooth Progress Bar */}
      <motion.div
        className="fixed top-0 left-0 right-0 h-1 bg-primary-accent z-[60] origin-left"
        style={{ scaleX: scrollYProgress }}
      />

      <motion.div
        style={{ y: gridY }}
        className="fixed inset-0 blueprint-grid pointer-events-none z-[1] opacity-20 will-change-transform"
      />

      <div className="fixed inset-0 arch-pattern pointer-events-none z-[0] opacity-30" />

      {/* Architectural Background Elements */}
      <div className="fixed inset-0 z-[1] pointer-events-none overflow-hidden">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.1 }}
          transition={{ duration: 2 }}
          className="absolute top-[10%] left-[5%] w-[400px] h-[400px] border border-primary-accent/30 rounded-full"
        />
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.05 }}
          transition={{ duration: 2, delay: 0.5 }}
          className="absolute bottom-[15%] right-[10%] w-[600px] h-[600px] border border-primary-accent/20 rotate-45"
        />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full max-w-7xl mx-auto opacity-[0.03]">
          <svg width="100%" height="100%" viewBox="0 0 800 800" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 100H700V700H100V100Z" stroke="currentColor" strokeWidth="1" />
            <path d="M100 300H700" stroke="currentColor" strokeWidth="1" />
            <path d="M300 100V700" stroke="currentColor" strokeWidth="1" />
            <path d="M100 500H400" stroke="currentColor" strokeWidth="1" />
            <path d="M500 100V400" stroke="currentColor" strokeWidth="1" />
            <circle cx="400" cy="400" r="50" stroke="currentColor" strokeWidth="1" />
          </svg>
        </div>
      </div>

      <Navbar isDark={isDark} toggleDark={toggleDark} onOpenForm={() => setIsFormOpen(true)} />

      <PlanForm
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        onGenerationComplete={() => setIsGenerated(true)}
      />

      {isGenerated ? (
        <ResultView onBack={() => setIsGenerated(false)} />
      ) : (
        <>
          {/* Cinematic Grain Overlay */}
          <div className="fixed inset-0 grain-overlay pointer-events-none" />

          {/* Hero Section */}
          <section className="relative min-h-screen flex flex-col items-center justify-center pt-20 pb-10 px-6 overflow-hidden">
            <motion.div
              style={{ scale, opacity }}
              className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center z-10 will-change-transform"
            >
              <div className="space-y-8 text-center lg:text-left">
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 1.2, ease: [0.21, 0.47, 0.32, 0.98] }}
                >
                  <span className="inline-block px-5 py-2 rounded-full bg-bg-surface text-primary-accent text-[10px] font-bold tracking-[0.2em] uppercase mb-6 md:mb-8 border border-border-main">
                    Architectural Intelligence
                  </span>
                  <h1 className="text-5xl sm:text-6xl md:text-8xl font-serif font-bold leading-[1.05] text-balance tracking-tight text-text-main">
                    Design with <br />
                    <span className="italic text-primary-accent">Precision</span>
                  </h1>
                </motion.div>

                <motion.p
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 1.2, delay: 0.1, ease: [0.21, 0.47, 0.32, 0.98] }}
                  className="text-lg md:text-xl text-text-muted max-w-xl mx-auto lg:mx-0 text-balance font-medium leading-relaxed"
                >
                  AI Vastu generates intelligent, regulation-compliant home layouts using advanced RAG technology and architectural principles.
                </motion.p>

                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 1.2, delay: 0.2, ease: [0.21, 0.47, 0.32, 0.98] }}
                  className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 md:gap-6"
                >
                  <button
                    onClick={() => setIsFormOpen(true)}
                    className="w-full sm:w-auto bg-primary-accent text-btn-text px-10 py-4 md:py-5 rounded-2xl font-bold hover:opacity-90 transition-all flex items-center justify-center gap-3 group shadow-2xl shadow-primary-accent/20 active:scale-95"
                  >
                    Generate Plan
                    <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                  </button>
                  <a
                    href="#demo"
                    className="w-full sm:w-auto bg-bg-surface text-text-main border border-border-main px-10 py-4 md:py-5 rounded-2xl font-bold hover:bg-bg-main transition-all active:scale-95 flex items-center justify-center"
                  >
                    View Demo
                  </a>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8, duration: 1 }}
                  className="flex items-center justify-center lg:justify-start gap-8 pt-8"
                >
                  <div className="text-center lg:text-left">
                    <div className="text-2xl font-serif font-bold text-text-main">12m+</div>
                    <div className="text-[10px] uppercase tracking-widest text-text-muted">Customers</div>
                  </div>
                  <div className="w-px h-8 bg-border-main" />
                  <div className="text-center lg:text-left">
                    <div className="text-2xl font-serif font-bold text-text-main">98%</div>
                    <div className="text-[10px] uppercase tracking-widest text-text-muted">Accuracy</div>
                  </div>
                </motion.div>
              </div>

              <motion.div
                initial={{ opacity: 0, scale: 0.8, rotateY: 15 }}
                animate={{ opacity: 1, scale: 1, rotateY: 0 }}
                transition={{ duration: 1.5, delay: 0.2, ease: [0.21, 0.47, 0.32, 0.98] }}
                className="relative perspective-1000"
              >
                <Hero3D scrollProgress={smoothProgress} isDark={isDark} />
              </motion.div>
            </motion.div>
          </section>

          {/* Features Section */}
          <section id="features" className="py-32 px-6 bg-bg-main/60 backdrop-blur-md relative z-10">
            <div className="max-w-7xl mx-auto">
              <div className="text-center mb-20">
                <motion.h2
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  className="text-4xl md:text-5xl font-serif font-bold mb-6 text-text-main"
                >
                  Intelligent Architecture
                </motion.h2>
                <motion.p
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.1 }}
                  className="text-text-muted max-w-2xl mx-auto"
                >
                  Our AI engine combines ancient wisdom with modern regulations to create the perfect living space.
                </motion.p>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <FeatureCard
                  icon={Compass}
                  title="AI Vastu Planning"
                  description="Automatically places rooms according to Vastu principles for optimal energy flow and harmony."
                  index={0}
                />
                <FeatureCard
                  icon={ShieldCheck}
                  title="Regulation-Aware Design"
                  description="Ensures compliance with KPBR and local building regulations automatically during generation."
                  index={1}
                />
                <FeatureCard
                  icon={Database}
                  title="RAG Knowledge System"
                  description="Retrieves architectural rules from thousands of legal documents using advanced AI retrieval."
                  index={2}
                />
                <FeatureCard
                  icon={Layout}
                  title="Automated Floor Plans"
                  description="Creates dimensioned 2D architectural layouts ready for professional drafting and review."
                  index={3}
                />
                <FeatureCard
                  icon={BarChart3}
                  title="Compliance Scoring"
                  description="Evaluates every plan with a detailed Vastu and regulation compliance score for peace of mind."
                  index={4}
                />
                <FeatureCard
                  icon={FileText}
                  title="Smart Reports"
                  description="Download professional architectural compliance reports with one click for your records."
                  index={5}
                />
              </div>
            </div>
          </section>

          {/* Demo Section */}
          <section id="demo" className="py-32 px-6 relative overflow-hidden bg-bg-surface/10 backdrop-blur-[2px] z-10">
            <div className="max-w-7xl mx-auto">
              <div className="text-center mb-16">
                <span className="text-primary-accent text-xs font-bold tracking-widest uppercase">Live Preview</span>
                <h2 className="text-4xl md:text-5xl font-serif font-bold mt-4 text-text-main">See it in Action</h2>
              </div>
              <ProductDemo />
            </div>
          </section>

          {/* How It Works Section */}
          <section id="how-it-works" className="py-32 px-6 bg-bg-surface backdrop-blur-md text-text-main relative overflow-hidden z-10">
            <div className="absolute inset-0 blueprint-grid opacity-10 pointer-events-none" />
            <div className="max-w-7xl mx-auto relative z-10">
              <div className="text-center mb-20">
                <h2 className="text-4xl md:text-5xl font-serif font-bold mb-6">The Process</h2>
                <p className="text-text-muted max-w-2xl mx-auto">From plot details to a complete architectural report in minutes.</p>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-6 gap-12 lg:gap-4">
                <Step number="01" title="Enter Plot" description="Input dimensions and facing direction." />
                <Step number="02" title="Upload Rules" description="Provide local building regulations." />
                <Step number="03" title="AI Processing" description="RAG engine analyzes all constraints." />
                <Step number="04" title="Generation" description="2D blueprint is created instantly." />
                <Step number="05" title="Evaluation" description="Compliance scoring and Vastu check." />
                <Step number="06" title="Final Report" description="Download your ready-to-use plan." isLast />
              </div>
            </div>
          </section>

          {/* Benefits Section */}
          <section id="benefits" className="py-32 px-6 bg-bg-main/60 backdrop-blur-md z-10">
            <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-20 items-center">
              <div className="space-y-8">
                <h2 className="text-4xl md:text-5xl font-serif font-bold leading-tight text-text-main">
                  We combine nature & <br /> home comfort
                </h2>
                <p className="text-text-muted text-lg">
                  AI Vastu isn't just a tool; it's your digital architect that understands the soul of a home.
                </p>

                <div className="space-y-6">
                  {[
                    "10× Faster architectural planning",
                    "Automated regulation compliance",
                    "AI-Assisted Vastu optimization",
                    "Smart urban housing design"
                  ].map((benefit, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: i * 0.1, duration: 0.6 }}
                      className="flex items-center gap-4"
                    >
                      <div className="w-6 h-6 rounded-full bg-primary-accent/10 flex items-center justify-center text-primary-accent">
                        <CheckCircle2 size={16} />
                      </div>
                      <span className="font-medium text-text-main/90">{benefit}</span>
                    </motion.div>
                  ))}
                </div>

                <button className="text-text-main font-bold flex items-center gap-2 group hover:text-primary-accent transition-colors">
                  LEARN MORE
                  <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                </button>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="space-y-6 pt-0 sm:pt-12">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="glass-card p-8 rounded-3xl space-y-4 hover:bg-bg-surface transition-all duration-500"
                  >
                    <Clock className="text-primary-accent" size={32} />
                    <h4 className="text-xl font-serif font-bold text-text-main">Time Saving</h4>
                    <p className="text-sm text-text-muted">Reduce manual drafting time by up to 90%.</p>
                  </motion.div>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.1 }}
                    className="glass-card p-8 rounded-3xl space-y-4 hover:bg-bg-surface transition-all duration-500"
                  >
                    <ShieldCheck className="text-secondary-accent" size={32} />
                    <h4 className="text-xl font-serif font-bold text-text-main">Risk Free</h4>
                    <p className="text-sm text-text-muted">Avoid costly regulation compliance errors.</p>
                  </motion.div>
                </div>
                <div className="space-y-6">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.2 }}
                    className="glass-card p-8 rounded-3xl space-y-4 hover:bg-bg-surface transition-all duration-500"
                  >
                    <Zap className="text-primary-accent" size={32} />
                    <h4 className="text-xl font-serif font-bold text-text-main">Smart AI</h4>
                    <p className="text-sm text-text-muted">Advanced RAG system for rule retrieval.</p>
                  </motion.div>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.3 }}
                    className="bg-primary-accent p-8 rounded-3xl space-y-4 text-btn-text shadow-xl shadow-primary-accent/20 hover:scale-[1.02] transition-transform duration-500"
                  >
                    <Layout size={32} />
                    <h4 className="text-xl font-serif font-bold">Pro Layouts</h4>
                    <p className="text-sm text-btn-text/70">Dimensioned plans ready for construction.</p>
                  </motion.div>
                </div>
              </div>
            </div>
          </section>

          {/* CTA Section */}
          <section className="py-32 px-6 relative z-10">
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 1, ease: [0.21, 0.47, 0.32, 0.98] }}
              className="max-w-5xl mx-auto bg-bg-surface rounded-[3rem] p-12 md:p-24 text-center text-btn-text relative overflow-hidden"
            >
              <div className="absolute inset-0 blueprint-grid opacity-10 pointer-events-none" />
              <div className="relative z-10 space-y-8">
                <h2 className="text-4xl md:text-6xl font-serif font-bold leading-tight">
                  Start Designing Your <br /> Vastu-Compliant Home Today
                </h2>
                <p className="text-btn-text/80 text-lg max-w-2xl mx-auto">
                  Join thousands of homeowners and architects using AI Vastu to create perfect, regulation-compliant living spaces.
                </p>
                <div className="flex flex-wrap justify-center gap-4 pt-4">
                  <button
                    onClick={() => setIsFormOpen(true)}
                    className="bg-bg-main text-text-main px-10 py-5 rounded-full font-bold hover:bg-bg-surface transition-all shadow-2xl active:scale-95"
                  >
                    Generate Your Floor Plan
                  </button>
                  <button className="bg-transparent border border-btn-text/20 text-btn-text px-10 py-5 rounded-full font-bold hover:bg-bg-surface/10 transition-all active:scale-95">
                    Book a Demo
                  </button>
                </div>
              </div>
            </motion.div>
          </section>

          {/* Footer */}
          <footer className="py-20 px-6 border-t border-border-main bg-bg-main transition-colors duration-700">
            <div className="max-w-7xl mx-auto grid md:grid-cols-2 lg:grid-cols-4 gap-12">
              <div className="space-y-6">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-primary-accent rounded-lg flex items-center justify-center text-btn-text font-bold">V</div>
                  <span className="font-serif font-bold text-xl tracking-tight text-text-main">AI Vastu</span>
                </div>
                <p className="text-text-muted text-sm leading-relaxed">
                  The world's first AI-powered Vastu and regulation-compliant floor plan generator.
                </p>
              </div>

              <div>
                <h5 className="font-bold mb-6 text-text-main">Product</h5>
                <ul className="space-y-4 text-sm text-text-muted">
                  <li><a href="#" className="hover:text-text-main transition-colors">Generator</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">Compliance Check</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">API Access</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">Pricing</a></li>
                </ul>
              </div>

              <div>
                <h5 className="font-bold mb-6 text-text-main">Company</h5>
                <ul className="space-y-4 text-sm text-text-muted">
                  <li><a href="#" className="hover:text-text-main transition-colors">About Us</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">Careers</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">Blog</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">Contact</a></li>
                </ul>
              </div>

              <div>
                <h5 className="font-bold mb-6 text-text-main">Legal</h5>
                <ul className="space-y-4 text-sm text-text-muted">
                  <li><a href="#" className="hover:text-text-main transition-colors">Privacy Policy</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">Terms of Service</a></li>
                  <li><a href="#" className="hover:text-text-main transition-colors">Cookie Policy</a></li>
                </ul>
              </div>
            </div>
            <div className="max-w-7xl mx-auto mt-20 pt-8 border-t border-border-main flex flex-col md:row items-center justify-between gap-4 text-xs text-text-muted/50 uppercase tracking-widest font-bold">
              <div>© 2026 AI VASTU TECHNOLOGIES INC.</div>
              <div className="flex gap-8">
                <a href="#" className="hover:text-text-main transition-colors">Twitter</a>
                <a href="#" className="hover:text-text-main transition-colors">LinkedIn</a>
                <a href="#" className="hover:text-text-main transition-colors">Instagram</a>
              </div>
            </div>
          </footer>
          <Chatbot isDark={isDark} />
        </>
      )}
    </div>
  );
}
