from django.forms.widgets import DateInput


class DatePickerInput(DateInput):
    """Date input widget using HTML5 date type and browser date picker"""
    input_type = "date"

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs)
        self.format = format or '%Y-%m-%d'
