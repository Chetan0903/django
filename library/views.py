from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from datetime import datetime,timedelta,date,timezone
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group



# Create your views here.

from .forms import *
from .models import Book,Student,IssueBook,BookCodes
from . import models
from .filters import StudentFilter,BookFilter
from .decorators import unauthenticated_user,allowed_users,admin_only





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
        books=models.BookCodes.objects.filter(isbn=ib.book.isbn)
        
        days=(datetime.now(timezone.utc)-ib.issue_date)
        #print(date.today())
        d=days.days
        fine=0
        if d>1:
            day=d-1
            fine=day*10

        t = (ib.book.title,ib.book.isbn,ib.book.department,ib.issue_date,ib.return_date,fine)
        li2.append(t)
        

    context = {'book_issued':book_issued,'book_count':book_count,'li2':li2}
    return render(request,'library/user.html', context)


#home page

@login_required(login_url='login')
@admin_only
def home(request):
     return render(request, 'library/home.html')

#show all books

@login_required(login_url='login')
def viewbook(request):
    books = models.Book.objects.all()
    #For search
    myFilter = BookFilter(request.GET,queryset=books)
    books = myFilter.qs
    booksCountTotal=list()
    booksCountAvl=list()
    
    for i in books:
        booksCountTotal.append(BookCodes.objects.filter(book__title=i.title).count())
        booksCountAvl.append(BookCodes.objects.filter(book__title=i.title).filter(status='Available').count())
        #print(i,BookCodes.objects.filter(book__title=i.title).count())
    
    booksCount=zip(tuple(booksCountTotal),tuple(booksCountAvl))
    #print(booksCount)
    booksCount=tuple(booksCount)#zip of total books and available books

    #print(booksCount)
    books=zip(books,booksCount)
    
    context = {'books':books,'myFilter': myFilter}
    return render(request,'library/viewbook.html', context)


#show all students

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewstudent(request):
    student = models.Student.objects.all()
    #For search
    myFilter = StudentFilter(request.GET,queryset=student)
    student = myFilter.qs

    context ={'student':student,'myFilter': myFilter}
    return render(request,'library/viewstudent.html',context)


#show details of individual student
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def studentDetails(request, pk_test):
    student = Student.objects.get(id=pk_test)
    book_issued = student.issuebook_set.all()
    book_count = book_issued.count()   

    li2=[]
    for ib in book_issued:
        
        books=models.BookCodes.objects.filter(isbn=ib.book.isbn)
        
        days=(datetime.now(timezone.utc)-ib.issue_date)
       # print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-1
            fine=day*10

        t = (ib.book.book.title,ib.book.isbn,ib.book.book.department,ib.issue_date,ib.return_date,fine,ib.id)
        li2.append(t)
        
    context ={'student':student,'book_issued': book_issued,'book_count':book_count,'li2':li2}
    return render(request, 'library/student_details.html',context)


#show details of individual book
@login_required(login_url='login')
def bookDetails(request, pk_test):
    requestedUser=Student.objects.filter(user__username=request.user).first()#user who requested book
    if(request.method=='POST'):
        requestedBook=Book.objects.get(title=request.POST.get('book'))#book title
        print(request.user.student)
        requestForBook=RequestBook(book=requestedBook,student=requestedUser)#RequestBook object
        #print(requestForBook)
        requestForBook.save()
        return redirect(userPage)
    book = Book.objects.get(id=pk_test)
    # book_issued = student.issuebook_set.all()
    #book_count = book_issued.count()
    totalBooks=book.bookcodes_set.all().count()
    availableBooks=book.bookcodes_set.filter(status='Available')
    availableBooksCount=availableBooks.count()
    isRequestedAlready=RequestBook.objects.filter(student=requestedUser).filter(book=book)
    print(isRequestedAlready,'isalready')#isRequestedAlready is queryset
    if(isRequestedAlready.count()>0):#already has request
        isRequestedAlready=1
    #print(totalBooks,availableBooks)
    form=RequestForm()
    context ={
        'book':book,
        'totalBooks':totalBooks,
        'availableBooks':availableBooks,
        'availableBooksCount':availableBooksCount,
        'isRequestedAlready':isRequestedAlready
        }
    return render(request, 'library/book_details.html',context)


#issue a book
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def bookIssue(request, pk):  

    student = Student.objects.get(id=pk)

    form = IssueForm(pk,initial={'student': student})

    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            #field.book.status= 'Not Available'
            bk = form.cleaned_data['book']
            id = bk.id
            #print(id,bk,type(id),type(bk))
            book = BookCodes.objects.get(id=id)
            
            book.status = 'Not Available'
            book.save()
           # print(book.status)
           # print(ids)
           # print(bk)
            form.save()
            messages.success(request,f'book {book} issued successfully to {student}')
            return redirect('/')

    context ={'form': form}
    return render(request, 'library/issue_form.html', context) 



#return book
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def bookReturn(request, pk):
    #print("pk->", pk)
    bookInIssueBook = IssueBook.objects.get(id=pk)
    #print(bookInIssueBook,bookInIssueBook.book.isbn)
    if request.method == 'POST':
        bookInBookCodes=BookCodes.objects.get(isbn=bookInIssueBook.book.isbn)
        #print(bookInBookCodes)
        bookInIssueBook.delete()
        bookInBookCodes.status="Available"
        bookInBookCodes.save()
        return redirect('/')

    return render(request, 'library/returnbook.html', {'item': bookInIssueBook}) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addBookOptionsPage(request):
    return render(request,'library/addBookOptionsPage.html')


#To add new book
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addBook(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
           # return render(request,'library/bookadded.html')
    context ={'form': form}
    return render(request, 'library/addbook_form.html', context)

#To add new book
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addNewCopy(request):
    form = AddBookCopyForm()
    if request.method == 'POST':
        form = AddBookCopyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
           # return render(request,'library/bookadded.html')
    context ={'form': form}
    return render(request, 'library/addbook_form.html', context)

#To update book info
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
           # messages.success(request, 'Your details has been changed successfully!')
           
            return redirect('/' )


    context ={'form': form}
    return render(request, 'library/addbook_form.html', context)


#Delete Book
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('/')
    context ={'item': book}
    return render(request, 'library/deletebook.html', context)     


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewRequestedBook(request,pk_test):
    print(request.POST,pk_test)
    requested=RequestBook.objects.filter(book__id=pk_test).order_by('timestamp')
    print(requested)
    print("inside viewrequested book section")
    book = Book.objects.get(id=pk_test)
    totalBooks=book.bookcodes_set.all().count()
    availableBooks=book.bookcodes_set.filter(status='Available')
    availableBooksCount=availableBooks.count()
    form=RequestForm()
    context ={
        'book':book,
        'totalBooks':totalBooks,
        'availableBooks':availableBooks,
        'availableBooksCount':availableBooksCount,
        'requested':requested
        }
    
    return render(request,'library/requestedBookList.html',context)


#To add student
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addStudent(request):

    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context ={'form': form}
    return render(request, 'library/addstudent_form.html', context)


#To update student info
@login_required(login_url='login')
def updateStudent(request, pk):

    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')


    context ={'form': form}
    return render(request, 'library/addstudent_form.html', context)


#Delete Student
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteStudent(request, pk):
    
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/')

    context ={'item': student}

    return render(request, 'library/deletestudent.html', context)     


    