from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    #path('profile/', views.Profile, name="profile"),
    

]