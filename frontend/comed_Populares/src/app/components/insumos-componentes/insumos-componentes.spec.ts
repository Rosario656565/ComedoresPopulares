import { ComponentFixture, TestBed } from '@angular/core/testing';
import { InsumosComponentes } from './insumos-componentes';

describe('InsumosComponentes', () => {
  let component: InsumosComponentes;
  let fixture: ComponentFixture<InsumosComponentes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InsumosComponentes],
    }).compileComponents();

    fixture = TestBed.createComponent(InsumosComponentes);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
