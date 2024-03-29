from django.views.generic import ListView, FormView
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.db.models import CharField
from django.db.models.functions import Cast
from .forms import *

class ListSearchView(ListView):
	form_class = SearchForm
	fields_search = []
	#ordering = '-id'
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
				#if self.search=='':
				#	return HttpResponseRedirect(self.request.path)
		redirect = self.get_page_object_is_on()
		if(redirect):
			return redirect
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
					trigram = trigram + TrigramSimilarity(Coalesce(Cast(field, CharField()),Value('')),search)
			return query.annotate(
				similarity = trigram
			).order_by('-similarity')
		else:
			return query
	def get_queryset(self):
		query = super().get_queryset()
		return self.search_fields(query)
	def get_page_object_is_on(self):
		if self.request.method == 'GET':
			if('idpage' in self.request.GET and hasattr(self, 'paginate_by')):
				idpage = int(self.request.GET['idpage'])
				idoriginalobj = int(self.request.GET['idoriginalobj'] if self.request.GET.get('idoriginalobj','')!='' else idpage)
				redirectlistnameid = self.request.GET.get('redirectlistnameid','')
				query = self.get_queryset().values_list('id', flat=True)
				model_ids = list(query)
				page = model_ids.index(idpage) // self.get_paginate_by(self.get_queryset()) + 1
				return HttpResponseRedirect(self.request.path + '?page=' + str(page) + '#' + redirectlistnameid + str(idoriginalobj))
			else:
				return None
		else:
			return None

class ModelExtraView(FormView):
	#model_extra
	def get_context_data(self, *args , **kwargs):
		context = super().get_context_data(*args, **kwargs)
		if 'object_extra' not in context and hasattr(self, 'model_extra'):
			context['object_extra'] = self.model_extra.objects.get(id=self.kwargs['pk'])
		return context