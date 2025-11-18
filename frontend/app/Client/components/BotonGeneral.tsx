import React from "react";

type Props = {
  texto: string;
  children?: React.ReactNode;
  onClick: () => void;
};
export default function BotonGeneral({ texto, children, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className="cursor-pointer flex flex-row items-center gap-1 bg-[#E1DED3] p-4 rounded-xl text-[#808080] font-bold hover:bg-[#c9c7bf]"
    >
      {children}
      {texto}
    </button>
  );
}
