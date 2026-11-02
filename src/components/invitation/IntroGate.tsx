import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
const seal = "https://media.invitestory.in/ever-after-bloom/src/assets/invite-seal.png";
const video = "https://media.invitestory.in/ever-after-bloom/src/assets/invite-open.mp4";

/** Frame of the film where the envelope is fully open and we cross into the site. */
const FADE_AT = 7.15;

type Stage = "seal" | "film" | "done";

/**
 * The cover of the storybook: a wax-sealed envelope. Tapping the seal plays the
 * opening film, which dissolves into the invitation at 7.15s.
 */
export function IntroGate() {
  const [stage, setStage] = useState<Stage>("seal");
  const [playing, setPlaying] = useState(false);
  const [fading, setFading] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  // Lock scrolling until the book is open.
  useEffect(() => {
    if (stage === "done") return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [stage]);

  const open = () => {
    if (stage !== "seal") return;
    setStage("film");
    window.dispatchEvent(new CustomEvent("play-wedding-music"));
    const el = videoRef.current;
    if (!el) return;
    el.currentTime = 0;
    void el.play();
  };

  const finish = () => {
    if (fading) return;
    window.dispatchEvent(new CustomEvent("play-wedding-music"));
    setFading(true);
    window.setTimeout(() => setStage("done"), 1300);
  };

  if (stage === "done") return null;

  return (
    <motion.div
      className="fixed inset-0 z-[100] overflow-hidden bg-[var(--ivory)]"
      initial={{ opacity: 1 }}
      animate={{ opacity: fading ? 0 : 1 }}
      transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
      style={{ pointerEvents: fading ? "none" : "auto" }}
    >
      {/* The film is mounted from the start and preloaded, so the cut is seamless.
          It sits under the envelope and is only revealed once frames are playing. */}
      <motion.video
        ref={videoRef}
        src={video}
        playsInline
        muted
        preload="auto"
        initial={false}
        animate={{ opacity: playing ? 1 : 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="absolute inset-0 h-full w-full object-cover"
        onPlaying={() => setPlaying(true)}
        onTimeUpdate={(e) => {
          if (e.currentTarget.currentTime >= FADE_AT) finish();
        }}
        onEnded={finish}
        onError={finish}
      />

      {/* The sealed envelope plate — stays put until the film is actually running */}
      <motion.button
        type="button"
        onClick={open}
        disabled={stage === "film"}
        aria-label="Tap the seal to open the invitation"
        className="absolute inset-0 h-full w-full cursor-pointer"
        initial={{ opacity: 0, scale: 1.04 }}
        animate={{ opacity: playing ? 0 : 1, scale: playing ? 1.02 : 1 }}
        transition={{ duration: playing ? 0.5 : 1.1, ease: [0.22, 1, 0.36, 1] }}
        style={{ pointerEvents: stage === "film" ? "none" : "auto" }}
      >
        <img
          src={seal}
          alt="Ivory wedding envelope with a gold wax seal on a marble pedestal, framed by bougainvillea"
          className="h-full w-full object-cover"
        />
        {/* Breathing glow over the wax seal to invite the tap */}
        <motion.span
          aria-hidden
          className="pointer-events-none absolute top-[46%] left-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2 rounded-full blur-2xl"
          style={{
            background:
              "radial-gradient(circle, color-mix(in oklab, var(--gold) 55%, transparent), transparent 70%)",
          }}
          animate={{ opacity: [0.35, 0.8, 0.35], scale: [0.9, 1.15, 0.9] }}
          transition={{ duration: 2.8, repeat: Infinity, ease: "easeInOut" }}
        />
      </motion.button>

      {/* Skip */}
      <button
        type="button"
        onClick={finish}
        className="absolute right-5 bottom-6 z-10 rounded-full bg-[color-mix(in_oklab,var(--ivory)_70%,transparent)] px-4 py-2 font-sans text-[0.6rem] tracking-[0.28em] text-primary uppercase backdrop-blur"
      >
        Skip
      </button>
    </motion.div>
  );
}
