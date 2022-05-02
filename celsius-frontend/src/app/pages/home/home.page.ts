import { Component } from '@angular/core';
import { OptionsDTO } from 'src/app/models/options/options.model';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  public readonly options: Array<OptionsDTO> = [
    { name: 'Window opened', checked: true },
    { name: 'People at home', checked: true },
    { name: 'Option 3', checked: true },
    { name: 'Option 4', checked: true },
    { name: 'Option 5', checked: false },
  ];

  constructor() {}
}
