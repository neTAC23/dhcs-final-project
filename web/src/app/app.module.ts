import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { NavBarComponent } from './components/nav-bar/nav-bar.component';
import { HomePageComponent } from './components/home-page/home-page.component';
import { CommonNamesPageComponent } from './components/common-names-page/common-names-page.component';
import { BibleNamesComponent } from './components/bible-names/bible-names.component';
import { MenVsWomenComponent } from './components/men-vs-women/men-vs-women.component';
import { MenSingAboutComponent } from './components/men-sing-about/men-sing-about.component';
import { AllNamesComponent } from './components/all-names/all-names.component';
import { NamesLetterComponent } from './components/names-letter/names-letter.component';
import { NameSongsComponent } from './components/name-songs/name-songs.component';
import { SearchComponent } from './components/search/search.component';


// Define the routes
const ROUTES = [

  { path: '', component: HomePageComponent },
  { path: 'common', component: CommonNamesPageComponent },
  { path: 'bible', component: BibleNamesComponent },
  { path: 'men-vs-women', component: MenVsWomenComponent }, 
  { path: 'sing-about', component: MenSingAboutComponent },
  { path: 'all-names', component: AllNamesComponent },
  { path: 'all-names/:letter', component: NamesLetterComponent },
  { path: 'all-names/:letter/:name', component: NameSongsComponent },
  { path: 'search/:query', component: SearchComponent},
  // otherwise redirect to home
  { path: '**', redirectTo: '' } 
];


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    NavBarComponent,
    HomePageComponent,
    CommonNamesPageComponent,
    BibleNamesComponent,
    MenVsWomenComponent,
    MenSingAboutComponent,
    AllNamesComponent,
    NamesLetterComponent,
    NamesLetterComponent,
    NameSongsComponent,
    SearchComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    RouterModule.forRoot(ROUTES)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
