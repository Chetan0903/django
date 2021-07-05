from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),

    path('', views.home, name="home"),
    path('viewbook/', views.viewbook, name="viewbook"),
    path('viewstudent/', views.viewstudent, name="viewstudent"),
    path('studentdetails/<str:pk_test>/', views.studentDetails, name="studentdetails"),
    path('bookdetails/<str:pk_test>/', views.bookDetails, name="bookdetails"),
    path('issuebook/<str:pk>/', views.bookIssue, name="issuebook"),
    path('returnbook/<str:pk>/', views.bookReturn, name="returnbook"),
    path('addbook/', views.addBook, name="addbook"),
    path('addstudent/', views.addStudent, name="addstudent"),
    
    path('updatestudent/<str:pk>/', views.updateStudent, name="updatestudent"),
    path('deletestudent/<str:pk>/', views.deleteStudent, name="deletestudent"),

    path('updatebook/<str:pk>/', views.updateBook, name="updatebook"),
    path('deletebook/<str:pk>/', views.deleteBook, name="deletebook"),
]
