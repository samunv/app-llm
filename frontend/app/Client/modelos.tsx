import { FaBolt, FaRocket } from "react-icons/fa6";
import { Modelo } from "../interfaces/Modelo";
import { SiOllama } from "react-icons/si";
import { RiGeminiFill } from "react-icons/ri";

export const modelosLLM: Modelo[] = [
  {
    id: "llama-3.1-8b-instant",
    nombre: "Llama Instant",
    version: "Última Generación",
    descripcion: "Lo último de Llama, perfecto para recetas innovadoras",
    velocidad: "ultrarrápido",
    icono: <SiOllama className="text-xl"/>,
    color: "#EA4335",
    recomendado: true,
  },
  {
    id: "llama-3.3-70b-versatile",
    nombre: "Llama Versatile",
    version: "Estándar",
    descripcion: "Rápido y eficiente, ideal para recetas del día a día",
    velocidad: "equilibrado",
    icono: <FaBolt className="text-xl" />,
    color: "#FBBC04",
  },
  // {
  //   id:"llama3:8b",
  //   nombre: "Llama (local)",
  //   version: "Local",
  //   descripcion:"Más Lento. No lee imágenes. Requiere instalación de llama3.2:1b en el equipo.",
  //   velocidad:"equilibrado",
  //   icono: <SiOllama className="text-xl"/>,
  //   color:"#318BFF"
  // }
];