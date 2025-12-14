import { Receta } from "./Receta";
import { VideoInfo } from "./VideoInfo";

export interface Conversacion {
  id: string,
  titulo: string, // Ej: "Paella Valenciana"
  fecha: string,
  receta: Receta,
  video: VideoInfo | null
}