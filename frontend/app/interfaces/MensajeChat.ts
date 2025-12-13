import { Receta } from "./Receta";
import { VideoInfo } from "./VideoInfo";

export interface MensajeChat {
  id: string,
  rol: "usuario" | "ia",
  tipo: "texto" | "receta" | "error",
  contenido: string | Receta,
  video?: VideoInfo | null,
  imagen?:string
}