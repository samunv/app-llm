'use server';
import { Especificaciones } from "@/app/interfaces/Especificaciones";
import { Receta } from "@/app/interfaces/Receta";
import { SolicitudReceta } from "@/app/interfaces/SolicitudReceta";
import { VideoInfo } from "@/app/interfaces/VideoInfo";

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

  if(!verificarLongitudPrompt(solicitudReceta.prompt)){
    return {error:"Tu prompt no debe exceder los 200 caracteres."}
  }

  if(!verificarCantidadMensajesHistorial(solicitudReceta.historial!)){
    return {
      error: "Has alcanzado el límite de conversación. Por favor, inicia una nueva haciendo click en 'Nueva receta'."
    }
  }

  if (solicitudReceta.imagen && solicitudReceta.imagen.length > 5 * 1024 * 1024) {
    return { error: "La imagen es demasiado pesada. No debe superar los 5MB." };
  }

  console.log("Enviando >>> ", solicitudReceta);

  switch (solicitudReceta.modeloIASeleccionado) {
    case "yt-receta":
      return fetchGenerarRecetaDeVideoYouTube(solicitudReceta);

    case "nevera":
      return fetchGenerarRecetaNevera(solicitudReceta);

    case "imagenes":
      if (!solicitudReceta.imagen || !solicitudReceta.tipoImagen) {
        return {
          error: "Debes incluir una imágen en tu solicitud.",
        };
      } else {
        return fetchGenerarRecetaDeImagen(solicitudReceta);
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
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(solicitudReceta),
    });
    return await response.json();
  } catch (error) {
    console.error("Error en fetch:", error);
    throw error;
  }
}

async function fetchGenerarRecetaDeVideoYouTube(solicitudReceta: SolicitudReceta): Promise<RespuestaBackend> {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/ia-video-yt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(solicitudReceta),
    });
    return await response.json();
  } catch (error) {
    console.error("Error en fetch:", error);
    throw error;
  }
}

async function fetchGenerarRecetaNevera(solicitudReceta: SolicitudReceta): Promise<RespuestaBackend> {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/ia-nevera", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(solicitudReceta),
    });
    return await response.json();
  } catch (error) {
    console.error("Error en fetch:", error);
    throw error;
  }
}

function verificarLongitudPrompt(prompt:string): boolean{
  if(prompt.length <= 200){
    return true
  }
  return false
}

async function fetchGenerarRecetaDeImagen(solicitudReceta: SolicitudReceta): Promise<RespuestaBackend> {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/ia-imagenes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(solicitudReceta),
    });
    return await response.json();
  } catch (error) {
    console.error("Error en fetch:", error);
    throw error;
  }
}
