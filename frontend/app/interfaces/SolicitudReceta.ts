import { Especificaciones } from './Especificaciones';

export interface SolicitudReceta {
    comida?: string,
    imagen?: string, // debe codificarse en Base64 
    especificaciones?: Especificaciones | undefined,
    modeloIASeleccionado?: string
}