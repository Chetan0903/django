
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from datetime import datetime,timedelta,date,timezone
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count


# Create your views here.

from library.forms import *
from library.models import Book,Student,IssueBook,BookCodes
from . import models
from library.filters import StudentFilter,BookFilter
from library.decorators import unauthenticated_user,allowed_users,admin_only




# Create your views here.

#REGISTRATION FUNCTION
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')  
            #messages.success(request, 'Account was created for ' + username)

            group = Group.objects.get(name='student')
            user.groups.add(group)
            Student.objects.create(
                user = user,
            )


            messages.success(request, 'Account was created for ' + username)
            return redirect('login')  
               
            
    context = {'form':form}
    return render(request, 'library/register.html', context)

#LOGIN FUNCTION
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:    
                messages.info(request, 'Username OR password is incorrect')
    
        
    context = {}
    return render(request, 'library/login.html', context)
    
#LOGOUT FUNCTION
def logoutUser(request):
	logout(request)
	return redirect('login')

#user info page
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userPage(request):
    book_issued = request.user.student.issuebook_set.all()
    book_count = book_issued.count()

    li2=[]
    for ib in book_issued:
        books=BookCodes.objects.filter(isbn=ib.book.isbn)
        
        days=(datetime.now(timezone.utc)-ib.issue_date)
        #print(date.today())
        d=days.days
        fine=0
        if d>1:
            day=d-1
            fine=day*10
        t = (ib.book.book.title,ib.book.isbn,ib.book.book.department,ib.issue_date,ib.return_date,fine)
        #print(t)
        li2.append(t)
        

    context = {'book_issued':book_issued,'book_count':book_count,'li2':li2}
    return render(request,'library/user.html', context)