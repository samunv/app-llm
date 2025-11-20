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
      className="cursor-pointer flex flex-row items-center gap-1 bg-gray-200 p-4 rounded-xl text-gray-400 font-bold hover:bg-gray-300"
    >
      {children}
      {texto}
    </button>
  );
}
