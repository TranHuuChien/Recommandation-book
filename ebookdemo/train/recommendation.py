
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
import pickle

class Recommendation:
  def __init__(self, master):
    self.master = master

  df_book = pd.read_csv('./train/book2.csv')
  df_book["combined"] = df_book['book_name'] + '  ' + df_book['author_name'] + ' ' + df_book['genre_name']
  tfidf =  TfidfVectorizer(stop_words ='english')
  tfidf_matrix = tfidf.fit_transform(df_book["combined"])

  cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
  indices = pd.Series(df_book.index, index = df_book['book_name']).drop_duplicates()

  def get_recommendations(title,cosine_sim = cosine_sim):
  #get the index of the movie that matches the title
      index = Recommendation.indices[title]
      sim_scores = list(enumerate(cosine_sim[index]))
      sim_scores = sorted(sim_scores,key = lambda x:x[1], reverse = True)
      sim_scores = sim_scores[1:7]
      sim_index = [i[0] for i in sim_scores]
      pickle.dump(Recommendation.df_book['id'].iloc[sim_index], open('./train/books.pkl', 'wb'))



