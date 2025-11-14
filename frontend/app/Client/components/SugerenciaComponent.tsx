import { useComida } from "@/app/contexts/ComidaContext";
import { Comida } from "./../../Comida";

type Props = {
  comidaObtenida: Comida;
};

export default function SugerenciaComponent({ comidaObtenida }: Props) {
  const { comida, setComida } = useComida();
  return (
    <div
      className="!p-4 rounded-[15px]  bg-[#e6e3d6] flex flex-col items-center gap-1 cursor-pointer hover:scale-105 transition-all duration-100"
      onClick={() => setComida(comidaObtenida)}
    >
      <h3 className="text-[#73726C]">
        <strong>{comidaObtenida.nombre}</strong> •{" "}
        <span>{comidaObtenida.pais}</span>
      </h3>
      <img
        src={comidaObtenida.foto}
        className="object-cover w-[170px] h-[120px] rounded-[7px] border border-white"
      />
    </div>
  );
}
