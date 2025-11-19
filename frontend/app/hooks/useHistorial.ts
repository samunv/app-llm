import { useState, useEffect } from "react";
import { Conversacion } from "../interfaces/Conversacion";
import { Receta } from "../interfaces/Receta";

export const useHistorial = () => {
  const [historial, setHistorial] = useState<Conversacion[]>([]);

  // Cargar historial al iniciar
  useEffect(() => {
    const guardado = localStorage.getItem("chefgpt_historial");
    if (guardado) {
      setHistorial(JSON.parse(guardado));
    }
  }, []);

  // Guardar una nueva receta en el historial
  const guardarConversacion = (receta: Receta, comidaSolicitada: string) => {
    const nuevaConversacion: Conversacion = {
      id: crypto.randomUUID(), // Genera un ID único
      titulo: comidaSolicitada.charAt(0).toUpperCase() + comidaSolicitada.slice(1), // Capitalizar
      fecha: new Date().toLocaleDateString(),
      receta: receta,
    };

    const nuevoHistorial = [nuevaConversacion, ...historial];
    setHistorial(nuevoHistorial);
    localStorage.setItem("chefgpt_historial", JSON.stringify(nuevoHistorial));
  };

  // Borrar una conversación
  const borrarConversacion = (id: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Evitar que se abra al borrar
    const nuevoHistorial = historial.filter((c) => c.id !== id);
    setHistorial(nuevoHistorial);
    localStorage.setItem("chefgpt_historial", JSON.stringify(nuevoHistorial));
  };

  return { historial, guardarConversacion, borrarConversacion };
};