import psycopg2
import feedparser
import logging

from psycopg2 import OperationalError
from bs4 import BeautifulSoup

logging.basicConfig(filename='sample.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

hostname = 'localhost'
username = 'gayathri'
database = 'testdb'
password = 'gayu123'


def connect_db():
    """
    Function to connect to the postgres db.
    :return: psycopg2 connection Object
    """
    try:
        logging.info("Trying to connect to db...")
        conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        logging.info("Connected to database successfully")
        return conn
    except OperationalError:
        logging.error("Database Connection Error")
        exit(1)


feed = raw_input("enter an rss feed :")


def clean_html(text):
    """
    Function to remove html tags from text.
    :param text: text to process
    :return: Clean text
    """
    return BeautifulSoup(text, 'html.parser').get_text()


def process_feed(feed):
    """
    Function to process each feed
    :param feed: Feed URL to process
    :return: A dictionary of articles
    """
    print("Processing %s" % feed)
    logging.debug("Executing process feed function...")
    parsed_feed = feedparser.parse(feed)
    articles = {}
    for item in parsed_feed.entries:
        article = {
            "link": item.link,
            "title": clean_html(item.title),
            "description": clean_html(item.description)
        }
        articles[article["link"]] = article
    return articles


def insert_articles(conn, articles):
    """
    :param conn: Psycopg2 connecting object
    :param articles: Articles in the form of dictionary.
    :return: Return True, if insertion was successful.
    """

    logging.info("Inserting to database..")
    cursor = conn.cursor()
    insert_article_sql = "INSERT INTO article(title, link, description) values(%s, %s, %s)"
    for link, article in articles.iteritems():
        print article
        cursor.execute(insert_article_sql, (article["title"], article["link"], article["description"]))
    conn.commit()


def close_connection(conn):
    conn.close()
    logging.info("Feed parsing success")


def main():
    """
    Main function
    """
    conn = connect_db()
    articles = {}
    try:
        articles.update(process_feed(feed))
    except TypeError:
        logging.error("Type Error")
    insert_articles(conn, articles)
    close_connection(conn)


if __name__ == "__main__":
    main()
