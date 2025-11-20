"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import {
  FaPaperPlane,
  FaChevronDown,
  FaCheck,
  FaFilePdf,
  FaImage,
  FaUser,
} from "react-icons/fa6";
import { FaRobot } from "react-icons/fa";
import { IoIosAddCircle } from "react-icons/io";

import "./Inicio.css";
import { useSolicitudReceta } from "../contexts/SolicitudRecetaContext";
import { useEspecificaciones } from "../contexts/EspecificacionesContext";
import FormularioEspecificaciones from "./FormularioEspecificaciones";
import BotonGeneral from "./components/BotonGeneral";
import { modelosGemini } from "./modelos";
import { Modelo } from "../interfaces/Modelo";
import { enviarReceta } from "@/Server/Server";
import TypingText from "./components/TypingText";
import { Receta } from "../interfaces/Receta";
import GeneradorPDF from "./components/GeneradorPDF";

// --- IMPORTS ---
import Sidebar from "./components/Sidebar";
import { useHistorial } from "../hooks/useHistorial";
import { Conversacion } from "../interfaces/Conversacion";
import ModalConfiguracion from "./components/ModalConfiguracion";

interface MensajeChat {
  id: string;
  rol: "usuario" | "ia";
  tipo: "texto" | "receta";
  contenido: string | Receta;
}

