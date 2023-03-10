# This is a sample Python script.
from bs4 import BeautifulSoup
from bs4 import Tag
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    global container_fluid
    with open("scratch.html", "r+", encoding="utf-8",) as scratch:
        soup = BeautifulSoup(scratch, "html.parser")
        container_fluid = soup.new_tag("div", class_="container-fluid", role="list")
        container_fluid["aria-owns"] = []
        soup.find(class_="row").insert_before(container_fluid)
        keyListItems = []
        for i in range(1,8):
            nextListItem = soup.find(id="hdc-key-list-" + str(i))
            if nextListItem is not None:
                container_fluid["aria-owns"].append("hdc-key-list-" + str(i))
                if "aria-role" in nextListItem.attrs.keys():
                    del nextListItem["aria-role"]
                nextListItem["role"] = "listitem"
                row = soup.new_tag("div")
                row["class"] = "row"
                container_fluid.append(row)
                image_div = soup.new_tag("div")
                image_div["class"] = "col col-md-3"
                row.append(image_div)
                image = soup.new_tag("img", src="/placeholder_image.jpg", alt="Image goes here")
                image["class"] = "img-fluid"
                image_div.append(image)
                row.append(nextListItem)
                keyListItems.append(nextListItem)
        for nextListItem in keyListItems:
            redundant_row = nextListItem.find(class_="row")
            while redundant_row is not None:
                redundant_row.decompose()
                redundant_row = nextListItem.find(class_="row")
        container_fluid_tag = container_fluid.find_next(class_="container_fluid")
        while container_fluid_tag is not None:
            container_fluid_tag.decompose()
            container_fluid_tag = container_fluid.find_next(class_="container_fluid")
        rows_to_delete = [row for row in soup.find_all(class_="row") if container_fluid not in list(row.parents)]
        for row in rows_to_delete:
            row.decompose()


        print(soup.prettify())
        scratch.seek(0)
        scratch.truncate(0)
        scratch.write(soup.prettify())# Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
