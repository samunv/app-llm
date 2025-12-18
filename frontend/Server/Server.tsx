import { Especificaciones } from "@/app/interfaces/Especificaciones";
import { Receta } from "@/app/interfaces/Receta";
import { SolicitudReceta } from "@/app/interfaces/SolicitudReceta";
import { VideoInfo } from "@/app/interfaces/VideoInfo";

// Definimos la nueva estructura de respuesta del Backend
export interface RespuestaBackend {
  respuesta?: Receta | string | "error";
  video?: VideoInfo;
  tipo?: "receta" | "chat" | "error";
  estado?: string;
  error?: string;
}

export const enviarReceta = async (
  solicitudReceta: SolicitudReceta
): Promise<RespuestaBackend> => {
  if (!solicitudReceta?.prompt && !solicitudReceta.imagen) {
    throw new Error("La solicitud de receta está vacía.");
  }

  if(!verificarCantidadMensajesHistorial(solicitudReceta.historial!)){
    return {
      error: "Has alcanzado el límite de conversación. Por favor, inicia una nueva haciendo click en 'Nueva receta'."
    }
  }

  console.log("Enviando >>> ", solicitudReceta);

  switch (solicitudReceta.modeloIASeleccionado) {
    case "yt-receta":
      return fetchGenerarRecetaDeVideoYouTube(solicitudReceta);

    case "nevera":
      return {
        error: "este modelo no está disponible en este momento.",
      };

    case "imagenes":
      if (!solicitudReceta.imagen || !solicitudReceta.tipoImagen) {
        return {
          error: "Debes incluir una imágen en tu solicitud.",
        };
      } else {
        return {
          error: "este modelo no está disponible en este momento.",
        };
      }

    default:
      return fetchGenerarRecetaNormal(solicitudReceta);
  }
};

function verificarCantidadMensajesHistorial(historial:Array<{ role: string; parts: { text: string }[] }>):boolean {
  if (historial.length >= 8){
    return false
  }
  return true
}

async function fetchGenerarRecetaNormal(
  solicitudReceta: SolicitudReceta
): Promise<RespuestaBackend> {
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
}

async function fetchGenerarRecetaDeVideoYouTube(solicitudReceta: SolicitudReceta): Promise<RespuestaBackend> {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/ia-video-yt", {
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
}
