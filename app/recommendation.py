# coding: utf-8

# All the recommandation logic and algorithms goes here

from random import choice

from app.User import User


class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.simplified_ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings
        self.process_ratings_to_users()

    # To process ratings, users associated to ratings are created and every rating is then stored in its user
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            if hasattr(rating, 'is_appreciated'):
                if rating.is_appreciated:
                    user.good_ratings.append(movie)
                else:
                    user.bad_ratings.append(movie)
            if hasattr(rating, 'score'):
                user.ratings[movie.id] = rating.score

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        similarities=self.compute_all_similarities (user)
        similarities_and_user=zip(similarities, list(self.test_users.values()))
        similarities_and_user.sort(reverse=True)
        bestuser=similarities_and_user[0][1]
        recommandation=bestuser.good_ratings
        string_recommandation = [movie.title for movie in recommandation]

        return "Vos recommandations : " + ", ".join(string_recommandation)

    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        similarity=0
        user_a.good_ratings
        for goodratings in user_a.good_ratings:
            if goodratings in user_b.good_ratings:
                similarity=similarity+1
            if goodratings in user_b.bad_ratings:
                similarity=similarity-1
        for badratings in user_a.good_ratings:
            if badratings in user_b.bad_ratings:
                similarity=similarity+1
            if badratings in user_b.good_ratings:
                similarity=similarity-1
        return similarity 

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        similarities=[]
        for testuser in list(self.test_users.values()):
            self.get_similarity(user, testuser)
            similarities.append(self.get_similarity(user, testuser))

            
        return similarities

    @staticmethod
    def get_best_movies_from_users(users):
        return []

    @staticmethod
    def get_user_appreciated_movies(user):
        return []

    @staticmethod
    def get_user_norm(user):
        return 1

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []
