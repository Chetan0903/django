import csv

import csv

def main():
    file=open('users_data\ users_data.csv')
    csvreader=csv.reader(file)
    return csvreader
main()



'''
for i in main():
    f,l,un,email,pwd=i
    u=User(first_name=f,last_name=l,email=email,username=un,password=pwd)
    u.save()
    u.set_password(pwd)
    u.save(update_fields=['password'])
    prn=''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    contact=''.join(random.choices(string.digits, k=10))
    u.groups.add(grp)
    s=Student(user=u,prn_no=prn,contact_no=contact,name=u.username,branch=random.choice(branches))
    s.save()
'''