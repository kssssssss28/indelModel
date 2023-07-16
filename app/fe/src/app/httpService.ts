import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
@Injectable()

export class httpService{
  sendRequest = (method:string,data:any)=>{
    if(method === "GET"){
      let url = "http://localhost:3000/?dna=" + encodeURIComponent(data)
      return this.http.get(url);
    }else(method === "POST")
    {
      return this.http.post("http://localhost:3000/",[])
    }
  }
  constructor(private http: HttpClient){
    this.http = http
  }
}
