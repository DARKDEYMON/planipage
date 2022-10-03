from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .generic import *
from .forms import *
from .models import *
from constance import config

# Create your views here.

def Main(request):
	publicaciones = Publicacion.objects.filter(publicar=True).prefetch_related('archivo_set','tipo','tipo__departamento')[:20]
	return render(request,'main.html', {'publicaciones':publicaciones})

def nosotros(request):
	autoridades = Autoridades.objects.all()
	return render(request, 'nosotros.html',{'autoridades':autoridades,'config':config})

def publicacion_view(request, pk):
	noticia = Publicacion.objects.prefetch_related('archivo_set').get(id=pk)
	return render(request, 'publicacion.html',{'noticia':noticia})

class CreatePublicacionView(CreateView):
	form_class = PublicacionForm
	template_name = 'publicacion/create_publicacion.html'
	success_url = 'noticias:archivo_inline'
	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs={'pk':self.object.id})

class UpdatePublicaionView(UpdateView):
	model = Publicacion
	form_class = PublicacionForm
	template_name = 'publicacion/update_publicacion.html'
	success_url = 'noticias:archivo_inline'
	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs={'pk':self.object.id})

class ListPublicacionView(ListSearchView):
	model = Publicacion
	paginate_by = 10
	template_name = 'publicacion/list_publicaion.html'
	fields_search = ['id','nombre','tipo','publicar']

def archivo_inline_view(request, pk):
	instance = get_object_or_404(Publicacion, id=pk)
	fom_inline = archivos_inline_form
	helper = ArchivoHelperForm()
	if request.method == 'POST':
		formset = fom_inline(request.POST, request.FILES, instance=instance)
		if formset.is_valid():
			formset.save()
			if 'add' in request.POST:
				return HttpResponseRedirect(request.path)
			else:
				return HttpResponseRedirect(reverse_lazy('noticias:list_publicacion'))
	else:
		formset = fom_inline(instance=instance)
	return render(request, 'publicacion/archivos_inline.html',{'formset':formset, 'helper':helper, 'instance':instance})

class ListPublicacionBusquedaView(ListSearchView):
	model = Publicacion
	paginate_by = 10
	template_name = 'publicacion/list_publicaion_search.html'
	fields_search = ['id','nombre','tipo','publicar']

class ListPaginasView(ListSearchView):
	model = Pagina
	paginate_by = 10
	template_name = 'paginas/list_paginas.html'
	fields_search = ['id','nombre','url']

class CreatePaginaView(CreateView):
	form_class = PaginaForm
	template_name = 'paginas/create_paginas.html'
	success_url = reverse_lazy('noticias:list_paginas')

class UpdatePaginaView(UpdateView):
	model = Pagina
	form_class = PaginaForm
	template_name = 'paginas/update_pagina.html'
	success_url = reverse_lazy('noticias:list_paginas')

#tipos
class ListTiposView(ListSearchView):
	model = Tipo
	paginate_by = 10
	template_name = 'tipo/list_tipos.html'
	fields_search = ['id','tipò']

class CreateTipoView(CreateView):
	form_class = TipoForm
	template_name = 'tipo/create_tipo.html'
	success_url = reverse_lazy('noticias:list_tipo')

class UpdateTipoView(UpdateView):
	model = Tipo
	form_class = TipoForm
	template_name = 'tipo/update_tipo.html'
	success_url = reverse_lazy('noticias:list_tipo')

#Departamento
class ListDepartamentoView(ListSearchView):
	model = Departamento
	paginate_by = 10
	template_name = 'departamento/list_departamento.html'
	fields_search = ['id','tipo']

class CreateDepartamentoView(CreateView):
	form_class = DepartemanetoForm
	template_name = 'departamento/create_departamento.html'
	success_url = reverse_lazy('noticias:list_departamento')

class UpdateDepartamentoView(UpdateView):
	model = Departamento
	form_class = DepartemanetoForm
	template_name = 'departamento/update_departamento.html'
	success_url = reverse_lazy('noticias:list_departamento')

#lista filtrada
class ListPublicacionFiltroBusquedaView(ListSearchView, ModelExtraView):
	model_extra = Tipo
	model = Publicacion
	paginate_by = 10
	template_name = 'publicacion/list_publicaion_filtro_search.html'
	fields_search = ['id','nombre','tipo','publicar']
	def get_queryset(self):
		query = super().get_queryset().filter(tipo__id=self.kwargs['pk'])
		return self.search_fields(query)

#Autoridades
class ListAutoridadesView(ListSearchView):
	model = Autoridades
	paginate_by = 10
	template_name = 'autoridades/list_autoridades.html'
	fields_search = ['id','nombre']

class CreateAutoridadesView(CreateView):
	form_class = AutoridadesForm
	template_name = 'autoridades/create_autoridades.html'
	success_url = reverse_lazy('noticias:list_autoridades')

class UpdateAutoridadesView(UpdateView):
	model = Autoridades
	form_class = AutoridadesForm
	template_name = 'autoridades/update_autoridades.html'
	success_url = reverse_lazy('noticias:list_autoridades')