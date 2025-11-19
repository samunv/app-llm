"use client";

import { useEffect, useState } from "react";

type Props = {
frases: string [],
speed?: number 
}

export default function TypingText({ frases, speed = 100 }: Props) {
  const [text, setText] = useState("");
  const [index, setIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);

  useEffect(() => {
    if (index < frases.length) {
      if (charIndex < frases[index].length) {
        const timeout = setTimeout(() => {
          setText((prev) => prev + frases[index][charIndex]);
          setCharIndex(charIndex + 1);
        }, speed);
        return () => clearTimeout(timeout);
      } else {
        const timeout = setTimeout(() => {
          setText("");
          setCharIndex(0);
          setIndex(index + 1);
        }, 1000); // espera antes de la siguiente palabra
        return () => clearTimeout(timeout);
      }
    } else {
      // reinicia el loop
      const timeout = setTimeout(() => setIndex(0), 1000);
      return () => clearTimeout(timeout);
    }
  }, [charIndex, index, frases, speed]);

  return (
    <span className="bg-gradient-to-r from-orange-500 to-yellow-300 bg-clip-text text-transparent">
      {text}
      <span className="animate-pulse">|</span>
    </span>
  );
}