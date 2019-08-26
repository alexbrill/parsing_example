from bs4 import BeautifulSoup
import requests
import csv

def write_csv(data):
    with open('anime.csv', 'w', newline='') as f:
        fieldnames = ["title", "rating", "year"]
        writer = csv.DictWriter(f, fieldnames = fieldnames, delimiter=',',
                            quotechar=' ', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data)


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    r = requests.get(url, headers=headers, timeout=5)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, "lxml")
    nav = soup.find("span", class_ = "navigation")
    total_pages = nav.find_all("a")[-1].text.strip()
    return int(total_pages)



def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    content = soup.find("div", id = "dle-content")

    titles = []
    tits = content.find_all("a", class_ = "mov-t")
    for tit in tits:
        try:
            titles.append(tit.find("h2").text.strip())
        except:
            titles.append("")

    ratings = []
    rats = content.find_all("div", class_="rate_box")
    for rat in rats:
        try:
            ratings.append(rat.find("b").text.strip())
        except:
            ratings.append("")

    years = []
    yrs = content.find_all("div", class_="movie-text")
    for yr in yrs:
        try:
            years.append(yr.find_all("li")[0].find("div", class_ = "ml-desc").text.strip())
        except:
            years.append("")

    data = []
    keys = ("title", "rating", "year")
    for i in range(len(titles)):
        data.append(dict(zip(keys, (titles[i], ratings[i], years[i]))))

    write_csv(data)


URL = "https://animedub.ru/"
PAGES = "page/"

#get the first page
#get the amount of pages
#extract name, rating and year
#make csv file

#proxy, multi and so on


def main():
    main_page = get_html(URL)
    total_pages = get_total_pages(main_page)
    data = []

    for i in range(2, 3):
        url = URL + PAGES + str(i)
        html = get_html(url)
        get_data(html)

if __name__ == "__main__":
    main()