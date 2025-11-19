import { Especificaciones } from './Especificaciones';

export interface SolicitudReceta {
    comida?: string,
    tipoImagen?: string, //png o jpeg
    imagen?: string, // debe codificarse en Base64 
    especificaciones?: Especificaciones | undefined,
    modeloIASeleccionado?: string
}