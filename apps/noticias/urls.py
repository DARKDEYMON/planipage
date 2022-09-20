"""planipage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', Main, name='main'),
    path('publicacion/<int:pk>/', publicacion_view, name='publicacion'),
    path('createpublicaion/', login_required(CreatePublicacionView.as_view()), name='create_publicacion'),
    path('updatepublicaion/<int:pk>/', login_required(UpdatePublicaionView.as_view()), name='update_publicaion'),
    path('listpublicacion/', login_required(ListPublicacionView.as_view()), name='list_publicacion'),
    path('archivoinline/<int:pk>/', login_required(archivo_inline_view), name='archivo_inline'),
    path('search/', ListPublicacionBusquedaView.as_view(), name='search'),

    path('listpaginas/', login_required(ListPaginasView.as_view()), name='list_paginas'),
    path('createpagina/', login_required(CreatePaginaView.as_view()), name='create_pagina'),
    path('updatepagina/<int:pk>/', login_required(UpdatePaginaView.as_view()), name='update_pagina'),

    path('listtipo/', login_required(ListTiposView.as_view()), name='list_tipo'),
    path('createtipo/', login_required(CreateTipoView.as_view()), name='create_tipo'),
    path('updatetipo/<int:pk>/', login_required(UpdateTipoView.as_view()), name='update_tipo'),

    path('listdepartemento/', login_required(ListDepartamentoView.as_view()), name='list_departamento'),
    path('creardeparatmento/', login_required(CreateDepartamentoView.as_view()), name='create_departamento'),
    path('updatedepartamento/<int:pk>/', login_required(UpdateDepartamentoView.as_view()), name='update_departamento'),
]
