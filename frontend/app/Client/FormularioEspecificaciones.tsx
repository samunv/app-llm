'use client';

import { useState } from 'react';
import { Especificaciones } from '../interfaces/Especificaciones';

export default function EspecificacionesForm() {
  const [message, setMessage] = useState('');
  const [isPending, setIsPending] = useState(false);

  async function handleSubmit(formData: FormData) {
    setIsPending(true);
    setMessage('Procesando solicitud de receta...');

    // 1. Obtener los datos del formulario
    const especificaciones: Especificaciones = {
      tipo_dieta: String(formData.get('tipo_dieta')),
      restricciones: String(formData.get('restricciones')),
      ingredientes_evitar: String(formData.get('ingredientes_evitar')),
      tiempo_maximo: String(formData.get('tiempo_maximo')),
      objetivo: String(formData.get('objetivo')),
    };

    const result = ()=>{} // await guardarEspecificaciones(especificaciones); 

    // if (result.success) {
    //   setMessage('✅ Receta solicitada y especificaciones enviadas.');

    // } else {
    //   setMessage(`❌ Error: ${result.error}`);
    // }
    
    setIsPending(false);
  }

  return (
    <form id="especificaciones-form" action={handleSubmit}>
      <h2>Opciones de Receta (Opcional)</h2>

      <div>
        <label htmlFor="tipo_dieta">Tipo de Dieta (Vegana, Keto, etc.)</label>
        <input 
          type="text" 
          id="tipo_dieta" 
          name="tipo_dieta" 
          placeholder="Ej: vegetariana"
          disabled={isPending}
        />
      </div>

      <div>
        <label htmlFor="restricciones">Restricciones Dietéticas</label>
        <input 
          type="text" 
          id="restricciones" 
          name="restricciones" 
          placeholder="Ej: sin gluten, sin lactosa"
          disabled={isPending}
        />
      </div>

      <div>
        <label htmlFor="ingredientes_evitar">Ingredientes a Evitar</label>
        <input 
          type="text" 
          id="ingredientes_evitar" 
          name="ingredientes_evitar" 
          placeholder="Ej: cebolla, champiñones"
          disabled={isPending}
        />
      </div>
      
      <div>
        <label htmlFor="tiempo_maximo">Tiempo Máximo (en minutos)</label>
        <input 
          type="number" 
          id="tiempo_maximo" 
          name="tiempo_maximo" 
          placeholder="Ej: 30"
          disabled={isPending}
        />
      </div>
      
      <div>
        <label htmlFor="objetivo">Objetivo de la Comida</label>
        <input 
          type="text" 
          id="objetivo" 
          name="objetivo" 
          placeholder="Ej: cena rápida, postre bajo en azúcar"
          disabled={isPending}
        />
      </div>

      <button type="submit" disabled={isPending}>
        {isPending ? 'Solicitando...' : 'Generar Receta'}
      </button>

      {message && <p style={{ marginTop: '10px' }}>{message}</p>}
    </form>
  );
}