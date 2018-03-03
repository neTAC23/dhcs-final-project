/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { NameSongsComponent } from './name-songs.component';

describe('NameSongsComponent', () => {
  let component: NameSongsComponent;
  let fixture: ComponentFixture<NameSongsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NameSongsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NameSongsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
