export interface Receta{
    nombrePlato:string,
    ingredientes:Ingrediente[],
    pasos?:string[],
    especificaciones?:string
}
export interface Ingrediente{
    nombre:string,
    cantidad:string | number,
    unidadMedida:string
}