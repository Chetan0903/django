from faker import Faker
file = open("users data\\ users_data.csv", "w")  # append mode

# fname,lname,username,email,password

fake = Faker()
for i in range(50):
    name=fake.name()
    fname,lname=name.split(' ')
    email=fake.email()
    password=fake.password()
    username=email.split('@')[0]
    print(fname,lname,email,password,username)
    file.write(f'{fname},{lname},{username},{email},"{password}"\n')
    
file.close()