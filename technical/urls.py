from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from technical import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('plotregestration/',views.plotregestration,name='plotregestration'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('test/', views.test,name='test'),
    path('add',views.add,name='add'),
    path('edit',views.edit,name='edit'),
    path('update/', views.update, name='update'),
    path('clup/', views.clup, name='clup'),
    path('delete', views.delete_plot, name='delete'),
    
]