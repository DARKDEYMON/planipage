from django.views.generic import ListView, FormView
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import CharField
from django.db.models.functions import Cast
from .forms import *

class ListSearchView(ListView):
	form_class = SearchForm
	fields_search = []
	ordering = '-id'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class()
		if self.request.GET:
			context['form'] = self.form_class(self.request.GET)
		return context
	def get(self, *args, **kwargs):
		self.search = None
		if self.request.method == "GET" and 'search' in self.request.GET:
			form = self.form_class(self.request.GET)
			if form.is_valid():
				self.search = form.cleaned_data['search']
				if self.search=='':
					return HttpResponseRedirect(self.request.path)
		return super().get(*args, **kwargs)
	def search_fields(self, query):
		search = self.search
		if (search and len(self.fields_search)!=0):
			trigram = None
			for field in self.fields_search:
				#self.model._meta.get_field(field)
				if trigram==None:
					trigram = TrigramSimilarity(Cast(field, CharField()),search)
				else:
					trigram = trigram + TrigramSimilarity(Cast(field, CharField()),search)
			return query.annotate(
				similarity = trigram
			).order_by('-similarity')
		else:
			return query
	def get_queryset(self):
		query = super().get_queryset()
		return self.search_fields(query)

class ModelExtraView(FormView):
	#model_extra
	def get_context_data(self, *args , **kwargs):
		context = super().get_context_data(*args, **kwargs)
		if 'object_extra' not in context and hasattr(self, 'model_extra'):
			context['object_extra'] = self.model_extra.objects.get(id=self.kwargs['pk'])
		return context