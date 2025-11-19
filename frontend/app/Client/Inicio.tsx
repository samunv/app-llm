"use client";

import { useEffect, useState, useRef, JSX, useCallback } from "react";
import { Comida } from "../interfaces/Comida";
import {
  FaPaperPlane,
  FaChevronDown,
  FaCheck,
  FaXmark,
  FaFilePdf,
} from "react-icons/fa6";
import { SiGoogle } from "react-icons/si";
import { FaRobot, FaBolt, FaRocket, FaImage } from "react-icons/fa";
import { IoIosAddCircle } from "react-icons/io";
import ReactMarkdown from "react-markdown";

import "./Inicio.css";
import { useSolicitudReceta } from "../contexts/SolicitudRecetaContext";
import { useEspecificaciones } from "../contexts/EspecificacionesContext";
import FormularioEspecificaciones from "./FormularioEspecificaciones";
import BotonGeneral from "./components/BotonGeneral";
import { modelosGemini } from "./modelos";
import { Modelo } from "../interfaces/Modelo";
import { enviarReceta } from "@/Server/Server";
import { SolicitudReceta } from "../interfaces/SolicitudReceta";
import remarkGfm from "remark-gfm";
import TypingText from "./components/TypingText";
import { Receta } from "../interfaces/Receta";
import GeneradorPDF from "./components/GeneradorPDF";

