/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { MenVsWomenComponent } from './men-vs-women.component';

describe('MenVsWomenComponent', () => {
  let component: MenVsWomenComponent;
  let fixture: ComponentFixture<MenVsWomenComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MenVsWomenComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MenVsWomenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
