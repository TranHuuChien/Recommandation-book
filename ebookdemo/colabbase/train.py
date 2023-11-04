import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle

books = pd.read_csv('./colabbase/book.csv')
books.rename(columns={
    'id': 'ISBN',
    "book_name": 'title',
    'author_name': 'auth',},
    inplace = True)
users = pd.read_csv('./colabbase/users.csv')
ratings = pd.read_csv('./colabbase/ratings.csv')

ratings.rename(columns={
    'book_id': 'ISBN',
}, inplace = True)
ratings = ratings[['user_id', 'ISBN', 'rating']]

x = ratings['user_id'].value_counts()>0
y = x[x].index
ratings = ratings[ratings['user_id'].isin(y)]

ratings_with_books = ratings.merge(books, on = 'ISBN')
num_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
num_rating.rename(columns={ 'rating': 'num_rating' }, inplace=True)

final_rating = ratings_with_books.merge(num_rating, on = "title")
final_rating.drop_duplicates(['user_id','title'], inplace= True)

final_rating = ratings_with_books.merge(num_rating, on = "title")
final_rating.drop_duplicates(['user_id', 'title'], inplace= True)

books_pivot = final_rating.pivot_table(columns='user_id', index='title', values='rating')
books_pivot.fillna(0, inplace=True)

book_sparse = csr_matrix(books_pivot)
model = NearestNeighbors(algorithm='brute')
model.fit(book_sparse)
book_name = books_pivot.index
pickle.dump(model, open('./colabbase/artifacts/model.pkl', 'wb'))
pickle.dump(book_name, open('./colabbase/artifacts/book_name.pkl', 'wb'))
pickle.dump(final_rating, open('./colabbase/artifacts/final_rating.pkl', 'wb'))
pickle.dump(books_pivot, open('./colabbase/artifacts/books_pivot.pkl', 'wb'))



