import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import random
from library.models import HistoryBook

class Recommender():
    def __init__(self):
        self.books=None
        self.ratings=None
        self.studs=None
    def read_data(self):
        self.books = pd.read_csv('books_data\\data.csv',sep=',',error_bad_lines=False)
        self.books.columns=['Title','Author','Domain']
        # print(self.books.head())
        self.studs=pd.read_csv('stud_data\\stud_data.csv',sep=',')
        self.studs.columns=['name','prn','username']
        self.ratings=pd.read_csv('ratings_data\\rating.csv',sep=',')
        self.ratings.columns=['Title','isbn','prn','rating']

    def clean_up(self):
        self.read_data()
        self.book_ratingCount = (self.ratings.
            groupby(by = ['Title'])['rating'].
            count().
            reset_index().
            rename(columns = {'rating': 'totalRatingCount'})
            [['Title', 'totalRatingCount']]
            )
        self.ratings=self.ratings.drop_duplicates(['prn', 'Title'])

    def recommend(self,user):
        self.clean_up()
        self.ratings_pivot = self.ratings.pivot(index='prn', columns='isbn').rating
        self.ratings_pivot = self.ratings.pivot(index = 'Title', columns = 'prn', values = 'rating').fillna(0)
        self.ratings_matrix = csr_matrix(self.ratings_pivot.values)
        model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
        model_knn.fit(self.ratings_matrix)
        recommended_books=[]
        history_books=[]
        # print(self.ratings_pivot.head())
        new1= self.ratings_pivot.reset_index(level=0)
        for i in HistoryBook.objects.filter(student=user.student):
            title=i.book_copy.book.title
            try:
                id=new1.index.get_loc(new1.index[new1['Title'] == title][0])
                history_books.append(id)
            except:
                print("error occured")
        query_index=random.choice(history_books)
        distances, indices = model_knn.kneighbors(self.ratings_pivot.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)
        print(self.ratings_pivot.index[query_index])
        for i in range(0, len(distances.flatten())):
            if i != 0:
                recommended_books.append(self.ratings_pivot.index[indices.flatten()[i]])
                # print('{0}: {1}, with distance of {2}:'.format(i, self.ratings_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
        return recommended_books
        


