import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-all-names',
  templateUrl: './all-names.component.html',
  styleUrls: ['./all-names.component.css']
})
export class AllNamesComponent implements OnInit {
  letters = [];
  constructor() { }

  ngOnInit() {
    this.letters  = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ", "ק", "ר", "ש", "ת"];

    console.log(this.letters);
  }

}
