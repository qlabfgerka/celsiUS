import { Component, OnInit } from '@angular/core';
import {
  FormArray,
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { OptionsDTO } from 'src/app/models/options/options.model';
import { StorageService } from 'src/app/services/storage/storage.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  public optionsForm: FormGroup;
  public options: Array<OptionsDTO>;
  public timeout: any;
  public decision: string = 'OFF';

  private readonly TIMEOUT_LENGTH = 5000;
  private readonly LS_OPTS = 'LS_OPTS';

  constructor(
    private readonly formBuilder: FormBuilder,
    private readonly storageService: StorageService
  ) {}

  async ngOnInit(): Promise<void> {
    await this.refreshOptions();
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

  private async refreshOptions(): Promise<void> {
    this.options = JSON.parse(await this.storageService.get(this.LS_OPTS));
    if (!this.options) {
      this.options = [
        { name: 'Day heating preference', checked: false, id: 'DHP' },
        { name: 'Night heating preference', checked: false, id: 'NHP' },
      ];
      this.saveOptions();
    }
  }

  private async detectChanges(): Promise<void> {
    this.optionsForm.valueChanges.subscribe(async (changes) => {
      if (this.timeout) clearTimeout(this.timeout);

      for (const key in changes) {
        this.options.find((option: OptionsDTO) => option.id === key).checked =
          changes[key];
      }
      await this.saveOptions();

      this.timeout = setTimeout(() => {
        //POST options to backend
        this.initForm();
      }, this.TIMEOUT_LENGTH);
    });
  }

  private async saveOptions(): Promise<void> {
    await this.storageService.set(this.LS_OPTS, JSON.stringify(this.options));
  }
}
