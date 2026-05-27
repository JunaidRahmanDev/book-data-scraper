Book Data Scraper
I built this to practice web scraping. Before this I only wrote small scripts for assignments. This was the first thing that actually felt like a real project.

It goes to books.toscrape.com and collects info on all 1000 books across 50 pages. Then it writes everything into a CSV file.

What it extracts
Full book title (the one in the title attribute, not the truncated version)

Price

Star rating (converted from words to numbers)

Whether the book is in stock or not

How to run it
Clone the repo and set up a virtual environment first.

git clone https://github.com/JunaidRahmanDev/book-data-scraper.git
cd book-data-scraper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Then run it.

python scraper.py

Add --pages 5 to scrape fewer pages or --output myfile.csv to change the filename.

Sample output
Book Scraper
Pages: 3 | Output: books_20260501_143022.csv
Scraping page 1/3
Found 20 books. Total: 20
Scraping page 2/3
Found 20 books. Total: 40
Scraping page 3/3
Found 20 books. Total: 60
Saved 60 books to: books_20260501_143022.csv

What I used
python, requests, beautifulsoup4, csv, argparse

What I learned
How to break a project into functions that each do one thing. How to handle errors so the whole script doesn't crash. How to use Git properly and push to GitHub.

If something breaks, open an issue. I'm still learning but I'll try to fix it.
