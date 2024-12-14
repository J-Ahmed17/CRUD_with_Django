from django.urls import path
from . import views

urlpatterns = [

    
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('receipe/', views.receipe, name='receipe'),
    path('delete-receipe/<id>/', views.delete_receipe, name="delete_receipe"),
    path('update-receipe/<id>/', views.update_receipe, name="update_recipe"),
    path('logout/', views.logout, name="logout"),
]
