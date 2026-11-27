export interface Beneficiario {
  id: number;
  nom: string;
  dni: string;
  dir: string;
  nac: string;
  mail: string;
  est: "Activo" | "Inactivo";
}
export interface Insumo {
  id: number;
  nom: string;
  cant: number;
  min: number;
  tipo: "Compra" | "Donación";
  costo: number;
  don?: string;
  venc: string;
  reg: string;
}
export interface Reporte {
  mes: string;
  ven: number;
  gas: number;
}
export interface Asistencia {
  fecha: string;
  ids: number[];
}
