import { Component, computed, inject, output } from "@angular/core";
import { DataService, dias, hoy } from "../../data.service";

interface Alerta {
  nom: string;
  txt: string;
  acc: string;
  rojo: boolean;
}

@Component({
  selector: "app-panel-componentes",
  templateUrl: "./panel-componentes.html",
})
export class PanelComponentes {
  irRaciones = output<void>();
  private d = inject(DataService);

  activos = computed(
    () => this.d.beneficiarios().filter((b) => b.est === "Activo").length,
  );
  racionesHoy = computed(
    () => this.d.asistencias().find((a) => a.fecha === hoy())?.ids.length ?? 0,
  );
  bajos = computed(
    () => this.d.insumos().filter((i) => i.cant <= i.min).length,
  );
  porVencer = computed(
    () => this.d.insumos().filter((i) => i.venc && dias(i.venc) <= 30).length,
  );

  alertas = computed(() => {
    const r: Alerta[] = [];
    for (const i of this.d.insumos()) {
      if (i.cant <= i.min)
        r.push({
          nom: i.nom,
          txt: `stock bajo (${i.cant} de mínimo ${i.min})`,
          acc: "Comprar",
          rojo: true,
        });
      if (i.venc) {
        const x = dias(i.venc);
        if (x < 0)
          r.push({
            nom: i.nom,
            txt: `venció hace ${-x} días`,
            acc: "Retirar",
            rojo: true,
          });
        else if (x <= 30)
          r.push({
            nom: i.nom,
            txt: `vence en ${x} días (${i.venc})`,
            acc: "Usar pronto",
            rojo: false,
          });
      }
    }
    return r;
  });
}
