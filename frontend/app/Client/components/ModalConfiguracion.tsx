"use client";
import { useState, useEffect } from "react";
import { PerfilUsuario } from "@/app/interfaces/PerfilUsuario";
import { FaUser, FaBan, FaLeaf, FaXmark, FaFloppyDisk } from "react-icons/fa6";

type Props = {
  perfilActual: PerfilUsuario;
  guardar: (p: PerfilUsuario) => void;
  cerrar: () => void;
};

export default function ModalConfiguracion({ perfilActual, guardar, cerrar }: Props) {
  const [form, setForm] = useState<PerfilUsuario>(perfilActual);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" onClick={cerrar}></div>
      <div className="relative w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 animate-scaleIn border border-orange-100">
        
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <FaUser className="text-[#E67E22]" /> Perfil de Chef
          </h2>
          <button onClick={cerrar} className="text-gray-400 hover:text-gray-600">
            <FaXmark size={24} />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Tu Nombre</label>
            <input name="nombre" value={form.nombre} onChange={handleChange} placeholder="Ej: Álvaro" className="w-full p-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-[#E67E22] outline-none transition-colors" />
          </div>
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1 flex gap-2 items-center"><FaBan className="text-red-400"/> Alergias / Intolerancias</label>
            <input name="alergias" value={form.alergias} onChange={handleChange} placeholder="Ej: Gluten, Cacahuetes..." className="w-full p-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-red-400 outline-none transition-colors" />
          </div>
          <div>
             <label className="block text-sm font-bold text-gray-700 mb-1 flex gap-2 items-center"><FaLeaf className="text-green-500"/> Dieta Habitual</label>
            <input name="dietaGeneral" value={form.dietaGeneral} onChange={handleChange} placeholder="Ej: Vegana, Keto, Mediterránea..." className="w-full p-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-green-500 outline-none transition-colors" />
          </div>
        </div>

        <div className="mt-8 flex gap-3">
            <button onClick={cerrar} className="flex-1 py-3 text-gray-500 font-bold hover:bg-gray-100 rounded-xl transition-colors">Cancelar</button>
            <button onClick={() => guardar(form)} className="flex-[2] py-3 bg-gradient-to-r from-[#E67E22] to-[#D35400] text-white font-bold rounded-xl shadow-lg hover:shadow-orange-500/30 transition-all flex justify-center items-center gap-2">
                <FaFloppyDisk /> Guardar Perfil
            </button>
        </div>
      </div>
    </div>
  );
}