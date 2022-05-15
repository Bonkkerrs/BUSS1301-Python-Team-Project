from category import MovieCategoryAcquirer, Category


class Movie:
    def __init__(self, id, rank, title, score, regions, types, vote_count, actors):
        self.id = id
        self.rank = rank
        self.title = title
        self.score = score
        self.regions = regions
        self.types = types
        self.vote_count = vote_count
        self.actors = actors


class RankingCrawler:
    def __init__(self, category_obj, query_limit):
        self.category = category_obj
        self.raw_info = category_obj.query_list(query_limit)
        self.movie_list = RankingCrawler.parse_info(self.raw_info)

    @staticmethod
    def parse_info(raw_info):
        movie_list = []
        for movie_info in raw_info:
            id = movie_info['id']
            rank = movie_info['rank']
            title = movie_info['title']
            score = movie_info['score']
            regions = movie_info['regions']
            types = movie_info['types']
            vote_count = movie_info['vote_count']
            actors = movie_info['actors']
            m = Movie(id, rank, title, score, regions, types, vote_count, actors)
            movie_list.append(m)
        return movie_list


if __name__ == '__main__':
    c = MovieCategoryAcquirer().category_list[0]
    r = RankingCrawler(c, 100)
    print(r.movie_list)
