import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable} from 'rxjs/Rx';


@Component({
  selector: 'app-names-letter',
  templateUrl: './names-letter.component.html',
  styleUrls: ['./names-letter.component.css']
})
export class NamesLetterComponent implements OnInit {
  letter;
  all;
  names;
  keys;
  constructor(private route: ActivatedRoute, private http: Http) {

   }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.letter = params['letter'];
      this.getJSON().subscribe(
        data => {
        //data contains the json.\
        this.all = data;
        console.log(data);
        this.names = this.all[this.letter]
        console.log(this.names)
        this.keys = Object.keys(this.names).sort()
        }, 
        error => console.log(error)
      );

      });
  }

  public getJSON(): Observable<any> {
     let json = '../../../json_data/names.json'
         return this.http.get(json)
                         .map((res:any) => res.json());

  }
}
