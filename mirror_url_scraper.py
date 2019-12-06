import sys
from contextlib import closing
from pathlib import Path
from urllib.request import urlopen

from bs4 import BeautifulSoup

DATA_FOLDER = Path("Mirror URL/")


def main():
    file_to_open = DATA_FOLDER / "official_urls.txt"
    file_to_write = DATA_FOLDER / "good_urls.txt"

    # Making a request for the archilinux mirrors status page
    with closing(urlopen("https://www.archlinux.org/mirrors/status/")) as res:
        # Assigning the parsed page to the soup variable
        soup = BeautifulSoup(res.text, "lxml")

    # Making a new variable called soup_table, that contains the desired table we want to scrape
    soup_table = soup.find("table", {"id": "successful_mirrors"})

    # Assigning all rows in that table to the rows variable
    rows = soup_table.find_all("tr")

    # Making a list that will contain all of the URLS we are scraping
    urls = []

    # Making a for loop that loops over all rows in the table, skipping the first row, since it is the headers of the table
    for row in rows[1:]:
        # Stripping white spaces, and splitting the row so each category will be an item in a list
        row = row.text.strip().split("\n")
        # Row[1] is the Protocol, and row[3] is the Completion %, so we are checking that they both meet the conditions we have
        if row[1] == "https" and row[3] == "100.0%":

            # If the items in the row we are looping over meets the conditions, we are appending row[0] which is the url to the url list
            urls.append(row[0])

    # Output "Done" to the console when script is finished
    print("Done")

    with open(file_to_open, "r") as f:
        lines = f.readlines()
        official_urls = lines[1::2]

    for i, url in enumerate(official_urls):
        url = url.split("= ")[1].rstrip()
        url = url.split("$")
        official_urls[i] = url[0]

    with open(file_to_write, "w") as f:
        for url in urls:
            if url in official_urls:
                f.write(f"{url}$repo/os/$arch\n")


if __name__ == "__main__":
    sys.exit(main())
