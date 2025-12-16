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

  console.log("Enviando >>> ", solicitudReceta);

  if (solicitudReceta.modeloIASeleccionado === "yt-receta") {
    return fetchGenerarRecetaDeVideoYouTube({
      prompt_url: solicitudReceta.prompt,
    });
  } else if (solicitudReceta.modeloIASeleccionado === "nevera") {
    return { error: "este modelo no está disponible en este momento." };
  } else if (solicitudReceta.modeloIASeleccionado === "imagenes") {
    if (!solicitudReceta.imagen || !solicitudReceta.tipoImagen) {
      return { error: "Debes incluir una imágen en tu solicitud." };
    } else {
      return { error: "este modelo no está disponible en este momento." };
    }
  } else {
    return fetchGenerarRecetaNormal(solicitudReceta);
  }
};

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

async function fetchGenerarRecetaDeVideoYouTube(prompt_url: {
  prompt_url: string;
}): Promise<RespuestaBackend> {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/ia-video-yt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(prompt_url),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error en fetch:", error);
    throw error;
  }
}