export default function Inicio() {
  // Contextos
  const { solicitudReceta, updateSolicitudReceta } = useSolicitudReceta();
  const { especificaciones } = useEspecificaciones();

  // Hooks
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { historial, guardarConversacion, borrarConversacion } = useHistorial();

  // Estados UI
  const [isOpen, setIsOpen] = useState(false);
  const [modeloSeleccionado, setModeloSeleccionado] = useState<Modelo>(
    modelosGemini[0]
  );
  const [mostrarFormEspecificaciones, setMostrarFormEspecificaciones] =
    useState<boolean>(false);
  const [imagenPreview, setImagenPreview] = useState<string>();

  // Estados Chat
  const [chatLog, setChatLog] = useState<MensajeChat[]>([]);
  const [cargando, setCargando] = useState(false);

  // Refs
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputFileRef = useRef<HTMLInputElement>(null);

  // Scroll automático
  useEffect(() => {
    if (chatLog.length > 0) {
      window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [chatLog, cargando]);

  // --- LÓGICA DE ENVÍO ---
  const handleEnviar = async () => {
    const textoInput = solicitudReceta?.comida;
    const imagenInput = solicitudReceta?.imagen;

    if (!textoInput && !imagenInput) return;

    // 1. Mensaje Usuario
    const msgUsuario: MensajeChat = {
      id: crypto.randomUUID(),
      rol: "usuario",
      tipo: "texto",
      contenido: textoInput || (imagenInput ? "Analiza esta imagen" : ""),
    };

    const nuevoLog = [...chatLog, msgUsuario];
    setChatLog(nuevoLog);
    setCargando(true);
    updateSolicitudRecetaCallback("comida", "");

    try {
      // 2. Historial para Backend
      const historialBackend = nuevoLog.slice(0, -1).map((msg) => {
        let texto = "";
        if (msg.tipo === "texto") texto = msg.contenido as string;
        else texto = JSON.stringify(msg.contenido);

        return {
          role: msg.rol === "usuario" ? "user" : "model",
          parts: [{ text: texto }],
        };
      });

      // 3. Playload
      const playload = {
        ...solicitudReceta,
        comida: textoInput || "",
        historial: historialBackend,
        modeloIASeleccionado:
          solicitudReceta?.modeloIASeleccionado || "gemini-2.5-flash",
        imagen: solicitudReceta?.imagen || "",
        tipoImagen: solicitudReceta?.tipoImagen || "",
      };

      // 4. Petición
      const data = await enviarReceta(playload);

      if (data.estado === "exito") {
        const msgIA: MensajeChat = {
          id: crypto.randomUUID(),
          rol: "ia",
          tipo: data.tipo === "receta" ? "receta" : "texto",
          contenido: data.respuesta,
        };

        setChatLog((prev) => [...prev, msgIA]);

        if (data.tipo === "receta") {
          guardarConversacion(
            data.respuesta as Receta,
            textoInput || "Receta generada"
          );
        }
      } else {
        setChatLog((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            rol: "ia",
            tipo: "texto",
            contenido: "Error: " + (data.error || "Desconocido"),
          },
        ]);
      }
    } catch (error) {
      console.error(error);
      setChatLog((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          rol: "ia",
          tipo: "texto",
          contenido: "Error de conexión con el servidor.",
        },
      ]);
    } finally {
      setCargando(false);
    }
  };

  // --- FUNCIONES AUXILIARES ---
  const cargarConversacionDesdeHistorial = (conv: Conversacion) => {
    setChatLog([
      {
        id: crypto.randomUUID(),
        rol: "ia",
        tipo: "receta",
        contenido: conv.receta,
      },
    ]);
    if (typeof window !== "undefined" && window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  };

  const handleNuevaConversacion = () => {
    setChatLog([]);
    updateSolicitudRecetaCallback("comida", "");
    setImagenPreview(undefined);
    updateSolicitudReceta("imagen", "");
  };

  const handleClickImagen = () => inputFileRef.current?.click();
  const cerrarFormulario = () => setMostrarFormEspecificaciones(false);

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

  // const getVelocidadConfig = (velocidad: string) => {
  //   switch (velocidad) {
  //     case "ultrarrápido":
  //       return { color: "text-green-600", emoji: "⚡⚡", bg: "bg-green-50" };
  //     case "rápido":
  //       return { color: "text-emerald-600", emoji: "⚡", bg: "bg-emerald-50" };
  //     case "equilibrado":
  //       return { color: "text-blue-600", emoji: "⚖️", bg: "bg-blue-50" };
  //     case "potente":
  //       return { color: "text-purple-600", emoji: "🔥", bg: "bg-purple-50" };
  //     default:
  //       return { color: "text-gray-600", emoji: "⭐", bg: "bg-gray-50" };
  //   }
  // };

  useEffect(() => {
    if (modeloSeleccionado) {
      updateSolicitudRecetaCallback(
        "modeloIASeleccionado",
        modeloSeleccionado.id
      );
    }
  }, [modeloSeleccionado, updateSolicitudRecetaCallback]);

  return (
    <div className="flex w-full min-h-screen bg-[#FAF9F5] relative">
      <Sidebar
        isOpen={sidebarOpen}
        toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        historial={historial}
        cargarConversacion={cargarConversacionDesdeHistorial}
        borrarConversacion={borrarConversacion}
        nuevaConversacion={handleNuevaConversacion}
      />

      <main
        className={`
        flex-1 flex flex-col items-center min-h-screen transition-all duration-300 ease-in-out
        ${sidebarOpen ? "md:ml-[300px]" : ""}
        ${
          chatLog.length > 0
            ? "justify-start pt-10 pb-48"
            : "justify-center pb-20"
        }
      `}
      >
        {/* LOGO */}
        <div
          className={`flex flex-row-reverse items-center gap-1 transition-all duration-500 ${
            chatLog.length > 0 ? "scale-75 mb-2" : "mb-8"
          }`}
        >
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

        {/* BIENVENIDA */}
        {chatLog.length === 0 && !cargando && (
          <h1 className="text-[#343A40] text-3xl text-center font-medium animate-fadeIn px-4">
            ¡Hola! soy tu chef y hago recetas
            <TypingText
              frases={[" rápidas.", " creativas.", " personalizadas."]}
            />
          </h1>
        )}

        {/* --- AREA CHAT --- */}
        <div className="w-full max-w-[750px] px-4 flex flex-col gap-8">
          {chatLog.map((msg) => (
            <div
              key={msg.id}
              className={`flex w-full ${
                msg.rol === "usuario" ? "justify-end" : "justify-start"
              } animate-fadeIn`}
            >
              {/* TEXTO (Usuario o IA Conversación) */}
              {msg.tipo === "texto" && (
                <div
                  className={`max-w-[85%] p-5 rounded-2xl shadow-sm text-base leading-relaxed ${
                    msg.rol === "usuario"
                      ? "bg-white border border-gray-300 text-[#1F1F1F] rounded-br-sm"
                      : "bg-white border border-gray-300 text-[#343A40] rounded-bl-sm"
                  }`}
                >
                  {msg.rol === "ia" && (
                    <div className="flex items-center gap-1 mb-2 font-bold text-[#E67E22]">
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        width={20}
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
                      </svg>{" "}
                      ChefGPT
                    </div>
                  )}
                  <p className="whitespace-pre-wrap">
                    {msg.contenido as string}
                  </p>
                </div>
              )}

              {/* RECETA (Diseño Original Restaurado) */}
              {msg.tipo === "receta" && (
                <div className="w-full bg-white p-10 rounded-3xl shadow-xl border border-gray-300">
                  {/* Contenido Receta (Estilo Original) */}
                  {(() => {
                    const r = msg.contenido as Receta;
                    return (
                      <div className="prose prose-orange max-w-none text-[#343A40] leading-relaxed">
                        <div id={`receta-${msg.id}`} className="mb-5">
                          <h1 className="font-bold text-3xl text-[#343A40]">
                            {r.nombrePlato}
                          </h1>

                          <hr className="mt-4 mb-4 border border-[#DCD3D0]" />

                          <h2 className="font-bold text-2xl text-[#343A40]">
                            Ingredientes
                          </h2>
                          <ul className="list-disc pl-5 space-y-1">
                            {r.ingredientes?.map((ingrediente, index) => (
                              <li key={index}>{ingrediente}</li>
                            ))}
                          </ul>

                          <hr className="mt-4 mb-4 border border-[#DCD3D0]" />

                          <h2 className="font-bold text-2xl text-[#343A40]">
                            Pasos
                          </h2>
                          <ul className="space-y-2">
                            {r.pasos?.map((paso, index) => (
                              <li key={index} className="list-none">
                                <span className="font-bold mr-1">
                                  {index + 1})
                                </span>{" "}
                                {paso}
                              </li>
                            ))}
                          </ul>

                          {r.especificaciones && (
                            <>
                              <hr className="mt-4 mb-4 border border-[#DCD3D0]" />
                              <h2 className="font-bold text-2xl text-[#343A40]">
                                Especificaciones
                              </h2>
                              <p>{r.especificaciones}</p>
                            </>
                          )}
                        </div>

                        {/* Botón PDF Integrado */}
                        <GeneradorPDF htmlElement={`receta-${msg.id}`} />
                      </div>
                    );
                  })()}
                </div>
              )}
            </div>
          ))}

          {
            cargando && 
              <div className="flex justify-start w-full">
                <div className="loader"></div>
              </div>
          }
        </div>

        {/* BARRA FLOTANTE */}
        <div
          className={`
            bg-white mt-7 text-[#343A40] p-2 pr-3 pl-4 border-1 border-gray-400 rounded-2xl flex flex-row items-center gap-3 shadow-2xl shadow-orange-500/10 focus-within:border-[#E67E22]  z-50
            ${
              chatLog.length > 0
                ? `fixed bottom-8 w-[750px] ${
                    sidebarOpen ? "left-[calc(50%+150px)]" : "left-1/2"
                  } transform -translate-x-1/2`
                : "w-[750px] min-h-[70px]"
            }
          `}
        >
          {/* Dropdown */}
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
              <div className="flex-1 text-left min-w-0 hidden sm:block">
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
                className={`absolute left-0 w-[350px] max-h-[300px] overflow-y-auto bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 animate-fadeIn p-2
              ${chatLog.length > 0 ? "bottom-full mb-3" : "top-full mt-1"}
              `}
              >
                {modelosGemini.map((modelo) => (
                  <button
                    key={modelo.id}
                    onClick={() => seleccionarModelo(modelo)}
                    className={`w-full p-3 mb-1 rounded-xl flex items-center gap-3 transition-all duration-200 hover:bg-gray-50 ${
                      modeloSeleccionado.id === modelo.id
                        ? "bg-orange-50 border border-orange-100"
                        : ""
                    }`}
                  >
                    <div
                      className="p-2 rounded-lg flex-shrink-0 shadow-sm bg-white"
                      style={{ color: modelo.color }}
                    >
                      {modelo.icono}
                    </div>
                    <div className="flex-1 text-left">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-gray-700 text-sm">
                          {modelo.nombre}
                        </span>
                        {modeloSeleccionado.id === modelo.id && (
                          <FaCheck className="text-[#E67E22] text-xs" />
                        )}
                      </div>
                      <div className="text-xs text-gray-400">
                        {modelo.descripcion}
                      </div>
                    </div>
                  </button>
                ))}
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
            placeholder={
              chatLog.length > 0
                ? "Pregunta sobre la receta..."
                : "¿Qué vamos a preparar hoy?"
            }
            className="flex-1 outline-none text-base bg-transparent px-2 text-gray-700 placeholder-gray-400"
            value={solicitudReceta?.comida ?? ""}
            onChange={(e) =>
              updateSolicitudRecetaCallback("comida", e.target.value)
            }
            onKeyDown={(e) => e.key === "Enter" && handleEnviar()}
          />

          {chatLog.length == 0 && (
            <IoIosAddCircle
              size={25}
              className="text-gray-400 hover:text-[#E67E22] transition-colors cursor-pointer"
              onClick={() => setMostrarFormEspecificaciones(true)}
            />
          )}

          {chatLog.length == 0 && (
            <div>
              {imagenPreview ? (
                <div className="relative group w-10 h-10">
                  <img
                    src={imagenPreview}
                    className="w-full h-full object-cover rounded-lg border border-orange-200 cursor-pointer"
                  />
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setImagenPreview(undefined);
                      updateSolicitudReceta("imagen", "");
                    }}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center text-[10px] shadow-sm"
                  >
                    ✕
                  </button>
                </div>
              ) : (
                <button
                  onClick={handleClickImagen}
                  className="p-2 text-gray-400 hover:text-[#E67E22] rounded-xl transition-colors cursor-pointer"
                  title="Subir foto"
                >
                  <FaImage size={25} />
                </button>
              )}
            </div>
          )}

          <button
            onClick={handleEnviar}
            disabled={
              cargando || (!solicitudReceta?.comida && !solicitudReceta?.imagen)
            }
            className={`bg-[#E67E22] hover:bg-[#D35400] text-white p-3 rounded-xl transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center`}
          >
            {cargando ? (
              <div className="w-[18px] h-[18px] border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <FaPaperPlane size={18} />
            )}
          </button>
        </div>

        {/* Modales */}
        {mostrarFormEspecificaciones && (
          <FormularioEspecificaciones cerrar={cerrarFormulario} />
        )}
        {/* {modalAbierto && (
          <ModalConfiguracion
            perfilActual={perfil}
            guardar={guardarPerfil}
            cerrar={() => setModalAbierto(false)}
          />
        )} */}

        {/* Estilos Animación */}
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
            animation: fadeIn 0.4s ease-out forwards;
          }
        `}</style>
      </main>
    </div>
  );
}
