import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class StudentFilter(django_filters.FilterSet):
	#start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	#end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	name = CharFilter(field_name='name', lookup_expr='icontains')


	class Meta:
		model = Student
		fields = '__all__'
		exclude = ['email', 'contact_no','total_books_due','user']


class BookFilter(django_filters.FilterSet):
    	
	title = CharFilter(field_name='title', lookup_expr='icontains')
	author=CharFilter(field_name='author',lookup_expr='icontains')
	
	class Meta:
		model = Book
		fields = '__all__'
		exclude = [ 'available_copies','total_copies']        