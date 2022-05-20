import requests
# from category import MovieCategoryAcquirer, Category
from lxml import etree
import tqdm


class Movie:
    def __init__(self, id, rank, title, score, regions, types, vote_count, actors, release_date):
        self.id = id
        self.rank = rank
        self.title = title
        self.score = score
        self.regions = regions
        self.types = types
        self.vote_count = vote_count
        self.actors = actors
        self.release_date = release_date
    
    def get_year(self):
        try:
            return (self.release_date).split('-')[0]
        except:
            return '1990'


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
            release_date = movie_info['release_date']
            vote_count = movie_info['vote_count']
            actors = movie_info['actors']
            m = Movie(id, rank, title, score, regions,
                      types, vote_count, actors, release_date)
            movie_list.append(m)
        return movie_list

    def get_length_list(self):
        length_list = []
        for movie in tqdm.tqdm(self.movie_list):
            response = requests.get(
                f'https://movie.douban.com/subject/{movie.id}/', headers={"User-Agent": "Mozilla/5.0"})
            try:
                length = etree.HTML(response.text).xpath(
                    '//*[@id="info"]/span[@property="v:runtime"]/@content')[0]
                length = int(length)
            except:
                length = 120
            length_list.append(length)
        return length_list


if __name__ == '__main__':
    c = MovieCategoryAcquirer().category_list[0]
    r = RankingCrawler(c, 20)
    # print(r.movie_list)
    print(r.get_length_list())
