import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { DecisionDTO } from 'src/app/models/decision/decision.model';
import { OptionsDTO } from 'src/app/models/options/options.model';

@Injectable({
  providedIn: 'root',
})
export class HeatingService {
  private readonly hostname: string = 'http://localhost:5000';

  constructor(private readonly httpClient: HttpClient) {}

  public updateHeating(options: Array<OptionsDTO>): Observable<DecisionDTO> {
    let params: HttpParams = new HttpParams();
    params = params.append('people', this.getValue(options, 'PHM'));
    params = params.append('windowOpen', this.getValue(options, 'WOP'));
    params = params.append('warmDay', this.getValue(options, 'DHP'));
    params = params.append('warmNight', this.getValue(options, 'NHP'));
    params = params.append('temperature', 15);
    return this.httpClient.get<DecisionDTO>(`${this.hostname}/predict`, {
      params,
    });
  }

  private getValue(options: Array<OptionsDTO>, id: string): string {
    return options.find((option: OptionsDTO) => option.id === id).checked
      ? 'YES'
      : 'NO';
  }
}
