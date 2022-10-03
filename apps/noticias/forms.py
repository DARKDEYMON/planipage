from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import *

class SearchForm(forms.Form):
	search = forms.CharField(required=False, label="", help_text="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Buscar...','autocomplete':'off'}))

class PublicacionForm(forms.ModelForm):
	class Meta:
		model = Publicacion
		fields = '__all__'

archivos_inline_form = inlineformset_factory(Publicacion, Archivo, exclude=[''], extra=1, can_delete=True)

class PaginaForm(forms.ModelForm):
	class Meta:
		model = Pagina
		exclude = ['']

class TipoForm(forms.ModelForm):
	class Meta:
		model = Tipo
		exclude = ['']

class DepartemanetoForm(forms.ModelForm):
	class Meta:
		model = Departamento
		exclude = ['']

class AutoridadesForm(forms.ModelForm):
	class Meta:
		model = Autoridades
		exclude = ['']

class ArchivosHelperForm(FormHelper):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.form_method = 'post'
		self.layout = Layout(
			Row(
				Column('archivo'),
				Column('prioridad'),
				css_class='g-1'
			)
		)
		self.render_required_fields = True
		self.form_tag = False