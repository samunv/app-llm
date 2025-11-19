import { Receta } from "@/app/interfaces/Receta";
import { SolicitudReceta } from "@/app/interfaces/SolicitudReceta";

export const enviarReceta = async (
  solicitudReceta: SolicitudReceta
): Promise<{respuesta: Receta, estado: string}> => {
  if (!solicitudReceta?.comida || solicitudReceta.comida.trim() === "") {
    throw new Error("El campo 'comida' es obligatorio");
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

    const data = await response.json()

    return data;
  } catch (error) {
    throw error;
  }
};
