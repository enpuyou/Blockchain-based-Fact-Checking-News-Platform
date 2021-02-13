"""Access fact checking API"""
# API doc:
# https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims/search
import logging
import requests
from gensim.summarization import summarize
from newspaper import Article

API_KEY = "AIzaSyCr6s761Tq1OpyY5Lky8P3VpNx56qTHXx4"
URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
# claims = "Vaccine is toxic"


def summarize_article(text: str) -> str:
    """Summarize the given article or text into 30 words"""
    summarized = ""
    try:
        summarized = summarize(text, word_count=30)
    except ValueError as err:
        logging.warning(f"Cannot summarize text: {err}")
    except TypeError as err:
        logging.warning(f"Cannot summarize text: {err}")
    return summarized


def retrieve_review(claim):
    """Retrieve reviews of a claim from Google fact checking API"""
    # print(claim)
    params = {"query": claim, "key": API_KEY}
    if claim:
        r = requests.get(url=URL, params=params)
        data = r.json()
        if data == {}:
            print("No review found")
            return "No review found"
        reviews = []
        for review in data["claims"]:
            reviews.append(review["claimReview"][0]["textualRating"])
        # print(reviews)
        return reviews
    else:
        print("There is no claim entered")
        return "There is no claim entered"


def retrieve_article(url):
    """return article dict constructed from article url"""
    article = Article(url)
    article.download()
    article.parse()
    # print(dict(article))
    article_dict = {
        "title": article.title,
        "text": article.text,
        "date": str(article.publish_date)
    }
    # print(article_dict)
    return article_dict


if __name__ == '__main__':
    news_url = "https://www.local10.com/news/local/2021/02/04/florida-supermarket-owner-believes-coronavirus-pandemic-is-a-hoax/"
    news_article = retrieve_article(news_url)
    retrieve_review(news_article["title"])
    retrieve_review("Coronavirus is a hoax")
