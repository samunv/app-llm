import { RecetaIA } from "../interfaces/RecetaIA";
import { SolicitudReceta } from "../interfaces/SolicitudReceta";

export async function enviarSolicitud(solicitudReceta: SolicitudReceta): Promise<RecetaIA> {
    const URL = "http://localhost:5000/api/obtener-receta";

    try {
        const response = await fetch(URL, {
            method: 'POST', // Enviar por POST
            headers: {
                // Indicar que el cuerpo es JSON
                'Content-Type': 'application/json', 
            },
            // Enviar el objeto solicitudReceta en formato JSON
            body: JSON.stringify(solicitudReceta), 
        });

        if (!response.ok) {
            // Intenta leer el mensaje de error del backend
            const errorData = await response.json(); 
            throw new Error(`Error ${response.status}: ${errorData.detail || 'Fallo en el servidor.'}`);
        }

        const data: RecetaIA = await response.json();
        return data;

    } catch (error) {
        console.error("Error al enviar la solicitud de receta:", error);
        throw error;
    }
}