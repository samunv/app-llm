import { Conversacion } from "@/app/interfaces/Conversacion";
import { FaPlus, FaTrash, FaMessage, FaBars, FaXmark, FaGear } from "react-icons/fa6";
import { IoSparkles } from "react-icons/io5";

type Props = {
  isOpen: boolean;
  toggleSidebar: () => void;
  historial: Conversacion[];
  cargarConversacion: (conv: Conversacion) => void;
  borrarConversacion: (id: string, e: React.MouseEvent) => void;
  nuevaConversacion: () => void;
  abrirAjustes: () => void; // <--- NUEVA PROP
};

export default function Sidebar({
  isOpen,
  toggleSidebar,
  historial,
  cargarConversacion,
  borrarConversacion,
  nuevaConversacion,
  abrirAjustes, // <--- Recibimos la función
}: Props) {
  return (
    <>
      {/* Botón flotante para ABRIR el menú (Solo visible cuando está cerrado) */}
      {!isOpen && (
        <button
          onClick={toggleSidebar}
          className="fixed top-6 left-6 z-50 p-3 text-[#343A40] hover:bg-orange-50 hover:text-[#E67E22] rounded-xl transition-all shadow-sm border border-transparent hover:border-orange-100"
        >
          <FaBars size={20} />
        </button>
      )}

      {/* CONTENEDOR DEL SIDEBAR */}
      <div
        className={`fixed inset-y-0 left-0 z-40 w-[300px] bg-white/95 backdrop-blur-md text-[#343A40] transform transition-transform duration-300 ease-in-out shadow-2xl border-r border-orange-100 flex flex-col
        ${isOpen ? "translate-x-0" : "-translate-x-full"}`}
      >
        {/* Cabecera Sidebar (Botón cerrar y Logo pequeño) */}
        <div className="p-5 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-lg tracking-tight">
            <span className="text-[#E67E22]">Chef</span>GPT
            <span className="text-xs bg-orange-100 text-orange-600 px-2 py-0.5 rounded-full">
              Historial
            </span>
          </div>
          <button
            onClick={toggleSidebar}
            className="p-2 text-gray-400 hover:text-[#E67E22] hover:bg-orange-50 rounded-lg transition-colors"
          >
            <FaXmark size={20} />
          </button>
        </div>

        {/* Botón Nueva Conversación (ESTILO MEJORADO) */}
        <div className="px-5 mb-6">
          <button
            onClick={() => {
              nuevaConversacion();
              if (window.innerWidth < 768) toggleSidebar();
            }}
            className="w-full flex items-center justify-center gap-2 px-4 py-3.5 bg-gradient-to-r from-[#E67E22] to-[#D35400] hover:from-[#D35400] hover:to-[#C0392B] text-white rounded-xl transition-all shadow-lg shadow-orange-500/20 hover:shadow-orange-500/40 active:scale-95 font-semibold text-sm"
          >
            <FaPlus />
            Nueva receta
          </button>
        </div>

        {/* Lista de Recientes */}
        <div className="flex-1 overflow-y-auto px-3 custom-scrollbar">
          <h3 className="px-4 text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
            Recientes
          </h3>
          <div className="space-y-1">
            {historial.length === 0 && (
              <div className="px-4 py-8 text-center text-gray-400 text-sm flex flex-col items-center gap-2 opacity-60">
                <IoSparkles size={20} />
                <p>Tu historial aparecerá aquí</p>
              </div>
            )}

            {historial.map((conv) => (
              <div
                key={conv.id}
                onClick={() => cargarConversacion(conv)}
                className="group flex items-center justify-between px-4 py-3 rounded-xl hover:bg-orange-50 cursor-pointer transition-all duration-200 text-sm border border-transparent hover:border-orange-100"
              >
                <div className="flex items-center gap-3 overflow-hidden">
                  <FaMessage
                    className="text-gray-300 group-hover:text-[#E67E22] transition-colors"
                    size={14}
                  />
                  <span className="truncate max-w-[170px] text-gray-600 group-hover:text-gray-900 font-medium">
                    {conv.titulo}
                  </span>
                </div>

                {/* Botón borrar */}
                <button
                  onClick={(e) => borrarConversacion(conv.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-50 hover:text-red-500 rounded-md text-gray-400 transition-all"
                  title="Borrar"
                >
                  <FaTrash size={12} />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Footer Sidebar - BOTÓN DE AJUSTES AÑADIDO */}
        <div className="p-4 border-t border-gray-100 bg-gray-50/50">
          <button
            onClick={abrirAjustes}
            className="w-full flex items-center gap-3 p-2 text-sm text-gray-600 hover:text-[#E67E22] hover:bg-white rounded-lg transition-all font-medium group"
          >
            <FaGear className="group-hover:rotate-90 transition-transform duration-500" />
            <span>Configuración y Alérgenos</span>
          </button>
        </div>
      </div>

      {/* Overlay Móvil */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 md:hidden"
          onClick={toggleSidebar}
        ></div>
      )}
    </>
  );
}