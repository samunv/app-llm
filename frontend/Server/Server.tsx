import { Receta } from "@/app/interfaces/Receta";
import { SolicitudReceta } from "@/app/interfaces/SolicitudReceta";

// Definimos la nueva estructura de respuesta del Backend
export interface RespuestaBackend {
  respuesta: Receta | string | "error"; // Puede ser objeto Receta O texto simple
  tipo: "receta" | "chat" | "error";
  estado: string;
  error?: string;
}

export const enviarReceta = async (
  solicitudReceta: SolicitudReceta
): Promise<RespuestaBackend> => {
  if (!solicitudReceta?.comida && !solicitudReceta.imagen) {
     // Permitimos enviar si hay imagen o texto (antes solo texto)
     // Si quieres ser estricto con el texto, descomenta la validación anterior
  }

  console.log("Enviando >>> ", solicitudReceta);

  try {
    const response = await fetch("http://127.0.0.1:5000/api/ia", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(solicitudReceta),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error en fetch:", error);
    throw error;
  }
};