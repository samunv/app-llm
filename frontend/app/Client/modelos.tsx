import { FaBolt, FaRocket } from "react-icons/fa6";
import { Modelo } from "../interfaces/Modelo";

export const modelosGemini: Modelo[] = [
  {
    id: "gemini-2.5-flash",
    nombre: "Gemini 2.5 Flash",
    version: "Última Generación",
    descripcion: "Lo último de Google, perfecto para recetas innovadoras",
    velocidad: "ultrarrápido",
    icono: <FaRocket className="text-xl" />,
    color: "#EA4335",
    recomendado: true,
  },
  {
    id: "gemini-2.0-flash-lite",
    nombre: "Gemini 2.0 Flash Lite",
    version: "Estándar",
    descripcion: "Rápido y eficiente, ideal para recetas del día a día",
    velocidad: "equilibrado",
    icono: <FaBolt className="text-xl" />,
    color: "#FBBC04",
  },
];