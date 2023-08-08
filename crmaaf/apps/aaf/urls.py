from django.urls import path
from . import views


urlpatterns = [
    #path('', views.dontwork, name = 'dontwork'),
    path('', views.index, name = 'main_page'),
    path('contacts', views.contacts, name = 'contacts'),
    path('shareholder', views.shareholder, name = 'shareholder'),
    path('company/about_us', views.about_us, name = 'about_us'),
    path('company/history_us', views.history_us, name = 'history_us'),
     path('group', views.group, name = 'group'),
]