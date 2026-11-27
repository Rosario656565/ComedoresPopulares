import { Component, signal } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { PanelComponentes } from "./components/panel-componentes/panel-componentes";
import { BeneficiariosComponentes } from "./components/beneficiarios-componentes/beneficiarios-componentes";
import { InsumosComponentes } from "./components/insumos-componentes/insumos-componentes";
import { RacionesComponentes } from "./components/raciones-componentes/raciones-componentes";
import { ReportesComponentes } from "./components/reportes-componentes/reportes-componentes";

type Vista = "panel" | "beneficiarios" | "raciones" | "insumos" | "reportes";

@Component({
  selector: "app-root",
  imports: [
    FormsModule,
    PanelComponentes,
    BeneficiariosComponentes,
    InsumosComponentes,
    RacionesComponentes,
    ReportesComponentes,
  ],
  templateUrl: "./app.html",
  styleUrl: "./app.css",
})
export class App {
  logged = signal(false);
  vista = signal<Vista>("panel");
  usuario = "";
  clave = "";
  error = "";

  menu: { id: Vista; txt: string }[] = [
    { id: "panel", txt: "Panel" },
    { id: "beneficiarios", txt: "Beneficiarios" },
    { id: "raciones", txt: "Raciones" },
    { id: "insumos", txt: "Insumos" },
    { id: "reportes", txt: "Reportes" },
  ];

  // TODO backend: reemplazar por autenticación real
  entrar() {
    if (this.usuario.trim() === "admin" && this.clave === "1234") {
      this.error = "";
      this.clave = "";
      this.vista.set("panel");
      this.logged.set(true);
    } else {
      this.error =
        "Usuario o contraseña incorrectos. Revisa los datos e inténtalo de nuevo.";
    }
  }

  salir() {
    this.logged.set(false);
  }
}