export default function Inicio() {
  const [comidas, setComidas] = useState<Comida[]>([]);

  // Contextos
  const { solicitudReceta, updateSolicitudReceta } = useSolicitudReceta();
  const { especificaciones } = useEspecificaciones();

  // Estados locales de UI
  const [isOpen, setIsOpen] = useState(false);
  const [modeloSeleccionado, setModeloSeleccionado] = useState<Modelo>(
    modelosGemini[0]
  );
  const [mostrarFormEspecificaciones, setMostrarFormEspecificaciones] =
    useState<boolean>(false);
  const [imagenPreview, setImagenPreview] = useState<string>();

  // Estados para la IA
  const [cargando, setCargando] = useState(false);
  const [respuestaIA, setRespuestaIA] = useState("");
  const [receta, setReceta] = useState<Receta>();

  // Referencias
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputFileRef = useRef<HTMLInputElement>(null);

  const handleEnviarReceta = async () => {
    if (solicitudReceta) {
      setCargando(true);
      setRespuestaIA("");
      try {
        const data = await enviarReceta(solicitudReceta);
        if (data.estado === "exito") {
          setRespuestaIA("Receta generada:");
          setReceta(data.respuesta as Receta);
          updateSolicitudRecetaCallback("comida", "");
        } else {
          setRespuestaIA("Hubo un error al generar la receta.");
        }
      } catch (error) {
        console.error("Error:", error);
        setRespuestaIA(
          "Error conectando con el servidor Python. Asegúrate de que 'python run.py' esté ejecutándose."
        );
      } finally {
        setCargando(false);
      }
    }
  };

  // --- MANEJADORES DE EVENTOS ---

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
    if (file) {
      const fileBase64: string = await convertirEnBase64(file);
      updateSolicitudReceta("imagen", fileBase64);
      const imageUrl = URL.createObjectURL(file);
      setImagenPreview(imageUrl);
    }
  };

  function convertirEnBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64Url = String(reader.result);
        obtenerTipoImagenDeImagen(base64Url);
        const base64Data = base64Url?.split(",")[1];
        resolve(base64Data);
      };
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file);
    });
  }

  function obtenerTipoImagenDeImagen(imagenBase64URL: string) {
    const match = imagenBase64URL.match(/^data:([^;]+);base64,/);

    if (match && match[1]) {
      updateSolicitudRecetaCallback("tipoImagen", match[1]);
    }
  }

  // useEffect(() => {
  //   // Datos mock iniciales
  //   setComidas([
  //     { nombre: "Paella", foto: "...", pais: "España" },
  //     { nombre: "Sushi", foto: "...", pais: "Japón" },
  //     { nombre: "Tacos", foto: "...", pais: "México" },
  //   ]);
  // }, []);

  // Cerrar dropdown al hacer click fuera
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

  // Sincronizar modelo seleccionado con el contexto
  useEffect(() => {
    if (modeloSeleccionado) {
      updateSolicitudRecetaCallback(
        "modeloIASeleccionado",
        modeloSeleccionado.id
      );
    }
  }, [modeloSeleccionado, updateSolicitudRecetaCallback]);

  return (
    <main className="flex flex-col items-center !w-full gap-6 pb-20">
      {/* CABECERA LOGO */}
      <div className="flex flex-row-reverse items-center gap-1 mt-10">
        <h1 className="text-6xl font-bold bg-gradient-to-r from-orange-500 to-yellow-300 bg-clip-text text-transparent inline-block">
          ChefGPT
        </h1>
        <svg
          viewBox="0 0 24 24"
          fill="none"
          width={70}
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M7 5C4.23858 5 2 7.23858 2 10C2 12.0503 3.2341 13.8124 5 14.584V17.25H19L19 14.584C20.7659 13.8124 22 12.0503 22 10C22 7.23858 19.7614 5 17 5C16.7495 5 16.5033 5.01842 16.2626 5.05399C15.6604 3.27806 13.9794 2 12 2C10.0206 2 8.33961 3.27806 7.73736 5.05399C7.49673 5.01842 7.25052 5 7 5Z"
            className="fill-orange-500"
          ></path>
          <path
            d="M18.9983 18.75H5.00169C5.01188 20.1469 5.08343 20.9119 5.58579 21.4142C6.17157 22 7.11438 22 9 22H15C16.8856 22 17.8284 22 18.4142 21.4142C18.9166 20.9119 18.9881 20.1469 18.9983 18.75Z"
            className="fill-orange-500"
          ></path>
        </svg>
      </div>

      {!respuestaIA && !cargando && (
        <h1 className="text-[#343A40] text-3xl text-center font-medium">
          ¡Hola! soy tu chef y hago recetas
          <TypingText
            frases={[" rápidas.", " creativas.", " personalizadas."]}
          />
        </h1>
      )}

      {respuestaIA && (
        <div className="w-[700px] bg-white p-8 rounded-3xl shadow-xl border-2 border-[#DCD3D0] animate-fadeIn mb-10">
          <div className="flex items-center gap-3 pb-4">
            <div className="flex flex-row items-center gap-2">
              <div
                className="p-2.5 rounded-lg flex-shrink-0 shadow-sm"
                style={{
                  backgroundColor: `${modeloSeleccionado.color}15`,
                  color: modeloSeleccionado.color,
                }}
              >
                {modeloSeleccionado.icono}
              </div>
              <h2 className="font-bold text-[#343A40]">
                {modeloSeleccionado.nombre}
              </h2>
            </div>
          </div>

          <div className="prose prose-orange max-w-none text-[#343A40]  leading-relaxed">
            <p>{respuestaIA}</p>
            {receta && receta.nombrePlato ? (
              <div>
                <div id="respuesta-receta" className="mb-5">
                  <h1 className="font-bold text-3xl">{receta.nombrePlato}</h1>
                  <hr className="mt-3 mb-3 border border-[#DCD3D0]" />
                  <h2 className="font-bold text-2xl">Ingredientes</h2>
                  <ul>
                    {receta.ingredientes?.map((ingrediente, index) => (
                      <li key={index}>{ingrediente}</li>
                    ))}
                  </ul>

                  <hr className="mt-3 mb-3 border border-[#DCD3D0]" />
                  <h2 className="font-bold text-2xl">Pasos</h2>
                  <ul>
                    {receta.pasos?.map((paso, index) => (
                      <li key={index}>
                        {index + 1 + ")"} {paso}
                      </li>
                    ))}
                  </ul>

                  {receta.especificaciones ? (
                    <>
                      <hr className="mt-3 mb-3 border border-[#DCD3D0]" />
                      <h2 className="font-bold text-2xl">Especificaciones</h2>
                      <p>{receta.especificaciones}</p>
                    </>
                  ) : (
                    ""
                  )}
                </div>
                <GeneradorPDF htmlElement="respuesta-receta" />
              </div>
            ) : (
              "Error al generar receta. Solo puedo realizar recetas de comida. Prueba a pedir una receta válida o prueba a cambiar de modelo."
            )}
          </div>
        </div>
      )}

      {/* BARRA DE ENTRADA PRINCIPAL */}

      <div
        className={
          respuestaIA
            ? "fixed bottom-5 left-1/2 transform -translate-x-1/2 bg-white text-[#343A40] p-3 border-2 border-[#8D6E63]/30 rounded-2xl flex flex-row items-center w-[750px] gap-3 shadow-lg z-50 focus-within:border-[#E67E22] min-h-[65px] z-20"
            : "bg-[white] text-[#343A40] p-3 border-2 border-[#8D6E63]/30 rounded-2xl flex flex-row items-center w-[750px] gap-3 shadow-lg focus-within:border-[#E67E22]  min-h-[65px] z-20"
        }
      >
        {/* Dropdown de Modelos */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex items-center gap-2.5 px-3 py-2 bg-gradient-to-r from-[#E67E22] to-[#D35400] hover:from-[#D35400] hover:to-[#C0392B] text-white rounded-xl transition-all duration-300 shadow-md hover:shadow-lg border border-[#8D6E63]/10 min-w-[180px] group relative"
          >
            {modeloSeleccionado.recomendado && (
              <div className="absolute -top-1 -right-1 bg-yellow-400 text-[white] text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow-sm">
                Recomendado
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
            <div
              className={`absolute left-0 w-[420px] max-h-[220px] overflow-y-auto bg-white rounded-2xl shadow-2xl border-2 border-2 border-[#DCD3D0] z-50 animate-fadeIn
              ${respuestaIA ? "bottom-full mb-2" : "top-full mt-1"}
              `}
            >
              {" "}
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
                          <span className="font-bold text-[#343A40] text-sm block truncate">
                            {modelo.nombre}
                          </span>
                          {modeloSeleccionado.id === modelo.id && (
                            <FaCheck className="text-[#E67E22] text-sm animate-scaleIn flex-shrink-0 ml-2" />
                          )}
                        </div>
                        <div className="text-xs text-[#343A40]/75 mb-2 leading-relaxed">
                          {modelo.descripcion}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        <input
          type="file"
          ref={inputFileRef}
          hidden
          onChange={handleFileChange}
        />

        <input
          type="text"
          placeholder="¿Qué vamos a preparar hoy?"
          className="placeholder:text-[#8D6E63]/60 flex-1 outline-none text-base bg-transparent px-2"
          value={solicitudReceta?.comida ?? ""}
          onChange={(e) =>
            updateSolicitudRecetaCallback("comida", e.target.value)
          }
          onKeyDown={(e) => e.key === "Enter" && handleEnviarReceta()}
        />
        <BotonGeneral texto="" onClick={() => {}}>
          <FaFilePdf size={20} />
        </BotonGeneral>
        <BotonGeneral
          texto=""
          onClick={() => setMostrarFormEspecificaciones(true)}
        >
          <IoIosAddCircle size={20} />
        </BotonGeneral>

        {modeloSeleccionado.id != "gemini-1.0-pro" ? (
          <div>
            {imagenPreview ? (
              <div className="relative">
                <img
                  src={imagenPreview}
                  alt="Preview"
                  className="w-[50px] h-[50px] rounded-xl object-cover cursor-pointer border-2 border-[#DBD0C9]"
                  onClick={handleClickImagen}
                />
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setImagenPreview(undefined);
                    updateSolicitudReceta("imagen", "");
                  }}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-5 h-5 flex items-center justify-center text-xs"
                >
                  ✕
                </button>
              </div>
            ) : (
              <button
                onClick={handleClickImagen}
                className="bg-[#e1ded3] hover:bg-[#d4d1c6] transition-colors rounded-xl flex flex-col items-center justify-center w-[50px] h-[50px] cursor-pointer"
                title="Subir foto de comida"
              >
                <FaImage size={20} color="#8D6E63" />
              </button>
            )}
          </div>
        ) : (
          ""
        )}

        <button
          onClick={handleEnviarReceta}
          disabled={cargando || !solicitudReceta?.comida}
          className={`bg-gradient-to-r from-[#E67E22] to-[#D35400] hover:from-[#D35400] hover:to-[#C0392B] rounded-full p-3 text-white cursor-pointer transition-all duration-300 shadow-md hover:shadow-lg hover:scale-105 active:scale-95 flex-shrink-0 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          {cargando ? (
            <div className="w-[18px] h-[18px] border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <FaPaperPlane size={18} />
          )}
        </button>
      </div>
      {/* BOTÓN ESPECIFICACIONES */}

      {mostrarFormEspecificaciones && (
        <FormularioEspecificaciones cerrar={cerrarFormulario} />
      )}

      {/* ESTILOS EN LINEA PARA ANIMACIONES */}
      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out forwards;
        }
      `}</style>
    </main>
  );
}
