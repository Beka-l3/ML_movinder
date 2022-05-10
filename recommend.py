from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)
col = client['movierecommend']['movie']


def get_top_movies():
    top = col.find({}, {'_id': 1}).sort('rating.imdb', -1)[:1000]
    return top

def get_movie_df():
    movies = col.find({}, { '_id': 1, 'genres': 1, 'persons': 1} )
    ids = []
    genres = []
    directors = []
    actors = []
    for movie in movies:
        ids.append(movie['_id'])
        if movie['genres']:
            genres.append([genre['_id'] for genre in movie['genres']][:3])
        else:
            genres.append([])
        directors.append(
            [str(person['id']) for person in movie['persons'] if person['enProfession'] == 'director'][:1] * 3
        )
        actors.append(
            [str(person['id']) for person in movie['persons'] if person['enProfession'] == 'actor'][:3]
        )


    movies_df = pd.DataFrame(data={'id': ids, 'genres' : genres, 'director': directors, 'actors': actors})
    movies_df['soup'] = movies_df['genres'] + movies_df['director'] + movies_df['actors']
    movies_df['soup'] = movies_df['soup'].apply(lambda x: ' '.join(x))
    movies_df['id'] = movies_df['id'].astype('str')
    return movies_df

class CountModel:
    def __init__(self):
        self.movies_df = get_movie_df()
        self.count_vectorizer = CountVectorizer(analyzer='word', stop_words='english')
        self.count_matrix = self.count_vectorizer.fit_transform(self.movies_df['soup'])
        self.top = [str(id['_id']) for id in get_top_movies()]

    def exceprions_to_ids(self, exceptions):
        ids = []
        for i in exceptions:
            ids.append(self.movies_df[self.movies_df['id'] == i].index[0])
        return ids

    def recommend_on_ids(self, ids, exceptions):
        exception_ids = self.exceprions_to_ids(exceptions+ids)
        user_count = self.count_vectorizer.transform([self.movies_df[self.movies_df.id == id]['soup'].iloc[0] for id in ids])
        cos_similarity_count = map(lambda x: cosine_similarity(user_count, x), self.count_matrix)
        output_count = list(cos_similarity_count)
        top = sorted(range(len(output_count)), key=lambda i: sum(output_count[i]), reverse=True)
        for i in exception_ids:
            if i in top:
                top.remove(i)

        top = top[:10]
        ids = list(self.movies_df.loc[top]['id'])
        return ids

    def recommend_top(self, exceptions):
        result = self.top
        for i in exceptions:
            if i in result:
                result.remove(i)
        return result[:10]

class KNNModel:
    def __init__(self):
        self.movies_df = get_movie_df()
        self.count_vectorizer = CountVectorizer(analyzer='word', stop_words='english')
        self.count_matrix = self.count_vectorizer.fit_transform(self.movies_df['soup'])
        self.top = [str(id['_id']) for id in get_top_movies()]

    def exceprions_to_ids(self, exceptions):
        ids = []
        for i in exceptions:
            ids.append(self.movies_df[self.movies_df['id'] == i].index[0])
        return ids

    def recommend_on_ids(self, movie_id, exceptions):
        if len(self.movies_df[self.movies_df.id == movie_id]) == 0:
            return []
        exception_ids = self.exceprions_to_ids(exceptions+[movie_id])
        user_count = self.count_vectorizer.transform([self.movies_df[self.movies_df.id == movie_id]['soup'].iloc[0]])
        KNN = NearestNeighbors(n_neighbors = 100, p = 2)
        KNN.fit(self.count_matrix)
        NNs = KNN.kneighbors(user_count, return_distance = True)
        top = NNs[1][0].tolist()
        for i in exception_ids:
            if i in top:
                top.remove(i)

        top = top[:10]
        ids = list(self.movies_df.loc[top]['id'])
        return ids

    def recommend_top(self, exceptions):
        result = self.top
        for i in exceptions:
            if i in result:
                result.remove(i)
        return result[:10]
