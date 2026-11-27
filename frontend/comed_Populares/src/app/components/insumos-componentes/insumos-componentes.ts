import { Component, computed, inject } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { CurrencyPipe } from "@angular/common";
import { Insumo } from "../../models";
import { DataService, estado, porVenc } from "../../data.service";

@Component({
  selector: "app-insumos-componentes",
  imports: [FormsModule, CurrencyPipe],
  templateUrl: "./insumos-componentes.html",
})
export class InsumosComponentes {
  d = inject(DataService);
  form: Insumo | null = null;
  estado = estado;

  ordenados = computed(() => [...this.d.insumos()].sort(porVenc));

  clase(i: Insumo) {
    const e = estado(i);
    return e === "Normal" ? "ok" : e === "Por vencer" ? "warn" : "bad";
  }
  nuevo() {
    this.form = {
      id: 0,
      nom: "",
      cant: 0,
      min: 0,
      tipo: "Compra",
      costo: 0,
      don: "",
      venc: "",
      reg: "",
    };
  }
  editar(i: Insumo) {
    this.form = { ...i };
  }
  guardar() {
    if (!this.form) return;
    this.d.guardarInsumo(this.form);
    this.form = null;
  }
  eliminar(i: Insumo) {
    if (confirm("¿Eliminar este insumo?")) this.d.eliminarInsumo(i.id);
  }
}
