import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReportesComponentes } from './reportes-componentes';

describe('ReportesComponentes', () => {
  let component: ReportesComponentes;
  let fixture: ComponentFixture<ReportesComponentes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReportesComponentes],
    }).compileComponents();

    fixture = TestBed.createComponent(ReportesComponentes);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
