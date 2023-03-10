# This is a sample Python script.
from bs4 import BeautifulSoup
from bs4 import Tag
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def is_ul(tag: Tag) -> bool:
    return tag.name == "ul" or ("aria-role" in tag.attrs.keys() and tag["aria-role"] == "list")


def is_li(tag: Tag) -> bool:
    return tag.name == "li" or ("aria-role" in tag.attrs.keys() and tag["aria-role"] == "listitem")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    with open("scratch.html", "r+", encoding="utf-8",) as scratch:
        soup = BeautifulSoup(scratch, "html.parser")
        ul = soup.find(is_ul)
        if ul is not None:
            ul.name = "div"
            ul["class"] = "container-fluid"
            ul["aria-role"] = "list"
            ul["aria-owns"] = []
        li = soup.find(is_ul)
        index = 1
        while li is not None:
            li.name = "div"
            li["aria-role"] = "listitem"
            li["class"] = "col"
            li["id"] = "hdc-key-list-" + str(index)
            index += 1
            ul["owns"].append(li["id"])
            imagediv = soup.new_tag("div")
            imagediv["class"] = "col col-md-3"
            image = soup.new_tag("img")
            image["class"] = "img-fluid"
            image["alt"] = "Image goes here"
            image["src"] = "/img_placeholder.jpg"
            imagediv.append(image)
            rowdiv = soup.new_tag("div")
            rowdiv["class"] = "row"
            rowdiv.append(imagediv)
            li.insert_before(rowdiv)
            rowdiv.append(li)
            li = li.find_next(is_li)

        print(soup.prettify())
        scratch.seek(0)
        scratch.truncate(0)
        scratch.write(soup.prettify())# Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
