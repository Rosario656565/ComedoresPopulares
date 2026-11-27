import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RacionesComponentes } from './raciones-componentes';

describe('RacionesComponentes', () => {
  let component: RacionesComponentes;
  let fixture: ComponentFixture<RacionesComponentes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RacionesComponentes],
    }).compileComponents();

    fixture = TestBed.createComponent(RacionesComponentes);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
