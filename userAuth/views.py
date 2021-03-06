
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

from library.recommender import Recommender

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
    recommend=Recommender()
    r_titles=recommend.recommend(request.user)
    book_issued = request.user.student.issuebook_set.all()
    book_count = book_issued.count()
    recommended_books=[]
    for i in r_titles:
        # print(Book.objects.get(title=i))
        recommended_books.append(Book.objects.get(title=i))
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
        t = (ib.book.book.title,ib.book.isbn,ib.book.book.domain,ib.issue_date,ib.return_date,fine)
        #print(t)
        li2.append(t)
        
    context = {
        'book_issued':book_issued,'book_count':book_count,
        'li2':li2,
        'recommended':recommended_books
    }
    return render(request,'library/user.html', context)


'''
@login_required(login_url='login')
def Profile(request):
    if request.method=="POST":
        p_form=StudentForm(request.POST,instance=request.user.profile)
        imgUrl=request.user.profile.image.url
        path=''
        systemImgUrl=''
        
        if p_form.is_valid():
            os.remove(systemImgUrl)
            p_form.save()
            messages.success(request,f'account settings Updated!!!')
            return redirect('profile')
    else:
        p_form=StudentForm(instance=request.user.profile)
    context={
        #'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile.html',context)

'''