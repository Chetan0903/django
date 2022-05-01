from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('notifications', views.gather_notifications, name="all_notifications"),
    path('rate_book/<int:pk>', views.rate_book, name="rate_book"),
    path('viewbook/', views.viewbook, name="viewbook"),
    path('viewstudent/', views.viewstudent, name="viewstudent"),
    path('studentdetails/<str:pk_test>/', views.studentDetails, name="studentdetails"),
    path('bookdetails/<str:pk_test>/', views.bookDetails, name="bookdetails"),
    path('bookdetails/requested/<str:pk_test>/', views.viewRequestedBook, name="viewRequestedBook"),#admin
    path('issuebook/<str:pk>/', views.bookIssue, name="issuebook"),
    path('returnbook/<str:pk>/', views.bookReturn, name="returnbook"),
    path('studentRequested/<str:pk>/', views.studentRequested, name="studentRequested"),#for student
    path('addbook/addnewbook', views.addBook, name="addbook"),
    path('addbook/addbookdetailspage/',views.addBookOptionsPage,name="addBookOptions"),
    path('addbook/addbookcopy/',views.addNewCopy,name='addbookcopy'),

    path('addstudent/', views.addStudent, name="addstudent"),
    
    path('updatestudent/<str:pk>/', views.updateStudent, name="updatestudent"),
    path('deletestudent/<str:pk>/', views.deleteStudent, name="deletestudent"),

    path('updatebook/<str:pk>/', views.updateBook, name="updatebook"),
    path('deletebook/<str:pk>/', views.deleteBook, name="deletebook"),
]
