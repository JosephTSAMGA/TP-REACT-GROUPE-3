import { useEffect, useState } from "react";

type TimerProps = {
  roundKey: string;
  running: boolean;
};

function formatTime(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

export default function Timer({ roundKey, running }: TimerProps) {
  const [seconds, setSeconds] = useState(0);

  // Nouvelle manche -> on repart de 0.
  useEffect(() => {
    setSeconds(0);
  }, [roundKey]);

  // Tant que running est vrai, on incrémente chaque seconde.
  useEffect(() => {
    if (!running) return;

    const intervalId = setInterval(() => {
      setSeconds((previous) => previous + 1);
    }, 1000);

    return () => clearInterval(intervalId);
  }, [running]);

  return <span className="timer">⏱ {formatTime(seconds)}</span>;
}