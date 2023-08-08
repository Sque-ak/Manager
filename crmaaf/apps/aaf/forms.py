from django import forms
from captcha.fields import ReCaptchaField
from crmaaf import settings

class ContactWithUsForm(forms.Form):
    name_user = forms.CharField(min_length=1)
    phone_user = forms.CharField(min_length=1)
    message_user = forms.CharField(min_length=1, widget=forms.Textarea)
    captcha = ReCaptchaField(public_key=settings.RECAPTCHA_PUBLIC_KEY,
                             private_key=settings.RECAPTCHA_PRIVATE_KEY)

class ContactWithUsFormProduct(forms.Form):
    name_user = forms.CharField(min_length=1)
    phone_user = forms.CharField(min_length=1)
    message_user = forms.CharField(min_length=1, widget=forms.Textarea)
    order_product = forms.CharField(required=False)
    count_product = forms.CharField(required=False)
    captcha = ReCaptchaField(public_key=settings.RECAPTCHA_PUBLIC_KEY,
                             private_key=settings.RECAPTCHA_PRIVATE_KEY)
    
    

