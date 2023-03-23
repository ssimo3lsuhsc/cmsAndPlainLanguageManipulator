from bs4 import BeautifulSoup

with open("scratch.html") as scratch:
    soup = BeautifulSoup(scratch, "html.parser")
    #Do stuff here

    with open("output.html", "w") as output:
        output.truncate(0)
        output.write(soup.prettify())