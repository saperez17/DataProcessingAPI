from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
# from backend.schema import schema  to import scheme

from .views import *
urlpatterns = [
    path('', index, name="home"),
    path("admin/", admin.site.urls),
    path('load_data', load_data, name='index'),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))), #second argument could be scheme=scheme
    path('api/customer-history', CustomerHistory.as_view(),name='customer-history')
]
