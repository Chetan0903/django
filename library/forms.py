from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import IssueBook,Book, RequestBook,Student,BookCodes


class IssueForm(ModelForm):
    def __init__(self,pk,*args,**kwargs):
        super (IssueForm,self ).__init__(*args,**kwargs)
        self.fields['student'].queryset=Student.objects.filter(id=pk)
        self.fields['book'].queryset=BookCodes.objects.filter(status='Available')
    class Meta:
        model= IssueBook
        fields = '__all__'

class RequestForm(ModelForm):
    class Meta:
        model=RequestBook
        fields=[]

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'     

class AddBookCopyForm(ModelForm):
    class Meta:
        model = BookCodes
        fields = '__all__'   

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'        

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
		
		