import requests
from bs4 import BeautifulSoup
import sqlite3

url="http://books.toscrape.com/"

def scrape_books(url):
	#Make a url request
	request=requests.get(url).text

	#Initialize BS
	soup=BeautifulSoup(request, "html.parser")

	#Extract data
	books=soup.find_all(class_="product_pod")
	all_books=[]
	for book in books:
		all_books.append((
			get_titles(book),
			get_prices(book),
			get_stars(book)
		))
	save_to_db(all_books)

def save_to_db(all_books):
	# connect to DB
	conn=sqlite3.connect("all_books.db")
	# create cursor object
	c=conn.cursor()
	# execute sql
		# create table
	try:
		c.execute('''CREATE TABLE books 
			(title TEXT UNIQUE, price REAL, rating INTEGER)''')
	except sqlite3.OperationalError:
		pass

	# insert bulk data with no duplicates
	c.executemany('''INSERT OR IGNORE INTO books VALUES (?,?,?)''', all_books)

	# commit changes
	conn.commit()
	conn.close()


def get_titles(book):
	return 	book.find("h3").a["title"]

def get_prices(book):
	price=book.find(class_="price_color").text
	price=price.replace("Â£","")
	return float(price)

def get_stars(book):
	star=book.p["class"]
	star=star[1]
	rating={"One":1, "Two":2, "Three":3, "Four":4,"Five":5}
	return rating[star]



scrape_books(url)

#Retrive best books by rating