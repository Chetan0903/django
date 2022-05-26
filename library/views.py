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
from jsonschema import ValidationError

from django.core.mail import send_mail
# Create your views here.

from .forms import *
from .models import Book, HistoryBook,Student,IssueBook,BookCodes
from . import models
from .filters import StudentFilter,BookFilter
from .decorators import unauthenticated_user,allowed_users,admin_only

#To add student
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addStudent(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            # adding user and student
            name=user_form.cleaned_data['first_name']
            user_form.save()
            # adding to student group
            username=user_form.cleaned_data['username']
            curr_student_user=User.objects.get(username=username)
            group = Group.objects.get(name='student')
            curr_student_user.groups.add(group)
            # fixing issues
            prn=student_form.cleaned_data['prn_no']
            branch=student_form.cleaned_data['branch']
            contact=student_form.cleaned_data['contact_no']
            # print(prn,branch,contact)
            Student.objects.create(user=curr_student_user,
                prn_no=prn,
                contact_no=contact,
                name=name,
                branch=branch
            )            
            messages.success(request, (f'Student {username} added successfully...'))
            return redirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = CreateUserForm()
        student_form = StudentForm()
    return render(request, 'library/addstudent_form.html', {
        'user_form': user_form,
        'student_form': student_form
    })


#home page
@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, 'library/home.html')

#show all books

@login_required(login_url='login')
def viewbook(request):
    books = Book.objects.all()
    #For search
    myFilter = BookFilter(request.GET,queryset=books)
    books = myFilter.qs
    booksCountTotal=list()
    booksCountAvl=list()
    requestForThatBook=list()
    for book in books:
        booksCountTotal.append(BookCodes.objects.filter(book__title=book.title).count())
        booksCountAvl.append(BookCodes.objects.filter(book__title=book.title).filter(status='Available').count())
        requestForThatBook.append(book.requestbook_set.count())
    
    booksCount=zip(tuple(booksCountTotal),tuple(booksCountAvl),tuple(requestForThatBook))
    #print(booksCount)
    booksCount=tuple(booksCount)#zip of total books and available books
    #for i in booksCount:
     #   print(i)
    #print(booksCount)
    books=zip(books,booksCount)
    
    context = {'books':books,'myFilter': myFilter}
    return render(request,'library/viewbook.html', context)


