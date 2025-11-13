import Image from "next/image";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#FAF9F5] font-sans">
      <main className="flex flex-col items-center !w-full gap-3">
        <div className="flex flex-row-reverse items-center gap-1">
          <h1
            className="text-6xl 
      font-bold 
      // 1. Aplicar degradado de fondo (de naranja oscuro a amarillo)
      bg-gradient-to-r from-[#E67E22] to-yellow-300 
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
                fill="#E67E22"
              ></path>{" "}
              <path
                d="M18.9983 18.75H5.00169C5.01188 20.1469 5.08343 20.9119 5.58579 21.4142C6.17157 22 7.11438 22 9 22H15C16.8856 22 17.8284 22 18.4142 21.4142C18.9166 20.9119 18.9881 20.1469 18.9983 18.75Z"
                fill="#E67E22"
              ></path>{" "}
            </g>
          </svg>
        </div>
        {/** SECCIÓN DE MENSAJES (CHAT) */}
        <div className=""></div>

        {/** INPUT ESCRIBIR TEXTO */}
        <div className="bg-[white] text-[black] !p-4 border border-[#d0c19f] rounded-3xl flex flex-row items-center !w-[500px]">
          <input
            type="text"
            name=""
            id=""
            placeholder="¿Qúe te apetece preparar hoy?"
            className=" placeholder:text-[gray] flex-1 outline-none"
          />
        </div>
      </main>
         
    </div>
  );
}
