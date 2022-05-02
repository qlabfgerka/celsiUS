import { Component, OnInit } from '@angular/core';
import {
  FormArray,
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { OptionsDTO } from 'src/app/models/options/options.model';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  public optionsForm: FormGroup;
  public options: Array<OptionsDTO>;
  public timeout: any;

  private readonly TIMEOUT_LENGTH = 5000;

  constructor(private readonly formBuilder: FormBuilder) {}

  ngOnInit(): void {
    this.refreshOptions();
    this.initForm();
  }

  public get opts(): FormArray {
    return this.optionsForm.get('opts') as FormArray;
  }

  private initForm(): void {
    this.optionsForm = this.formBuilder.group({});
    for (const option of this.options) {
      this.optionsForm.addControl(
        option.id,
        this.formBuilder.control(option.checked, Validators.required)
      );
    }
    this.detectChanges();
  }

  private refreshOptions(): void {
    this.options = [
      { name: 'Window opened', checked: true, id: 'WOPN' },
      { name: 'People at home', checked: true, id: 'PATH' },
      { name: 'Option 3', checked: true, id: 'OPT3' },
      { name: 'Option 4', checked: true, id: 'OPT4' },
      { name: 'Option 5', checked: false, id: 'OPT5' },
    ];
  }

  private detectChanges(): void {
    this.optionsForm.valueChanges.subscribe((changes) => {
      if (this.timeout) clearTimeout(this.timeout);

      this.timeout = setTimeout(() => {
        for (const key in changes) {
          this.options.find((option: OptionsDTO) => option.id === key).checked =
            changes[key];
        }

        //POST options to backend
        this.initForm();
      }, this.TIMEOUT_LENGTH);
    });
  }
}
