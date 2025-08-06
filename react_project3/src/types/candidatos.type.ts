export interface CandidatoResponse {
  id?: number;
  nombre: string;
  apellido: string;
  tipo_documento: string;
  cedula: string;
  fecha_nacimiento: string;
  rh: string;
  ciudad_expedicion_id: number;
  ciudad_nacimiento_id: number;
  ciudad_domicilio_id: number;
  activo: boolean;
  nombres_ciudades?: {
    ciudad_expedicion: string;
    ciudad_nacimiento: string;
    ciudad_domicilio: string;
  };
}