from requests import get
from bs4 import BeautifulSoup
import csv

books_rank = []
books_title = []
books_author = []
books_url = []
books_price = []
books_average_rating = []
books_number_rating = []


def write(file):
    class excel_semicolon(csv.excel):
        delimiter = ';'
    with open(file, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'URL', 'Author', 'Price',
                      'Number of Ratings', 'Average Rating']
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, dialect=excel_semicolon)
        writer.writeheader()
        for i in range(len(books_rank)):
            writer.writerow({'Name': books_title[i], 'URL': books_url[i], 'Author': books_author[i], 'Price': books_price[i],
                             'Number of Ratings': books_number_rating[i], 'Average Rating': books_average_rating[i]})


def solve(url):
    domain = 'https://www.amazon.in'
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    book_containers = soup.find_all('div', class_='zg_itemImmersion')

    def getPropertyText(element, class_name):
        prop = book.find(element, class_name)
        if prop is None or (class_name == "a-icon-alt" and prop.text.strip() == "Prime"):
            return "Not available"
        else:
            return prop.text.strip()

    def getPropertyHref(element, class_name):
        prop = book.find(element, class_name)
        return domain + prop['href'].strip()

    for book in book_containers:
        books_rank.append(getPropertyText('span', 'zg_rankNumber'))
        books_title.append(getPropertyText(
            'div', 'p13n-sc-truncate p13n-sc-line-clamp-1'))
        books_author.append(getPropertyText('div', 'a-row a-size-small'))
        books_url.append(getPropertyHref('a', 'a-link-normal'))
        books_price.append(u"\u20B9" + getPropertyText('span', 'p13n-sc-price'))
        books_average_rating.append(getPropertyText('span', 'a-icon-alt'))
        books_number_rating.append(getPropertyText(
            'a', 'a-size-small a-link-normal'))


solve('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg=1')
solve('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=2')
solve('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_3?ie=UTF8&pg=3')
solve('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_4?ie=UTF8&pg=4')
solve('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_5?ie=UTF8&pg=5')
write('./output/in_book.csv')
