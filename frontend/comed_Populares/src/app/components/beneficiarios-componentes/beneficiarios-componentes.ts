import { Component, inject } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { Beneficiario } from "../../models";
import { DataService } from "../../data.service";

@Component({
  selector: "app-beneficiarios-componentes",
  imports: [FormsModule],
  templateUrl: "./beneficiarios-componentes.html",
})
export class BeneficiariosComponentes {
  d = inject(DataService);
  form: Beneficiario | null = null;

  nuevo() {
    this.form = {
      id: 0,
      nom: "",
      dni: "",
      dir: "",
      nac: "",
      mail: "",
      est: "Activo",
    };
  }
  editar(b: Beneficiario) {
    this.form = { ...b };
  }
  guardar() {
    if (!this.form) return;
    this.d.guardarBeneficiario(this.form);
    this.form = null;
  }
  eliminar(b: Beneficiario) {
    if (confirm("¿Eliminar este beneficiario?"))
      this.d.eliminarBeneficiario(b.id);
  }
}
