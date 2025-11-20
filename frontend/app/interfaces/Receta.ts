export interface Receta{
    nombrePlato:string,
    ingredientes: string[],
    pasos?:string[],
    especificaciones?:string,
    error?: string
}