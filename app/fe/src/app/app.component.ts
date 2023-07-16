import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { httpService } from './httpService';
import { checkFormatName, spliceFile } from './utils';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'ex';
  httpService:httpService
  dele = "NO DATA"
  oneIns = "NO DATA"
  oneDele = "NO DATA"
  showWarning = false
  showResult = false
  struct:any
  showStruct = false
  submitDNA = (dna:any)=>{
    if(dna.length <60){
      this.showWarning = true
      return
    }else{
      this.showWarning = false
      const res = this.httpService.sendRequest("GET", dna)
      res.subscribe({
        next:(v:any)=>{
          console.log(v)
          this.oneDele = v.oneDele.toFixed(3);
          this.oneIns = v.oneIns.toFixed(3);
          this.dele = v.dele.toFixed(3);

          this.showResult = true
        }
      })
    }
  }
  submitPic = async (e:any)=>{
    const file = e.target.files[0];
    const valid = await checkFormatName(file)
    if(valid){
      spliceFile(file)
    }
    const res = this.httpService.sendRequest("POST", [])
    res.subscribe({
      next:(v:any)=>{
        this.struct = v
        this.showStruct = true

      }
    })


  }
  constructor(httpService:httpService, private http: HttpClient){
    this.httpService = httpService
  }
}
