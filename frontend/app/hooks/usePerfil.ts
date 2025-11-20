// import { useState, useEffect } from "react";
// import { PerfilUsuario } from "../interfaces/PerfilUsuario";

// const PERFIL_INICIAL: PerfilUsuario = {
//   nombre: "",
//   alergias: "",
//   dietaGeneral: "",
//   ingredientesOdiados: "",
// };

// export const usePerfil = () => {
//   const [perfil, setPerfil] = useState<PerfilUsuario>(PERFIL_INICIAL);
//   const [modalAbierto, setModalAbierto] = useState(false);

 
//     if (typeof window !== "undefined") {
//       const guardado = localStorage.getItem("chefgpt_perfil");
//       if (guardado) {
//         setPerfil(JSON.parse(guardado));
//       }
//     }
 

//   // Guardar cambios
//   const guardarPerfil = (nuevoPerfil: PerfilUsuario) => {
//     setPerfil(nuevoPerfil);
//     localStorage.setItem("chefgpt_perfil", JSON.stringify(nuevoPerfil));
//     setModalAbierto(false);
//   };

//   return { perfil, guardarPerfil, modalAbierto, setModalAbierto };
// };