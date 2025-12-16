"use client";

import { JSX } from "react";
import { BiSolidFridge } from "react-icons/bi";
import { FaStar, FaYoutube } from "react-icons/fa6";
import { MdPermMedia } from "react-icons/md";

export default function Caracteristicas() {
  return (
    <section className="flex flex-row justify-between gap-5 mt-6 mb-4 max-w-[750px]">
      <BloqueCaracteristica
        titulo="Personalización"
        descripcion="Recetas adaptadas a tus gustos y necesidades."
        icono={<FaStar className="text-orange-500" size={30} />}
      />
      <BloqueCaracteristica
        titulo="Multimedia"
        descripcion="Envía imágenes; o vídeos de YouTube de Recetas para obtener recetas estructuradas."
        icono={<MdPermMedia className="text-orange-500" size={30}/>}
      />
      <BloqueCaracteristica
        titulo="Nevera"
        descripcion="Recetas adaptadas a los ingredientes de tu nevera."
        icono={<BiSolidFridge className="text-orange-500" size={30}/>}
      />
    </section>
  );
}

type BloqueCaracteristicaProps = {
  titulo: string;
  descripcion: string;
  icono: JSX.Element;
};
function BloqueCaracteristica({
  titulo,
  descripcion,
  icono,
}: BloqueCaracteristicaProps) {
  return (
    <div className="flex-1 flex flex-col items-center justify-between text-center p-4  rounded-xl shadow-md bg-white border border-gray-300">
      <div>
 <h2 className="font-bold bg-gradient-to-r from-orange-500 to-yellow-300 bg-clip-text text-transparent text-[18px]">{titulo}</h2>
      <p className="text-[14px] text-[#101828]">{descripcion}</p>
      </div>
     
      <span className="mt-2">{icono}</span>
    </div>
  );
}
