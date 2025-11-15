"use client";

import { useEffect, useState } from "react";
import { Comida } from "../interfaces/Comida";
import Image from "next/image";
import SugerenciaComponent from "./components/SugerenciaComponent";
import { FaPaperPlane } from "react-icons/fa6";
import { useComida } from "../contexts/ComidaContext";

import "./Inicio.css";

export default function Inicio() {
  const [comidas, setComidas] = useState<Comida[]>([]);
  const [modelos, setModelos] = useState<[]>([]);
  const [valorBusqueda, setValorBusqueda] = useState<string>("");
  const { comida, setComida } = useComida();

  useEffect((): void => {
    function settearComidas() {
      setComidas([
        {
          nombre: "Paella",
          foto: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS627Z6NYbA6MxUpEsZrFc1slfe6Z4Wmw4o0Q&s",
          pais: "España",
        },
        {
          nombre: "Sushi",
          foto: "https://assets.tmecosys.com/image/upload/t_web_rdp_recipe_584x480_1_5x/img/recipe/ras/Assets/2F60018A-7D11-48CA-BB83-B32497E02BF5/Derivates/bc77ea56-073d-4648-82a4-0782bbf1d37c.jpg",
          pais: "Japón",
        },
        {
          nombre: "Tacos al Pastor",
          foto: "https://comedera.com/wp-content/uploads/sites/9/2017/08/tacos-al-pastor-receta.jpg",
          pais: "México",
        },
      ]);
    }

    settearComidas();
  }, []);

  useEffect(() => {
    if (comida != null || comida != undefined) {
      function establecerComidaSeleccionadaEnBuscador(comidaNombre: string) {
        setValorBusqueda("Prepárame una receta para " + comidaNombre);
      }
      establecerComidaSeleccionadaEnBuscador(String(comida?.nombre));
    }
  }, [comida]);

  return (
    <main className="flex flex-col items-center !w-full gap-4">
      <div className="flex flex-row-reverse items-center gap-1">
        <h1
          className="text-6xl 
      font-bold 
      // 1. Aplicar degradado de fondo (de naranja oscuro a amarillo)
      bg-gradient-to-r from-orange-500 to-yellow-300 
      // 2. Recortar el fondo para que solo se aplique al texto
      bg-clip-text 

      // 3. Hacer el texto transparente para que se vea el degradado de fondo
      text-transparent
      // 4. Asegurar que no hay un color de texto por defecto que lo tape
      inline-block"
        >
          ChefGPT
        </h1>
        <svg
          viewBox="0 0 24 24"
          fill="none"
          width={70}
          xmlns="http://www.w3.org/2000/svg"
        >
          <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
          <g
            id="SVGRepo_tracerCarrier"
            strokeLinecap="round"
            strokeLinejoin="round"
          ></g>
          <g id="SVGRepo_iconCarrier">
            {" "}
            <path
              d="M7 5C4.23858 5 2 7.23858 2 10C2 12.0503 3.2341 13.8124 5 14.584V17.25H19L19 14.584C20.7659 13.8124 22 12.0503 22 10C22 7.23858 19.7614 5 17 5C16.7495 5 16.5033 5.01842 16.2626 5.05399C15.6604 3.27806 13.9794 2 12 2C10.0206 2 8.33961 3.27806 7.73736 5.05399C7.49673 5.01842 7.25052 5 7 5Z"
              className="fill-orange-500"
            ></path>{" "}
            <path
              d="M18.9983 18.75H5.00169C5.01188 20.1469 5.08343 20.9119 5.58579 21.4142C6.17157 22 7.11438 22 9 22H15C16.8856 22 17.8284 22 18.4142 21.4142C18.9166 20.9119 18.9881 20.1469 18.9983 18.75Z"
              className="fill-orange-500"
            ></path>{" "}
          </g>
        </svg>
      </div>
      {/** SECCIÓN DE MENSAJES (CHAT) */}
      {/* <div className="">
          
        </div> */}

      {/** INPUT ESCRIBIR TEXTO */}
      <h1
        className="text-[#322f2f] text-3xl text-center focus-within:border-orange-500   
            focus-within:ring-2 
            focus-within:ring-orange-500 "
      >
        ¡Hola! soy tu chef de recetas,
      </h1>
      <div
        className="
                    bg-white text-black p-3 border border-[#d0c19f] 
                    rounded-2xl flex flex-row items-center w-[700px] gap-2
                    shadow-lg
                    focus-within:border-orange-500   
                    focus-within:ring-1
                    focus-within:ring-orange-500
                    
                    h-[65px]
                    /* ---------------------------------- */
                    "
      >
        <select className="rounded-[7px] p-2 !h-max transition-colors duration-200 text-sm ml-2 cursor-pointer bg-[#E6E3D6] text-[#73726C]">
          <option value="">Modelo 1</option>
          <option value="">Modelo 2</option>
        </select>
        <input
          type="text"
          placeholder="¿qué vamos a preparar hoy?"
          className="placeholder:text-gray-400 flex-1 outline-none text-md bg-transparent"
          value={valorBusqueda}
          onChange={(e) => setValorBusqueda(e.target.value)}
        />

        {/* Selector de modelo de IA */}

        {valorBusqueda != "" ? (
          <button className="scale-up-center bg-orange-500 rounded-[30px] p-2 px-3 text-white cursor-pointer hover:bg-orange-600">
            <FaPaperPlane size={20} />
          </button>
        ) : (
          ""
        )}
      </div>

      {/*ZONA DE SUGERENCIAS DE PLATOS PARA COCINAR*/}
      <div className="mt-5">
        <h2 className="text-center !mb-3 text-[gray]">Sugerencias para probar</h2>
        <div className="flex flex-row items-center gap-4">
          {comidas.map((comida: Comida, index) => (
            <SugerenciaComponent comidaObtenida={comida} key={index} />
          ))}
        </div>
      </div>
    </main>
  );
}
