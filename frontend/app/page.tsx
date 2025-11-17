import Image from "next/image";
import Inicio from "./Client/Inicio";
import { ComidaProvider } from "./contexts/ComidaContext";
import { SolicitudRecetaProvider } from "./contexts/SolicitudRecetaContext";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#FAF9F5] font-sans">
      <SolicitudRecetaProvider>
        <ComidaProvider>
          <Inicio />
        </ComidaProvider>
      </SolicitudRecetaProvider>
    </div>
  );
}
