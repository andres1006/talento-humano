import { get, post, put, del, patch } from './index';

// Tipos para las entidades
export interface Cliente {
  id?: number;
  nombre: string;
  email: string;
  telefono: string;
  direccion: string;
  activo: boolean;
}

export interface Candidato {
  id?: number;
  nombre: string;
  apellido: string;
  email: string;
  telefono: string;
  experiencia: string;
  habilidades: string;
  activo: boolean;
}

export interface Oferta {
  id?: number;
  titulo: string;
  empresa: string;
  descripcion: string;
  requisitos: string;
  salario: string;
  ubicacion: string;
  tipo_contrato: string;
  activa: boolean;
}

export interface Asociacion {
  id?: number;
  candidato_id: number;
  oferta_id: number;
  fecha_asociacion: string;
  estado: 'pendiente' | 'en_revision' | 'aprobado' | 'rechazado';
  observaciones: string;
}

// Función genérica para hacer peticiones HTTP
export const apiRequest = async <T = any>(
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH',
  path: string,
  payload?: any
): Promise<T> => {
  console.log("🔄 Petición:", method, path, payload);
  try {
    switch (method) {
      case 'GET':
        return await get<T>(path);
      case 'POST':
        return await post<T>(path, payload);
      case 'PUT':
        return await put<T>(path, payload);
      case 'PATCH':
        return await patch<T>(path, payload);
      case 'DELETE':
        return await del<T>(path);
      default:
        throw new Error('Método HTTP no válido');
    }
  } catch (error) {
    console.error(`Error en petición ${method} ${path}:`, error);
    throw error;
  }
};


export const setBaseURL = (url: string) => {
  console.log('URL base establecida:', url);
};


// eslint-disable-next-line import/no-anonymous-default-export
export default {
  apiRequest,
  setBaseURL
}; 