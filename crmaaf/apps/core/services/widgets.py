from django import forms
import datetime

class DateInput(forms.DateInput):
      """ This is widget for user can pick date.
      """
      input_type = 'date'
      pass
