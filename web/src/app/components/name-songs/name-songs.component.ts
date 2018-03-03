import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable} from 'rxjs/Rx';

@Component({
  selector: 'app-name-songs',
  templateUrl: './name-songs.component.html',
  styleUrls: ['./name-songs.component.css']
})
export class NameSongsComponent implements OnInit {
  letter;
  name;
  songs;
  keys;
  constructor(private route: ActivatedRoute, private http: Http) { }

  ngOnInit() {
     this.route.params.subscribe(params => {
      this.letter = params['letter'];
      this.name = params['name']
      this.getJSON().subscribe(
        data => {
        //data contains the json.\
        this.songs = data[this.letter][this.name]
        console.log(this.songs)
        this.keys = Object.keys(this.songs)
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
  
  public getSongName(name){
    let singer = name.split("_")[0];
    let title = name.split("_")[1];
    return singer+" - "+title;

  }

}
