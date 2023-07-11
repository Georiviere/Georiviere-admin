from django import forms


class AdminFileWidget(forms.ClearableFileInput):
    template_name = "flatpages/clearable_file_input.html"
