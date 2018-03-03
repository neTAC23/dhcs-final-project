/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { BibleNamesComponent } from './bible-names.component';

describe('BibleNamesComponent', () => {
  let component: BibleNamesComponent;
  let fixture: ComponentFixture<BibleNamesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BibleNamesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BibleNamesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
