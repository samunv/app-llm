import { FaBolt, FaRocket } from "react-icons/fa6";
import { Modelo } from "../interfaces/Modelo";
import { SiOllama } from "react-icons/si";
import { RiGeminiFill } from "react-icons/ri";

export const modelosLLM: Modelo[] = [
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
  {
    id:"gemma:7b",
    nombre: "Gemma (local)",
    version: "Local",
    descripcion:"Sin límites. Lento. No lee imágenes. Requiere instalación en local.",
    velocidad:"equilibrado",
    icono: <RiGeminiFill className="text-xl"/>,
    color:"blue"
  }
];