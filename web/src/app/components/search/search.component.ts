import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable} from 'rxjs/Rx';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  
  error = false;
  constructor(private route: ActivatedRoute,private router: Router, private http: Http) { }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let query = params['query'];
      let index = this.letterToNumber(query[0]);
      if(index == -1){
        this.error = true;
      } else {
         this.getJSON().subscribe(
        data => {
          if(data[index][query])
            this.router.navigate(['/all-names/'+index+'/'+query])
          else
            this.error = true;
        }, 
        error => this.error = true
      );
        
      }

    });

  }

    public getJSON(): Observable<any> {
     let json = '../../../json_data/names.json'
         return this.http.get(json)
                         .map((res:any) => res.json());

  }

  letterToNumber(letter){
    let lettersArr = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ", "ק", "ר", "ש", "ת"];
    return lettersArr.indexOf(letter);
  }

}
