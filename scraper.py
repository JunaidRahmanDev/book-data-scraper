import argparse
from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import csv

BASE_URL= "https://books.toscrape.com/catalogue/"
FIRST_PAGE= "https://books.toscrape.com/catalogue/page-1.html"
HEADERS= {"User-Agent": "Mozilla/5.0 (BookScraper/1.0)"}
RATING_MAP={"One":1,"Two":2,"Three":3,"Four":4,"Five":5}

def fetch_page(url):
    try:
        response=requests.get(url,headers=HEADERS,timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text,"html.parser")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timed out:{url}")
        return None
    except requests.exceptions.HTTPError as err:
        print(f"[ERROR] Website error:{err}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] No internet. Check your connection")
        return None

def get_books_from_page(soup):
    books=[]
    all_book_cards=soup.find_all("article",class_="product_pod")

    for card in all_book_cards:
        title_tag=card.find("h3").find("a")
        title=title_tag["title"] if title_tag else "Unknown"

        price_tag=card.find("p",class_="price_color")
        price=price_tag.text.strip().replace("Â","").strip() if price_tag else "N/A"

        rating_tag=card.find("p",class_="star-rating")
        if rating_tag:
            word=rating_tag["class"][1]
            rating=RATING_MAP.get(word,0)
        else:
            rating=0

        avail_tag=card.find("p",class_="instock")
        availability="In stock" if avail_tag else "Not available"

        books.append({"title":title,"price": price,
                       "rating": rating, "availability": availability})
    return books

def get_next_page_url(soup):
    next_btn=soup.find("li",class_="next")
    if next_btn:
        filename=next_btn.find("a")["href"]
        return BASE_URL + filename
    return None

def save_to_csv(books,output_file):
   columns=["title","price","rating","availability"]
   with open(output_file,"w",newline="",encoding="utf-8")as f:
       writer=csv.DictWriter(f,fieldnames=columns)
       writer.writeheader()
       writer.writerows(books)
   print(f"\nSaved {len(books)} books to:{output_file}")

def main():
    parser=argparse.ArgumentParser(description="Scrape books.toscrape.com")
    parser.add_argument("--pages",type=int,default=50,help="Pages to scrape (default: all 50)")
    parser.add_argument("--output",type=str,default=f"books_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",help="Output CSV filename")
    args=parser.parse_args()

    max_pages=min(args.pages,50)
    print(f"\nBook Scraper")
    print(f"Pages:{max_pages} | Output:{args.output}\n")

    all_books=[]
    current_url=FIRST_PAGE
    page_num=0

    while current_url and page_num<max_pages:
        page_num+=1
        print(f"Scraping page {page_num}/{max_pages}")

        soup=fetch_page(current_url)
        if soup is None:
            print(f"Skipping page {page_num}")
            break

        page_books=get_books_from_page(soup)
        all_books.extend(page_books)
        print(f"Found {len(page_books)} books. Total:{len(all_books)}")

        current_url=get_next_page_url(soup)
        if current_url:
            time.sleep(0.5)

    if all_books:
        save_to_csv(all_books,args.output)
    else:
      print("No books scraped. Check errors above.")

if __name__ == "__main__":
      main()


