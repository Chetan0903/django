import csv

def main():
    file=open('books_data\data.csv')
    csvreader=csv.reader(file)
    return csvreader
main()


'''
for i in main():
    title=i[0].strip()
    author=i[1].strip()[1:-1]
    domain=i[2].strip()
    b=Book(title=title,author=author,domain=domain)
    b.save()
'''

'''
import random
def get_random_no():
    return random.randint(2,20)

bs=Book.objects.all()
for i in bs:
    count=get_random_no()
    while(count>0):
    isbn=''.join(random.choices(string.ascii_uppercase + string.digits, k=3))+'-'+''.join(random.choices(string.ascii_u 
    ppercase + string.digits, k=4))+'-'+''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    bc=BookCodes(book=i,status='Available',isbn=isbn)
    bc.save()
    count-=1

'''