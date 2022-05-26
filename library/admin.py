from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Book)
admin.site.register(Student)
admin.site.register(IssueBook)
admin.site.register(RequestBook)
admin.site.register(HistoryBook)
admin.site.register(RatingNotifier)
