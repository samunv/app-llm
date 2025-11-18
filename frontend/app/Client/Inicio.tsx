"use client";

import { useEffect, useState, useRef, JSX, useCallback } from "react";
import { Comida } from "../interfaces/Comida";
import Image from "next/image";
import SugerenciaComponent from "./components/SugerenciaComponent";
import { FaPaperPlane, FaChevronDown, FaCheck } from "react-icons/fa6";
import { SiGoogle } from "react-icons/si";
import { FaRobot, FaBolt, FaFlask, FaRocket } from "react-icons/fa";
import { useComida } from "../contexts/ComidaContext";
import { FaImage } from "react-icons/fa6";

import "./Inicio.css";
import { useSolicitudReceta } from "../contexts/SolicitudRecetaContext";
import { SolicitudReceta } from "./../interfaces/SolicitudReceta";
import { useEspecificaciones } from "../contexts/EspecificacionesContext";
import { IoIosAddCircle } from "react-icons/io";
import { Especificaciones } from "./../interfaces/Especificaciones";
import FormularioEspecificaciones from "./FormularioEspecificaciones";
import BotonGeneral from "./components/BotonGeneral";

interface Modelo {
  id: string;
  nombre: string;
  version: string;
  descripcion: string;
  velocidad: "ultrarrápido" | "rápido" | "equilibrado" | "potente";
  icono: JSX.Element;
  color: string;
  recomendado?: boolean;
}

const modelosGemini: Modelo[] = [
  {
    id: "gemini-2.5-flash",
    nombre: "Gemini 2.5 Flash",
    version: "Última Generación",
    descripcion: "Lo último de Google, perfecto para recetas innovadoras",
    velocidad: "ultrarrápido",
    icono: <FaRocket className="text-xl" />,
    color: "#EA4335",
    recomendado: true,
  },
  {
    id: "gemini-1.5-flash",
    nombre: "Gemini 1.5 Flash",
    version: "Generación Anterior",
    descripcion: "Rápido y eficiente, ideal para recetas del día a día",
    velocidad: "ultrarrápido",
    icono: <FaBolt className="text-xl" />,
    color: "#FBBC04",
  },
  {
    id: "gemini-1.5-pro",
    nombre: "Gemini 1.5 Pro",
    version: "Profesional",
    descripcion: "El más potente, para recetas complejas y detalladas",
    velocidad: "potente",
    icono: <SiGoogle className="text-xl" />,
    color: "#4285F4",
  },
];

