import requests
from bs4 import BeautifulSoup

branch=input("enter branch  ").strip().split(' ')

param='+'.join(branch)

branch_name=" ".join([i.capitalize() for i in branch])

print(param,branch_name)

count=1

while count<=5:
    # url="https://www.goodreads.com/search?q=mechanical+engineering&qid=vYZOP59sJ9"
    url=f"https://www.goodreads.com/search?q={param}&page={count}"

    page=requests.get(url)
    print(page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup.prettify())
    txt=soup.find_all('table')[0]

    titles=txt.find_all('a',class_="bookTitle")
    authors=txt.find_all('a',class_="authorName")
    ratings=txt.find_all('span',class_="minirating")

    rating_handler=open("books_data\\book_ratings.csv",'a',encoding='utf-8')

    length=len(titles)

    for i in range(length):
        rating=str(ratings[i].contents[-1].string)
        title=titles[i].span.text
        author=authors[i].span.text
        print(title,author,rating)
        rating_handler.write(f'"{title}", "{author}", {branch_name}, {rating}\n')

    count+=1

    rating_handler.close()

