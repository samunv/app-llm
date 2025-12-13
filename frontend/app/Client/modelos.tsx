import { FaBolt, FaRocket } from "react-icons/fa6";
import { Modelo } from "../interfaces/Modelo";
import { SiOllama } from "react-icons/si";
import { RiGeminiFill } from "react-icons/ri";

export const modelosLLM: Modelo[] = [
  {
    id: "gemini-2.5-flash-lite",
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
    id:"llama3:8b",
    nombre: "Llama (local)",
    version: "Local",
    descripcion:"Más Lento. No lee imágenes. Requiere instalación de llama3.2:1b en el equipo.",
    velocidad:"equilibrado",
    icono: <SiOllama className="text-xl"/>,
    color:"#318BFF"
  }
];