export default function Inicio() {
  const [comidas, setComidas] = useState<Comida[]>([]);
  // const { comida, setComida } = useComida();
  const { solicitudReceta, updateSolicitudReceta, setModeloSeleccionadoID } =
    useSolicitudReceta();

  const [isOpen, setIsOpen] = useState(false);
  const [modeloSeleccionado, setModeloSeleccionado] = useState<Modelo>(
    modelosGemini[0]
  );
  const dropdownRef = useRef<HTMLDivElement>(null);

  const inputFileRef = useRef<HTMLInputElement>(null);

  const [imagenPreview, setImagenPreview] = useState<string>();

  const { especificaciones, setEspecificaciones } = useEspecificaciones();

  const [mostrarFormEspecificaciones, setMostrarFormEspecificaciones] =
    useState<boolean>(false);

  const handleClickImagen = () => {
    inputFileRef.current?.click();
  };

  const cerrarFormulario = () => {
    setMostrarFormEspecificaciones(false);
  };

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    const fileBase64: string = await convertirEnBase64(file);
    if (file) {
      updateSolicitudReceta("imagen", fileBase64);
    }

    const imageUrl = URL.createObjectURL(file as File);
    setImagenPreview(imageUrl);
  };

  function convertirEnBase64(file: File | undefined): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      // Cuando el FileReader termine de cargar...
      reader.onload = () => {
        // El resultado contiene el prefijo "data:image/jpeg;base64,"
        const base64Url = String(reader.result);
        // Extraer solo la parte Base64 (después de la coma)
        const base64Data = base64Url?.split(",")[1];
        resolve(base64Data);
      };

      // Manejo de errores
      reader.onerror = (error) => {
        reject(error);
      };

      // 3. Lee el archivo como una URL de datos
      reader.readAsDataURL(file as File);
    });
  }

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
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const updateSolicitudRecetaCallback = useCallback(
    (claveActualizar: string, valorActualizar: string) => {
      updateSolicitudReceta(claveActualizar, valorActualizar);
    },
    [updateSolicitudReceta]
  );

  useEffect(() => {
    if (modeloSeleccionado) {
      updateSolicitudRecetaCallback(
        "modeloIASeleccionado",
        modeloSeleccionado.id
      );
      setModeloSeleccionadoID(modeloSeleccionado.id);
    }
  }, [
    modeloSeleccionado,
    updateSolicitudRecetaCallback,
    setModeloSeleccionadoID,
  ]);

  const seleccionarModelo = (modelo: Modelo) => {
    setModeloSeleccionado(modelo);
    setIsOpen(false);
  };

  const getVelocidadConfig = (velocidad: string) => {
    switch (velocidad) {
      case "ultrarrápido":
        return { color: "text-green-600", emoji: "⚡⚡", bg: "bg-green-50" };
      case "rápido":
        return { color: "text-emerald-600", emoji: "⚡", bg: "bg-emerald-50" };
      case "equilibrado":
        return { color: "text-blue-600", emoji: "⚖️", bg: "bg-blue-50" };
      case "potente":
        return { color: "text-purple-600", emoji: "🔥", bg: "bg-purple-50" };
      default:
        return { color: "text-gray-600", emoji: "⭐", bg: "bg-gray-50" };
    }
  };

  return (
    <main className="flex flex-col items-center !w-full gap-4">
      <div className="flex flex-row-reverse items-center gap-1">
        <h1 className="text-6xl font-bold bg-gradient-to-r from-orange-500 to-yellow-300 bg-clip-text text-transparent inline-block">
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
            <path
              d="M7 5C4.23858 5 2 7.23858 2 10C2 12.0503 3.2341 13.8124 5 14.584V17.25H19L19 14.584C20.7659 13.8124 22 12.0503 22 10C22 7.23858 19.7614 5 17 5C16.7495 5 16.5033 5.01842 16.2626 5.05399C15.6604 3.27806 13.9794 2 12 2C10.0206 2 8.33961 3.27806 7.73736 5.05399C7.49673 5.01842 7.25052 5 7 5Z"
              className="fill-orange-500"
            ></path>
            <path
              d="M18.9983 18.75H5.00169C5.01188 20.1469 5.08343 20.9119 5.58579 21.4142C6.17157 22 7.11438 22 9 22H15C16.8856 22 17.8284 22 18.4142 21.4142C18.9166 20.9119 18.9881 20.1469 18.9983 18.75Z"
              className="fill-orange-500"
            ></path>
          </g>
        </svg>
      </div>

      <h1 className="text-[#343A40] text-3xl text-center font-medium">
        ¡Hola! soy tu chef de recetas,
      </h1>

      {/* {solicitudReceta ? (
        <div>
         
          <p>Comida: {solicitudReceta.comida}</p>

          
          <p>Modelo IA: {solicitudReceta.modeloIASeleccionado}</p>

          <p>Imagen : {solicitudReceta.imagen?.slice(0, 8)}</p>

          <p>
            Especificaciones :{" "}
            {especificaciones?.restricciones +
              " " +
              especificaciones?.tipo_dieta}
          </p>
        </div>
      ) : (
        // Opcional: Podrías mostrar un mensaje si el objeto es nulo.
        <p>No hay solicitud de receta definida.</p>
      )} */}

      <div className="bg-[#FDFBF5] text-[#343A40] p-3 border-2 border-[#8D6E63]/30 rounded-2xl flex flex-row items-center w-[700px] gap-3 shadow-lg focus-within:border-[#E67E22] focus-within:ring-2 focus-within:ring-[#E67E22]/30 transition-all duration-300 min-h-[65px]">
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex items-center gap-2.5 px-3 py-2 bg-gradient-to-r from-[#E67E22] to-[#D35400] hover:from-[#D35400] hover:to-[#C0392B] text-white rounded-xl transition-all duration-300 shadow-md hover:shadow-lg border border-[#8D6E63]/10 min-w-[180px] group relative"
          >
            {modeloSeleccionado.recomendado && (
              <div className="absolute -top-1 -right-1 bg-yellow-400 text-[#343A40] text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow-sm">
                ⭐ NUEVO
              </div>
            )}

            <div
              className="p-1.5 bg-white/20 rounded-lg backdrop-blur-sm flex-shrink-0"
              style={{ color: modeloSeleccionado.color }}
            >
              {modeloSeleccionado.icono}
            </div>

            <div className="flex-1 text-left min-w-0">
              <div className="text-xs font-bold leading-tight truncate">
                {modeloSeleccionado.nombre}
              </div>
              <div className="text-[10px] opacity-90 leading-tight truncate">
                {modeloSeleccionado.version}
              </div>
            </div>

            <FaChevronDown
              className={`text-xs transition-transform duration-300 flex-shrink-0 ${
                isOpen ? "rotate-180" : ""
              }`}
            />
          </button>

          {isOpen && (
            <div className="absolute top-full left-0 mt-2 w-[420px] max-h-[150px] overflow-y-auto bg-white rounded-2xl shadow-2xl border-2 border-[#E67E22]/20 z-50 animate-fadeIn">
              <div className="sticky top-0 bg-gradient-to-r from-[#E67E22] to-[#D35400] px-4 py-3 z-10">
                <div className="flex items-center justify-between text-white">
                  <div className="flex items-center gap-2">
                    <FaRobot className="text-lg" />
                    <span className="font-bold text-sm">
                      Selecciona tu Chef de IA
                    </span>
                  </div>
                  <div className="flex items-center gap-1 text-xs bg-white/20 px-2 py-1 rounded-full backdrop-blur-sm">
                    <SiGoogle className="text-sm" />
                    <span className="font-semibold">Gemini</span>
                  </div>
                </div>
              </div>

              <div className="p-3">
                {modelosGemini.map((modelo) => {
                  const velocidadConfig = getVelocidadConfig(modelo.velocidad);

                  return (
                    <button
                      key={modelo.id}
                      onClick={() => seleccionarModelo(modelo)}
                      className={`w-full p-3.5 mb-2 rounded-xl flex items-start gap-3 transition-all duration-300 hover:scale-[1.01] hover:shadow-md border-2 relative ${
                        modeloSeleccionado.id === modelo.id
                          ? "bg-gradient-to-br from-[#E67E22]/10 via-[#D35400]/5 to-transparent border-[#E67E22] shadow-sm"
                          : "bg-white border-gray-200 hover:border-[#E67E22]/40"
                      }`}
                    >
                      {modelo.recomendado && (
                        <div className="absolute -top-1.5 -right-1.5 bg-gradient-to-r from-yellow-400 to-orange-400 text-white text-[9px] font-bold px-2 py-0.5 rounded-full shadow-md animate-pulse">
                          ⭐ RECOMENDADO
                        </div>
                      )}

                      <div
                        className="p-2.5 rounded-lg flex-shrink-0 shadow-sm"
                        style={{
                          backgroundColor: `${modelo.color}15`,
                          color: modelo.color,
                        }}
                      >
                        {modelo.icono}
                      </div>

                      <div className="flex-1 text-left min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <div className="flex-1 min-w-0">
                            <span className="font-bold text-[#343A40] text-sm block truncate">
                              {modelo.nombre}
                            </span>
                            <span className="text-[10px] text-[#8D6E63] font-medium">
                              {modelo.version}
                            </span>
                          </div>
                          {modeloSeleccionado.id === modelo.id && (
                            <FaCheck className="text-[#E67E22] text-sm animate-scaleIn flex-shrink-0 ml-2" />
                          )}
                        </div>

                        <div className="text-xs text-[#343A40]/75 mb-2 leading-relaxed">
                          {modelo.descripcion}
                        </div>

                        <div className="flex items-center gap-2">
                          <div
                            className={`text-[10px] font-bold px-2 py-1 rounded-full ${velocidadConfig.color} ${velocidadConfig.bg} border border-current/20`}
                          >
                            <span>
                              {velocidadConfig.emoji} {modelo.velocidad}
                            </span>
                          </div>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>

              {/* <div className="sticky bottom-0 bg-gradient-to-t from-gray-50 to-transparent px-4 py-3 rounded-b-2xl border-t border-gray-200/50">
                <p className="text-[10px] text-[#343A40]/60 text-center leading-relaxed">
                  <SiGoogle className="inline text-xs mr-1" />
                  Todos los modelos usan la API oficial de{" "}
                  <span className="font-semibold">Google Gemini</span>
                </p>
              </div> */}
            </div>
          )}
        </div>

        <input
          type="file"
          ref={inputFileRef}
          hidden
          accept="image/png, image/jpeg"
          onChange={handleFileChange} // cuando el usuario selecciona un archivo
        />
        <input
          type="text"
          placeholder="¿qué vamos a preparar hoy?"
          className="placeholder:text-[#8D6E63]/60 flex-1 outline-none text-base bg-transparent px-2"
          value={solicitudReceta?.comida ?? ""}
          onChange={(e) => {
            updateSolicitudRecetaCallback("comida", e.target.value);
          }}
        />

        {imagenPreview ? (
          <img
            src={imagenPreview}
            alt=""
            className="w-[50px] h-[50px] rounded-xl object-cover cursor-pointer border-2 border-[#DBD0C9]"
            onClick={handleClickImagen}
          />
        ) : (
          <button
            onClick={handleClickImagen}
            className="bg-[#e1ded3] rounded-xl flex flex-col items-center justify-center w-[50px] h-[50px] cursor-pointer"
          >
            <FaImage size={25} color="gray" />
          </button>
        )}

        {(solicitudReceta?.comida ?? "").trim().length > 0 &&
          solicitudReceta?.modeloIASeleccionado && (
            <button className="bg-gradient-to-r from-[#E67E22] to-[#D35400] hover:from-[#D35400] hover:to-[#C0392B] rounded-full p-2.5 px-4 text-white cursor-pointer transition-all duration-300 shadow-md hover:shadow-lg hover:scale-105 active:scale-95 flex-shrink-0">
              <FaPaperPlane size={18} />
            </button>
          )}
      </div>

      {/* <div className="mt-5">
        <h2 className="text-center mb-4 text-[#8D6E63] font-semibold text-sm">
          Sugerencias para probar
        </h2>
        <div className="flex flex-row items-center gap-4">
          {comidas.map((comida: Comida, index) => (
            <SugerenciaComponent comidaObtenida={comida} key={index} />
          ))}
        </div>
      </div> */}

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes scaleIn {
          from {
            transform: scale(0);
          }
          to {
            transform: scale(1);
          }
        }

        @keyframes pulse {
          0%,
          100% {
            opacity: 1;
          }
          50% {
            opacity: 0.8;
          }
        }

        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }

        .animate-scaleIn {
          animation: scaleIn 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        .animate-pulse {
          animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        div::-webkit-scrollbar {
          width: 6px;
        }

        div::-webkit-scrollbar-track {
          background: transparent;
        }

        div::-webkit-scrollbar-thumb {
          background: #e67e22;
          border-radius: 10px;
        }

        div::-webkit-scrollbar-thumb:hover {
          background: #d35400;
        }
      `}</style>

      <BotonGeneral
        texto="Añadir especificaciones"
        onClick={() => setMostrarFormEspecificaciones(true)}
      >
        <IoIosAddCircle size={20} />
      </BotonGeneral>

      {mostrarFormEspecificaciones && (
        <FormularioEspecificaciones cerrar={cerrarFormulario} />
      )}
    </main>
  );
}
