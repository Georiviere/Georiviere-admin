from django import forms


class AdminFileWidget(forms.ClearableFileInput):
    template_name = "main/clearable_file_input.html"
