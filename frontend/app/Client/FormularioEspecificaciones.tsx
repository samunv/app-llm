"use client";

import { useState } from "react";
import { Especificaciones } from "../interfaces/Especificaciones";
import { useEspecificaciones } from "../contexts/EspecificacionesContext";
import { FormEvent } from "react"; // Necesario para manejar el evento del formulario con estado
import BotonGeneral from "./components/BotonGeneral";

type Props = {
  cerrar: () => void;
};

export default function FormularioEspecificaciones({ cerrar }: Props) {
  // Obtenemos la función de actualización del contexto
  const { especificaciones, setEspecificaciones, updateEspecificaciones } =
    useEspecificaciones();

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    cerrar();
  };

  const handleCerrar = () => {
    cerrar();
  };

  const handleUpdateEspecificaciones = (clave: string, valor: string) => {
    updateEspecificaciones(clave, valor);
  };

  return (
    <>
      <div className="fixed inset-0 bg-black opacity-80 z-[100]"></div>
      <form
        onSubmit={handleSubmit}
        className="border border-black rounded-xl p-10 fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white z-[101] flex flex-col items-center gap-3"
      >
        <h1 className="font-bold text-3xl bg-gradient-to-r from-orange-500 to-yellow-300 bg-clip-text text-transparent">
          Especificaciones
        </h1>

        <div className="flex flex-col gap-3">
          <div className="flex flex-row items-center gap-2">
            <label htmlFor="tipo_dieta">Tipo de Dieta:</label>
            <input
              type="text"
              id="tipo_dieta"
              name="tipo_dieta"
              placeholder="(Vegana, Carne...)"
              value={especificaciones?.tipo_dieta}
              onChange={(e)=>handleUpdateEspecificaciones("tipo_dieta", e.target.value)}
            />
          </div>

          <div className="flex flex-row items-center gap-2">
            <label htmlFor="restricciones">Restricciones:</label>
            <input
              type="text"
              id="restricciones"
              name="restricciones"
              placeholder="(Alimentos a evitar, alergias, salud...)"
              value={especificaciones?.restricciones}
              onChange={(e)=>handleUpdateEspecificaciones("restricciones", e.target.value)}
            />
          </div>

          <div className="flex flex-row items-center gap-2">
            <label htmlFor="objetivo">Objetivo:</label>
            <input
              type="text"
              id="objetivo"
              name="objetivo"
              placeholder="(Perder peso, ganar músculo...)"
              value={especificaciones?.objetivo}
              onChange={(e)=>handleUpdateEspecificaciones("objetivo", e.target.value)}
            />
          </div>
        </div>

        <div className="flex flex-row items-center gap-5">
          <BotonGeneral texto="Cerrar" onClick={handleCerrar}></BotonGeneral>

          <button
            className="font-bold cursor-pointer flex items-center p-4 bg-gradient-to-r from-[#E67E22] to-[#D35400] hover:from-[#D35400] hover:to-[#C0392B] text-white rounded-xl transition-all duration-300 hover:shadow-lg"
            type="submit"
          >
            Guardar y Cerrar
          </button>
        </div>
      </form>
    </>
  );
}
