import {
  Injectable,
  PLATFORM_ID,
  inject,
  signal,
} from "@angular/core";
import { isPlatformBrowser } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Asistencia, Beneficiario, Insumo, Reporte } from "./models";

export const hoy = () => new Date().toISOString().slice(0, 10);
export const dias = (f: string) =>
  Math.ceil((new Date(f).getTime() - new Date(hoy()).getTime()) / 864e5);
export const porVenc = (a: Insumo, b: Insumo) =>
  (a.venc || "9") > (b.venc || "9") ? 1 : -1;
export const estado = (i: Insumo) => {
  const d = i.venc ? dias(i.venc) : 999;
  return d < 0
    ? "Vencido"
    : i.cant <= i.min
      ? "Stock bajo"
      : d <= 30
        ? "Por vencer"
        : "Normal";
};

@Injectable({ providedIn: "root" })
export class DataService {
  private browser = isPlatformBrowser(inject(PLATFORM_ID));
  private http = inject(HttpClient);

  // Ajusta esta URL al puerto donde corra tu servidor backend
  private apiUrl = "http://localhost:3000/api";

  beneficiarios = signal<Beneficiario[]>([]);
  insumos = signal<Insumo[]>([]);
  reportes = signal<Reporte[]>([]);
  asistencias = signal<Asistencia[]>([]);

  constructor() {
    if (this.browser) {
      this.cargarTodo();
    }
  }

  private cargarTodo() {
    this.http.get<Beneficiario[]>(`${this.apiUrl}/beneficiarios`).subscribe({
      next: (data) => this.beneficiarios.set(data),
      error: (err) => console.error("Error cargando beneficiarios:", err),
    });

    this.http.get<Insumo[]>(`${this.apiUrl}/insumos`).subscribe({
      next: (data) => this.insumos.set(data),
      error: (err) => console.error("Error cargando insumos:", err),
    });

    this.http.get<Reporte[]>(`${this.apiUrl}/reportes`).subscribe({
      next: (data) => this.reportes.set(data),
      error: (err) => console.error("Error cargando reportes:", err),
    });

    this.http.get<Asistencia[]>(`${this.apiUrl}/asistencias`).subscribe({
      next: (data) => this.asistencias.set(data),
      error: (err) => console.error("Error cargando asistencias:", err),
    });
  }

  // --- BENEFICIARIOS ---
  guardarBeneficiario(b: Beneficiario) {
    if (b.id) {
      this.http.put<Beneficiario>(`${this.apiUrl}/beneficiarios/${b.id}`, b).subscribe({
        next: (actualizado) =>
          this.beneficiarios.update((l) =>
            l.map((y) => (y.id === actualizado.id ? actualizado : y))
          ),
        error: (err) => console.error("Error actualizando beneficiario:", err),
      });
    } else {
      this.http.post<Beneficiario>(`${this.apiUrl}/beneficiarios`, b).subscribe({
        next: (creado) => this.beneficiarios.update((l) => [...l, creado]),
        error: (err) => console.error("Error creando beneficiario:", err),
      });
    }
  }

  eliminarBeneficiario(id: number) {
    this.http.delete(`${this.apiUrl}/beneficiarios/${id}`).subscribe({
      next: () => this.beneficiarios.update((l) => l.filter((x) => x.id !== id)),
      error: (err) => console.error("Error eliminando beneficiario:", err),
    });
  }

  // --- INSUMOS ---
  guardarInsumo(i: Insumo) {
    if (!i.id) i.reg = hoy().slice(0, 7);
    i.costo = i.tipo === "Donación" ? 0 : +i.costo || 0;

    if (i.id) {
      this.http.put<Insumo>(`${this.apiUrl}/insumos/${i.id}`, i).subscribe({
        next: (actualizado) =>
          this.insumos.update((l) =>
            l.map((y) => (y.id === actualizado.id ? actualizado : y))
          ),
        error: (err) => console.error("Error actualizando insumo:", err),
      });
    } else {
      this.http.post<Insumo>(`${this.apiUrl}/insumos`, i).subscribe({
        next: (creado) => this.insumos.update((l) => [...l, creado]),
        error: (err) => console.error("Error creando insumo:", err),
      });
    }
  }

  eliminarInsumo(id: number) {
    this.http.delete(`${this.apiUrl}/insumos/${id}`).subscribe({
      next: () => this.insumos.update((l) => l.filter((x) => x.id !== id)),
      error: (err) => console.error("Error eliminando insumo:", err),
    });
  }

  // --- REPORTES ---
  guardarReporte(r: Reporte) {
    this.http.post<Reporte>(`${this.apiUrl}/reportes`, r).subscribe({
      next: (guardado) =>
        this.reportes.update((l) =>
          l.some((x) => x.mes === guardado.mes)
            ? l.map((x) => (x.mes === guardado.mes ? guardado : x))
            : [...l, guardado]
        ),
      error: (err) => console.error("Error guardando reporte:", err),
    });
  }

  eliminarReporte(mes: string) {
    this.http.delete(`${this.apiUrl}/reportes/${mes}`).subscribe({
      next: () => this.reportes.update((l) => l.filter((x) => x.mes !== mes)),
      error: (err) => console.error("Error eliminando reporte:", err),
    });
  }

  // --- ASISTENCIAS (RACIONES) ---
  guardarAsistencia(fecha: string, ids: number[]) {
    this.http.post<Asistencia>(`${this.apiUrl}/asistencias`, { fecha, ids }).subscribe({
      next: (guardada) =>
        this.asistencias.update((l) =>
          l.some((a) => a.fecha === guardada.fecha)
            ? l.map((a) => (a.fecha === guardada.fecha ? guardada : a))
            : [...l, guardada]
        ),
      error: (err) => console.error("Error guardando asistencia:", err),
    });
  }

  /** Descuenta stock en el backend y actualiza la pantalla. */
  descontar(id: number, q: number): string {
    const i = this.insumos().find((x) => x.id === id);
    if (!i || !(q > 0))
      return "Elige un insumo e ingresa una cantidad mayor a 0.";
    if (q > i.cant) return `Solo hay ${i.cant} en stock de ${i.nom}.`;

    const nuevoStock = i.cant - q;
    this.http.put<Insumo>(`${this.apiUrl}/insumos/${id}`, { ...i, cant: nuevoStock }).subscribe({
      next: (actualizado) =>
        this.insumos.update((l) =>
          l.map((x) => (x.id === id ? actualizado : x))
        ),
      error: (err) => console.error("Error descontando stock:", err),
    });

    return "";
  }
}