#show all students

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewstudent(request):
    student = models.Student.objects.exclude(prn_no__exact='')
    #For search
    myFilter = StudentFilter(request.GET,queryset=student)
    student = myFilter.qs

    context ={'student':student,'myFilter': myFilter}
    return render(request,'library/viewstudent.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studentRequested(request,pk):
    student=Student.objects.get(pk=pk)
    if(request.method=="POST"):
        requestedBook=Book.objects.get(title=request.POST.get('book'))
        alreadyRequestedBook=RequestBook.objects.filter(book=requestedBook).filter(student=student).first()
        alreadyRequestedBook.delete()
    requested=RequestBook.objects.filter(student__id=pk)
    #print(requested)
    return render(request,'library/studentRequestedList.html',{'requested':requested})

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

        t = (ib.book.book.title,ib.book.isbn,ib.book.book.domain,ib.issue_date,ib.return_date,fine,ib.id)
        li2.append(t)
        
    context ={'student':student,'book_issued': book_issued,'book_count':book_count,'li2':li2}
    return render(request, 'library/student_details.html',context)


#show details of individual book
@login_required(login_url='login')
def bookDetails(request, pk_test):
    requestedUser=Student.objects.filter(user__username=request.user).first()#user who requested book
    if(request.method=='POST'):
        action=request.POST.get('act')
        requestedBook=Book.objects.get(title=request.POST.get('book'))#book title
        #print(request.user.student)
        if(action=='request'):
            requestForBook=RequestBook(book=requestedBook,student=requestedUser)#RequestBook object
            #print(requestForBook)
            requestForBook.save()
        else:#action=cancel
            alreadyRequestedBook=RequestBook.objects.filter(book=requestedBook).filter(student=requestedUser).first()
            alreadyRequestedBook.delete()
        return redirect('/')
    book = Book.objects.get(id=pk_test)
    # book_issued = student.issuebook_set.all()
    #book_count = book_issued.count()
    totalBooks=book.bookcodes_set.all().count()
    availableBooks=book.bookcodes_set.filter(status='Available')
    availableBooksCount=availableBooks.count()
    #print(isRequestedAlready,'isalready')#isRequestedAlready is queryset
    isIssuedAlready=0
    isRequestedAlready=0

    if( IssueBook.objects.filter(student=requestedUser).filter(book__book=book).count()!=0 ):#checking if book is issued alredy
        isIssuedAlready=1
        isRequestedAlready=0#removing cancel option for that book if already issued
    if(RequestBook.objects.filter(student=requestedUser).filter(book=book).count()>0):#only requested but not got issued
        isRequestedAlready=1
    #print(totalBooks,availableBooks)
    form=RequestForm()
    context ={
        'book':book,
        'totalBooks':totalBooks,
        'availableBooks':availableBooks,
        'availableBooksCount':availableBooksCount,
        'isRequestedAlready':isRequestedAlready,
        'isIssuedAlready':isIssuedAlready
        }
    return render(request, 'library/book_details.html',context)


#issue a book
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def bookIssue(request, pk):  

    student = Student.objects.get(id=pk)

    form = IssueForm(initial={'student':student},userId=student.id)

    if request.method == 'POST':
        form = IssueForm(request.POST,initial={'student':student},userId=student.id)
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
            ib=IssueBook.objects.filter(student=student,book=book).first()
            rn=RatingNotifier(book_to_rate=ib)
            rn.save()
            
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
        rate_given=bookInIssueBook.ratingnotifier.rating
        h=HistoryBook(rating=rate_given,book_copy=bookInIssueBook.book,student=bookInIssueBook.student)
        h.save()
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
            return redirect('addBookOptions')
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
            return redirect('addBookOptions')
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
    #print(request.POST,pk_test)
    if request.method=="POST":
        print('captured request')
        requestUserPrn=request.POST.get('student')
        student=Student.objects.get(prn_no=requestUserPrn)
        books=BookCodes.objects.filter(book__title=request.POST.get('book')).filter(status='Available')
        print(books,len(books))
        if(len(books)==0):
            return HttpResponse("<p>No books available at this time</p>")
        else:
            book=books.first()
            book.status='Not Available'
            book.save()
            #create issuebook obj 
            issueObj=IssueBook(book=book,student=student)
            issueObj.save()
            rn=RatingNotifier(book_to_rate=issueObj)
            rn.save()
            #deleting request for that book
            #print('request book deletion')
            RequestBook.objects.filter(student=student).filter(book__title=book.book.title).first().delete()
            return redirect(reverse('viewRequestedBook', kwargs={"pk_test": pk_test}))

    requested=RequestBook.objects.filter(book__id=pk_test).order_by('timestamp')
    #print(requested)
    #print("inside viewrequested book section")
    book = Book.objects.get(id=pk_test)
    totalBooks=book.bookcodes_set.all().count()
    availableBooks=book.bookcodes_set.filter(status='Available')
    availableBooksCount=availableBooks.count()
    #form=RequestForm()
    context ={
        'book':book,
        'totalBooks':totalBooks,
        'availableBooks':availableBooks,
        'availableBooksCount':availableBooksCount,
        'requested':requested,
        }
    
    return render(request,'library/requestedBookList.html',context)




#To update student info
@login_required(login_url='login')
def updateStudent(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student) 
    print(student)
    if request.method == 'POST':
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            messages.success(request,f'student {student.name} with {student.prn_no} updated successfully!!')
            return redirect('/')
        else:
            print("not valid")


    context ={'form': form}
    return render(request, 'library/update_student_form.html', context)

@login_required
@allowed_users(allowed_roles=['student'])
def gather_notifications(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        return redirect('rate_book',id)
    book_issued = request.user.student.issuebook_set.filter(ratingnotifier__has_rated=False)
    context={
        'issued':book_issued
    }
    return render(request,'library/notifications_form.html',context=context)

@login_required
@allowed_users(allowed_roles=['student'])
def rate_book(request,pk):
    book_to_rate=IssueBook.objects.get(id=pk)
    stud_of_book=book_to_rate.student
    if(request.user.student!=stud_of_book):
        return HttpResponse("Page doesn't exist")
    elif(book_to_rate.ratingnotifier.has_rated==True):
        return HttpResponse("you already rated")
    else:
        context={
            'title':book_to_rate.book.book.title
        }
        if(request.method=='POST'):
            rating=request.POST.get('rating')
            rn=RatingNotifier.objects.get(book_to_rate=book_to_rate)
            rn.rating=rating
            rn.has_rated=True
            rn.save()
            file=open("ratings_data\\rating.csv", "a")
            file.write(f'{book_to_rate.book.book.title},{book_to_rate.book.isbn},{request.user.student.prn_no},{rn.rating}\n')
            print("writen")
            file.close()
            return redirect('user-page')

        form=RatingForm()
        context['form']=form
    return render(request,'library/rating_template.html',context=context)

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


def sendmail(request):
     
    student = Student.objects.all()
    for stud in student:
        book_issued = stud.issuebook_set.all()
        for ib in book_issued:
            book = ib.book.book.title
            print(book)
            days=(datetime.now(timezone.utc)-ib.issue_date)
            d=days.days
            #li=[]
            if d>14:
                #li.append(book)
                send_mail(
                'DUE BOOKS',
                f'Dear Student, check the deadlines and kindly return the due books {book}.',
                'dyplibrary10@gmail.com',
                [stud.user.email],
                fail_silently=False,
                )
    #return render(request, 'library/home.html')
    return HttpResponse("Done")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def report_generation(request):
    return render(request,'library/report_home.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def report_studentwise(request):
    if request.method == 'POST':
        print("post")
        prn=request.POST.get('prn')
        print(prn)
        try:
            student=Student.objects.get(prn_no=prn)
            return redirect('show_student_report',student.prn_no)
        except Student.DoesNotExist:
            return HttpResponse("PRN not found")
    else:
        print("get")
    return render(request,'library/report_student_wise_form.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def display_student_wise_data(request,prn):
    student=Student.objects.get(prn_no=prn)
    historyb=HistoryBook.objects.filter(student=student)
    issueb=IssueBook.objects.filter(student=student)
    requestb=RequestBook.objects.filter(student=student)
    context={
        'student':student,
        'historyb':historyb,
        'issueb':issueb,
        'requestb':requestb
    }
    return render(request,'library/display_student_report.html',context)