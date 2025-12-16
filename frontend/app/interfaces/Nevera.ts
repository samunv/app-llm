import { Ingrediente } from "./Receta";

export interface Nevera{
    uid_usuario: string,
    ingredientes_disponibles: Ingrediente[],
    observaciones?: string
}