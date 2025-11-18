"use client";

import { FormEvent, useEffect, useState } from "react";
import { useEspecificaciones } from "../contexts/EspecificacionesContext";
import { FaLeaf, FaBan, FaBullseye, FaXmark, FaCheck } from "react-icons/fa6";
import { IoSparkles } from "react-icons/io5";

type Props = {
  cerrar: () => void;
};

export default function FormularioEspecificaciones({ cerrar }: Props) {
  const { especificaciones, updateEspecificaciones } = useEspecificaciones();
  const [animarSalida, setAnimarSalida] = useState(false);

  // Manejar el cierre con animación
  const handleCerrar = () => {
    setAnimarSalida(true);
    setTimeout(() => cerrar(), 300); // Espera a que termine la animación
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleCerrar();
  };

  const handleUpdate = (clave: string, valor: string) => {
    updateEspecificaciones(clave, valor);
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 overflow-y-auto">
      {/* Overlay con efecto Blur y Fade */}
      <div 
        className={`fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300 ${animarSalida ? 'opacity-0' : 'opacity-100'}`}
        onClick={handleCerrar}
      ></div>

      {/* Modal Principal */}
      <form
        onSubmit={handleSubmit}
        className={`
          relative w-full max-w-md bg-white rounded-3xl shadow-2xl 
          transform transition-all duration-300 ease-out
          border border-white/20
          ${animarSalida ? 'scale-95 opacity-0 translate-y-4' : 'scale-100 opacity-100 translate-y-0 animate-scaleIn'}
        `}
      >
        {/* Botón de cierre flotante (X) */}
        <button
          type="button"
          onClick={handleCerrar}
          className="absolute top-4 right-4 p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors z-10"
        >
          <FaXmark size={20} />
        </button>

        {/* Cabecera Decorativa */}
        <div className="p-8 pb-2 text-center">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-orange-50 text-[#E67E22] mb-4 shadow-inner">
            <IoSparkles size={26} />
          </div>
          <h2 className="text-3xl font-bold text-gray-800 mb-1">
            Detalles del Chef
          </h2>
          <p className="text-gray-500 text-sm">
            Personaliza cómo la IA generará tu receta
          </p>
        </div>

        {/* Campos del Formulario */}
        <div className="p-8 space-y-5">
          
          {/* Input: Tipo de Dieta */}
          <div className="group">
            <label htmlFor="tipo_dieta" className="block text-sm font-semibold text-gray-700 mb-1.5 ml-1">
              Tipo de Dieta
            </label>
            <div className="relative transition-all duration-300 focus-within:transform focus-within:scale-[1.02]">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <FaLeaf className="text-gray-400 group-focus-within:text-[#E67E22] transition-colors" />
              </div>
              <input
                type="text"
                id="tipo_dieta"
                placeholder="Ej: Vegana, Keto, Mediterránea..."
                className="block w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 placeholder-gray-400 focus:outline-none focus:bg-white focus:border-[#E67E22] focus:ring-4 focus:ring-[#E67E22]/10 transition-all"
                value={especificaciones?.tipo_dieta}
                onChange={(e) => handleUpdate("tipo_dieta", e.target.value)}
              />
            </div>
          </div>

          {/* Input: Restricciones */}
          <div className="group">
            <label htmlFor="restricciones" className="block text-sm font-semibold text-gray-700 mb-1.5 ml-1">
              Restricciones / Alergias
            </label>
            <div className="relative transition-all duration-300 focus-within:transform focus-within:scale-[1.02]">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <FaBan className="text-gray-400 group-focus-within:text-red-500 transition-colors" />
              </div>
              <input
                type="text"
                id="restricciones"
                placeholder="Ej: Sin gluten, nueces, lactosa..."
                className="block w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 placeholder-gray-400 focus:outline-none focus:bg-white focus:border-red-400 focus:ring-4 focus:ring-red-500/10 transition-all"
                value={especificaciones?.restricciones}
                onChange={(e) => handleUpdate("restricciones", e.target.value)}
              />
            </div>
          </div>

          {/* Input: Objetivo */}
          <div className="group">
            <label htmlFor="objetivo" className="block text-sm font-semibold text-gray-700 mb-1.5 ml-1">
              Objetivo Nutricional
            </label>
            <div className="relative transition-all duration-300 focus-within:transform focus-within:scale-[1.02]">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <FaBullseye className="text-gray-400 group-focus-within:text-blue-500 transition-colors" />
              </div>
              <input
                type="text"
                id="objetivo"
                placeholder="Ej: Alto en proteína, bajo en carbos..."
                className="block w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 placeholder-gray-400 focus:outline-none focus:bg-white focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 transition-all"
                value={especificaciones?.objetivo}
                onChange={(e) => handleUpdate("objetivo", e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Footer de Botones */}
        <div className="p-8 pt-2 flex items-center gap-3">
          <button
            type="button"
            onClick={handleCerrar}
            className="flex-1 px-4 py-3.5 rounded-xl border-2 border-gray-200 text-gray-600 font-bold hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800 transition-all duration-200 active:scale-95"
          >
            Cancelar
          </button>

          <button
            type="submit"
            className="flex-[2] px-4 py-3.5 rounded-xl bg-gradient-to-r from-[#E67E22] to-[#D35400] text-white font-bold shadow-lg shadow-orange-500/20 hover:shadow-orange-500/40 hover:from-[#D35400] hover:to-[#C0392B] transition-all duration-200 active:scale-95 flex items-center justify-center gap-2"
          >
            <FaCheck className="text-lg" />
            Guardar Preferencias
          </button>
        </div>
      </form>

      {/* Estilos Inline para la animación de entrada */}
      <style jsx>{`
        @keyframes scaleIn {
          0% {
            opacity: 0;
            transform: scale(0.9) translateY(10px);
          }
          100% {
            opacity: 1;
            transform: scale(1) translateY(0);
          }
        }
        .animate-scaleIn {
          animation: scaleIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
      `}</style>
    </div>
  );
}