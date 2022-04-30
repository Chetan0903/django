'''
from library.models import *
file=open('stud_data\\stud_data.csv','w')
a=Student.objects.all()
for i in a:
    name=i.name
    prn=i.prn_no
    username=i.user.username
    file.write(f'{name},{prn},{username}\n')
'''