import { useComida } from "@/app/contexts/ComidaContext";
import { Comida } from "../../interfaces/Comida";
import { useSolicitudReceta } from "@/app/contexts/SolicitudRecetaContext";
import { SolicitudReceta } from "@/app/interfaces/SolicitudReceta";

type Props = {
  comidaObtenida: Comida;
};

export default function SugerenciaComponent({ comidaObtenida }: Props) {
  const { setSolicitudReceta } = useSolicitudReceta();
  return (
    <div
      className="!p-4 rounded-[15px]  bg-[#e6e3d6] flex flex-col items-stretch gap-1 cursor-pointer hover:scale-105 transition-all duration-100"
      // onClick={() => {
      //   setSolicitudReceta((prev: SolicitudReceta | null) => {
      //     if (!prev) {
      //       return {
      //         comida: String(comidaObtenida.nombre),
      //       };
      //     }
      //     return {
      //       ...prev,
      //       comida: String(comidaObtenida.nombre),
      //     };
      //   });
      // }}
    >
      {/* <h3 className="text-[#73726C]">
        <strong>{comidaObtenida.nombre}</strong> •{" "}
        <span>{comidaObtenida.pais}</span>
      </h3>
      <img
        src={comidaObtenida.foto}
        className="object-cover w-[170px] h-[120px] rounded-[7px] border border-white"
      /> */}
    </div>
  );
}
