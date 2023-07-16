import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import {MatCardModule} from '@angular/material/card';
import { AppComponent } from './app.component';
import { httpService } from './httpService';
import {MatInputModule} from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatButtonModule} from '@angular/material/button';
import {MatTabsModule} from '@angular/material/tabs';
import { MatTableModule } from '@angular/material/table';
@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    MatTableModule,
    MatTabsModule,
    MatButtonModule,
    BrowserAnimationsModule,
    BrowserModule,
    HttpClientModule,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule
  ],
  providers: [
    httpService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
