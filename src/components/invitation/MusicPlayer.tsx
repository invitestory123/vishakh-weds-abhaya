import { useState, useEffect, useRef } from "react";
import { Music, VolumeX } from "lucide-react";
import { motion } from "motion/react";

export function MusicPlayer() {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const audio = new Audio("/assets/audio.mp3");
    audio.loop = true;
    audio.volume = 0.6;
    audioRef.current = audio;

    const handleEnded = () => {
      audio.currentTime = 0;
      audio.play().catch(() => {});
    };
    audio.addEventListener("ended", handleEnded);

    const handleTrigger = () => {
      audio
        .play()
        .then(() => {
          setIsPlaying(true);
        })
        .catch(() => {
          // Autoplay policy fallback
        });
    };

    window.addEventListener("play-wedding-music", handleTrigger);

    return () => {
      window.removeEventListener("play-wedding-music", handleTrigger);
      audio.removeEventListener("ended", handleEnded);
      audio.pause();
    };
  }, []);

  const togglePlay = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current
        .play()
        .then(() => {
          setIsPlaying(true);
        })
        .catch(() => {});
    }
  };

  return (
    <div className="fixed bottom-6 right-5 z-40 flex items-center gap-2">
      <motion.button
        type="button"
        onClick={togglePlay}
        whileTap={{ scale: 0.92 }}
        whileHover={{ scale: 1.05 }}
        aria-label={isPlaying ? "Mute music" : "Play music"}
        className="group relative flex h-12 w-12 items-center justify-center rounded-full border border-[var(--gold)]/50 bg-[color-mix(in_oklab,var(--ivory)_88%,transparent)] text-primary shadow-[0_4px_24px_rgba(0,0,0,0.12)] backdrop-blur-md transition-all hover:border-[var(--gold-deep)] hover:bg-[var(--ivory)]"
      >
        {isPlaying && (
          <span
            aria-hidden
            className="absolute inset-0 rounded-full bg-[var(--gold)]/20 blur-sm animate-pulse"
          />
        )}

        {isPlaying ? (
          <div className="relative flex items-end gap-[3px] h-4">
            <span className="w-[3px] bg-primary rounded-full animate-bounce [animation-delay:-0.3s] h-4" />
            <span className="w-[3px] bg-[var(--gold-deep)] rounded-full animate-bounce [animation-delay:-0.15s] h-3" />
            <span className="w-[3px] bg-primary rounded-full animate-bounce [animation-delay:-0.45s] h-4" />
            <span className="w-[3px] bg-[var(--gold-deep)] rounded-full animate-bounce h-2" />
          </div>
        ) : (
          <Music size={19} className="relative text-primary/75 transition-colors group-hover:text-primary" />
        )}
      </motion.button>
    </div>
  );
}
