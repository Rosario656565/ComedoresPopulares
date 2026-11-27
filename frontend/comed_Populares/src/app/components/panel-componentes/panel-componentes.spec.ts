import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PanelComponentes } from './panel-componentes';

describe('PanelComponentes', () => {
  let component: PanelComponentes;
  let fixture: ComponentFixture<PanelComponentes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PanelComponentes],
    }).compileComponents();

    fixture = TestBed.createComponent(PanelComponentes);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
