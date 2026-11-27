import { Component, computed, inject, signal } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { DataService, hoy, porVenc } from "../../data.service";

@Component({
  selector: "app-raciones-componentes",
  imports: [FormsModule],
  templateUrl: "./raciones-componentes.html",
})
export class RacionesComponentes {
  d = inject(DataService);
  fecha = hoy();
  sel = new Set<number>();
  insumoId: number | null = null;
  cant: number | null = null;
  error = "";
  mensaje = signal("");

  activos = computed(() =>
    this.d.beneficiarios().filter((b) => b.est === "Activo"),
  );
  lotes = computed(() =>
    this.d
      .insumos()
      .filter((i) => i.cant > 0)
      .sort(porVenc),
  );
  historial = computed(() =>
    [...this.d.asistencias()]
      .sort((a, b) => (a.fecha < b.fecha ? 1 : -1))
      .slice(0, 15),
  );

  constructor() {
    this.cargar();
  }

  cargar() {
    const a = this.d.asistencias().find((x) => x.fecha === this.fecha);
    this.sel = new Set(a?.ids ?? []);
  }
  cambiar(e: Event) {
    this.fecha = (e.target as HTMLInputElement).value || hoy();
    this.cargar();
  }
  toggle(id: number) {
    if (this.sel.has(id)) this.sel.delete(id);
    else this.sel.add(id);
  }
  guardar() {
    this.d.guardarAsistencia(this.fecha, [...this.sel]);
    this.mensaje.set(
      `Asistencia del ${this.fecha} guardada (${this.sel.size} raciones).`,
    );
    setTimeout(() => this.mensaje.set(""), 3000);
  }
  descontar() {
    this.error = this.d.descontar(Number(this.insumoId), Number(this.cant));
    if (!this.error) this.cant = null;
  }
}


