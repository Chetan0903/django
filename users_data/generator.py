from faker import Faker
file = open("users_data\\ users_data.csv", "w")  # write mode
# fname,lname,username,email,password

fake = Faker()
for i in range(150):
    name=fake.name()
    name_lst=name.strip().split()
    if 'Mr.' in name_lst: name_lst.remove('Mr.')
    if 'Mrs.' in name_lst: name_lst.remove('Mrs.')
    fname=name_lst[0]
    lname=name_lst[-1]
    email=fake.email()
    password='qwerty@123'
    username=email.split('@')[0]
    print(fname,lname,email,password,username)
    file.write(f'{fname},{lname},{username},{email},"{password}"\n')
    
file.close()