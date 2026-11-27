import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  PLATFORM_ID,
  ViewChild,
  computed,
  effect,
  inject,
} from "@angular/core";
import { CurrencyPipe, isPlatformBrowser } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { Chart, registerables } from "chart.js";
import { Reporte } from "../../models";
import { DataService, hoy } from "../../data.service";

Chart.register(...registerables);

const VACIO = { gi: 0, gas: 0, ven: 0, rac: 0 };

@Component({
  selector: "app-reportes-componentes",
  imports: [FormsModule, CurrencyPipe],
  templateUrl: "./reportes-componentes.html",
})
export class ReportesComponentes implements AfterViewInit, OnDestroy {
  private d = inject(DataService);
  private browser = isPlatformBrowser(inject(PLATFORM_ID));
  private chart?: Chart;

  @ViewChild("cv") cv?: ElementRef<HTMLCanvasElement>;
  form: Reporte | null = null;
  editando = false;

  meses = computed(() =>
    [
      ...new Set([
        ...this.d.reportes().map((r) => r.mes),
        ...this.d.insumos().map((i) => i.reg),
        ...this.d.asistencias().map((a) => a.fecha.slice(0, 7)),
      ]),
    ]
      .filter(Boolean)
      .sort(),
  );

  filas = computed(() =>
    this.meses().map((mes) => {
      const r = this.d.reportes().find((x) => x.mes === mes);
      const gi = this.d
        .insumos()
        .filter((i) => i.reg === mes)
        .reduce((s, i) => s + i.costo, 0);
      const rac = this.d
        .asistencias()
        .filter((a) => a.fecha.slice(0, 7) === mes)
        .reduce((s, a) => s + a.ids.length, 0);
      const gas = r?.gas ?? 0;
      return {
        mes,
        gi,
        gas,
        ven: r?.ven ?? 0,
        rac,
        costoRac: rac ? (gi + gas) / rac : null,
        tiene: !!r,
      };
    }),
  );

  actual = computed(
    () => this.filas().find((f) => f.mes === hoy().slice(0, 7)) ?? VACIO,
  );

  constructor() {
    effect(() => this.dibujar());
  }

  ngAfterViewInit() {
    this.dibujar();
  }
  ngOnDestroy() {
    this.chart?.destroy();
  }

  private dibujar() {
    const f = this.filas();
    if (!this.browser || !this.cv) return;
    this.chart?.destroy();
    this.chart = new Chart(this.cv.nativeElement, {
      type: "bar",
      data: {
        labels: f.map((x) => x.mes),
        datasets: [
          {
            label: "Gasto en insumos",
            data: f.map((x) => x.gi),
            backgroundColor: "#92400e",
          },
          {
            label: "Gastos generales",
            data: f.map((x) => x.gas),
            backgroundColor: "#b91c1c",
          },
          {
            label: "Dinero recaudado",
            data: f.map((x) => x.ven),
            backgroundColor: "#17552f",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: "Soles (S/)" },
          },
        },
      },
    });
  }

  nuevo() {
    this.editando = false;
    this.form = { mes: hoy().slice(0, 7), ven: 0, gas: 0 };
  }
  editar(f: { mes: string; ven: number; gas: number }) {
    this.editando = true;
    this.form = { mes: f.mes, ven: f.ven, gas: f.gas };
  }
  guardar() {
    if (!this.form) return;
    this.d.guardarReporte(this.form);
    this.form = null;
  }
  eliminar(mes: string) {
    if (confirm("¿Eliminar este reporte?")) this.d.eliminarReporte(mes);
  }
}
