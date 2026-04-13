"use client";

// 1. Quitamos el import estático de arriba:
// import html2pdf from "html2pdf.js"; 
import BotonGeneral from "./BotonGeneral";
import { LuDownload } from "react-icons/lu";

type Props = {
  htmlElement: string;
  fileName: string
};

export default function GeneradorPDF({ htmlElement, fileName }: Props) {
  const generarPDF = async () => { // Añadimos async
    const element = document.getElementById(htmlElement);

    if (!element) {
      console.error(`No se encontró el elemento con ID: ${htmlElement}`);
      return;
    }

    // 2. Importación dinámica justo antes de usarlo
    const html2pdf = (await import("html2pdf.js")).default;

    const opciones = {
      margin: 20,
      filename: fileName,
      image: {
        type: "jpeg",
        quality: 0.98,
      },
      html2canvas: {
        scale: 2,
      },
      jsPDF: {
        unit: "mm",
        format: "a4",
        orientation: "portrait",
      },
    } as const;

    // 3. Ahora html2pdf ya está disponible solo en el cliente
    html2pdf().set(opciones).from(element).save();
  };

  return (
    <BotonGeneral texto="Descargar PDF" onClick={generarPDF}>
      <LuDownload size={30} />
    </BotonGeneral>
  );
}