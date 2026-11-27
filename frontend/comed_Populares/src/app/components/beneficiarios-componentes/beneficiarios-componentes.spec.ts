import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BeneficiariosComponentes } from './beneficiarios-componentes';

describe('BeneficiariosComponentes', () => {
  let component: BeneficiariosComponentes;
  let fixture: ComponentFixture<BeneficiariosComponentes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BeneficiariosComponentes],
    }).compileComponents();

    fixture = TestBed.createComponent(BeneficiariosComponentes);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
