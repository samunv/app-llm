import { useState } from "react";
import { Conversacion } from "../interfaces/Conversacion";
import { Receta } from "../interfaces/Receta";

export const useHistorial = () => {
  const [historial, setHistorial] = useState<Conversacion[]>(() => {
    try {
      const guardado = localStorage.getItem("chefgpt_historial");
      return guardado ? JSON.parse(guardado) : [];
    } catch {
      return [];
    }
  });

  const guardarConversacion = (receta: Receta, comidaSolicitada: string) => {
    const nuevaConversacion: Conversacion = {
      id: crypto.randomUUID(),
      titulo: comidaSolicitada.charAt(0).toUpperCase() + comidaSolicitada.slice(1),
      fecha: new Date().toLocaleDateString(),
      receta,
    };

    const nuevoHistorial = [nuevaConversacion, ...historial];
    setHistorial(nuevoHistorial);
    localStorage.setItem("chefgpt_historial", JSON.stringify(nuevoHistorial));
  };

  const borrarConversacion = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const nuevoHistorial = historial.filter((c) => c.id !== id);
    setHistorial(nuevoHistorial);
    localStorage.setItem("chefgpt_historial", JSON.stringify(nuevoHistorial));
  };

  return { historial, guardarConversacion, borrarConversacion };
};
