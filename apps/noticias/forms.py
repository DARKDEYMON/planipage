from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from constance import config
from django.conf import settings
from .models import *

class SearchForm(forms.Form):
	search = forms.CharField(required=False, label="", help_text="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Buscar...','autocomplete':'off'}))

class PublicacionForm(forms.ModelForm):
	class Meta:
		model = Publicacion
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['contenido'].required = False

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

class ConstanceForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for key in self.Meta.constance_values.keys():
			data = self.Meta.constance_values[key]
			typo = self.getDataOrNone(data,2)
			if not typo or typo==str:
				self.fields[key] = forms.CharField(widget=forms.Textarea(),label=data[1], required=False, initial=getattr(self.Meta.constance,key))
			elif(typo==bool):
				self.fields[key] = forms.BooleanField(label=data[1], required=True, initial=getattr(self.Meta.constance,key))
			elif(typo==int):
				self.fields[key] = forms.IntegerField(label=data[1], required=True, initial=getattr(self.Meta.constance,key))
			elif(typo==float):
				self.fields[key] = forms.FloatField(label=data[1], required=True, initial=getattr(self.Meta.constance,key))
	def getDataOrNone(self, data, index):
		try:
			return data[index]
		except Exception as e:
			return None
	def save(self):
		for key in self.cleaned_data:
			setattr(self.Meta.constance, key, self.cleaned_data[key])
	class Meta:
		constance = config
		constance_values = settings.CONSTANCE_CONFIG
