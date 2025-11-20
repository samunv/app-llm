import { Receta } from "./Receta";

export interface MensajeChat {
  id: string;
  rol: "usuario" | "ia";
  tipo: "texto" | "receta" | "error";
  contenido: string | Receta;
}