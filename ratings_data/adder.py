from django.contrib.auth.models import User
from library.models import *
import random

stud_lst=Student.objects.filter(branch='Civil')
def get_total_rate_by_student():
        return random.randint(6,12)

def get_rating():
        return random.randint(1,5)


def get_books():
        return Book.objects.filter(domain__contains='Civil')


st=set() #set for user to isbn
bks=get_books()

for stud in stud_lst:
        total_rate=get_total_rate_by_student()
        while(total_rate>0):
                book=random.choice(bks)
                copy_to_rate=random.choice(book.bookcodes_set.all())
                if((stud,copy_to_rate) not in st):
                        st.add((stud,copy_to_rate))
                        # print(stud,copy_to_rate,get_rating())
                        h=HistoryBook(book_copy=copy_to_rate,student=stud,rating=get_rating())
                        h.save()
                total_rate-=1

