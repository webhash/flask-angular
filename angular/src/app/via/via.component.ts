import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http'
@Component({
  selector: 'app-via',
  templateUrl: './via.component.html',
  styleUrls: ['./via.component.scss']
})
export class ViaComponent implements OnInit {


  readonly INITIAL_INPUT: string = "Input to API."
  readonly INITIAL_OUTPUT: string = "Output from API"
  
  user_input: string;
  server_output: string;
  uri = `http://localhost:9999`
  
  
  // json can be used to get pass the CORS issue
  constructor(private http: HttpClient) { 
    this.user_input = ""
    this.server_output = ""
  }

  ngOnInit(): void {
  }
  doPOST(){
    console.log("I'm 'POST'ing");
    if (this.user_input.length > 0) {
      this.http.post(this.uri, {input:this.user_input}).subscribe(res => (this.server_output  = JSON.stringify(res)));
    } else {
      this.user_input = ""
      this.server_output = ""
    }
}
}