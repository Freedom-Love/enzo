from django.forms import ModelForm, Form, DateField
from django.forms.extras import SelectDateWidget
from .models import Foto


class FotoForm(ModelForm):
    class Meta:
        model = Foto
        fields = ['titolo', 'img']

class GiornataForm(Form):
    data = DateField(widget=SelectDateWidget())