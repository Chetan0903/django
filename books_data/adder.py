import csv

def main():
    file=open('books_data\data.csv')
    csvreader=csv.reader(file)
    return csvreader
main()



'''
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