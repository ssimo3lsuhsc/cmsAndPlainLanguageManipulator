from typing import Union, Any

from bs4 import BeautifulSoup, Tag
import os.path
import os
import imageio.v3 as iio
from skimage.transform import resize, rescale
import numpy as np
import numpy.typing as npt
import re
import shutil
import json

space_subber = re.compile(r"\s")

def copyHtml():
    html_matcher = re.compile(r"<MAINCONTENT>(?P<html>.*?)</MAINCONTENT>", re.I | re.DOTALL)
    filename_matcher = re.compile(r"plain_lang_(?P<iam>.*).aspx$")


    for file in os.listdir(r"W:\Development\dev.www.hdc.lsuhsc.edu\root"):
        match = filename_matcher.search(file)
        if match is not None:
            xml = ""
            with open(r"W:\Development\dev.www.hdc.lsuhsc.edu\root\xml\plain_lang_" + match.group("iam") + ".xml", encoding="utf-8") as xmlFile:
                xml = xmlFile.read()

            html_match = html_matcher.search(xml)
            if html_match is not None:
                with open(os.path.join("html_source", match.group("iam") + ".html"), "w", encoding="utf-8") as outputPath:
                    outputPath.truncate(0)
                    outputPath.write(html_match.group("html").strip())

def copyImage(paths: list[Union[str, os.PathLike]], resized: npt.NDArray[np.uint8]):
    iio.imwrite(os.path.join(*paths), resized)
def copyImages():
    space_subber = re.compile(r"\s")
    navPagesRoot = r"C:\Users\ssimo3\OneDrive - LSUHSC\Outreach OneDrive\01 HDC\Web\Navigation pages"
    startingLevel = navPagesRoot.count(os.sep)
    starting_paths = ["images", "plain_lang"]
    for root, dirs, files in os.walk(navPagesRoot):
        currentLevel = root.count(os.sep)
        if currentLevel == startingLevel + 1:
            for file in files:
                if os.path.splitext(file)[1] in [".jpg", ".png"]:
                    imagebytes = iio.imread(os.path.join(navPagesRoot, root, file))
                    width, height, aspect_ratio = imagebytes.shape
                    resized = (rescale(imagebytes, min(695, width)/width) * 255).astype(np.uint8)
                    paths = starting_paths + ["heroes", space_subber.sub("_", file)]
                    copyImage(paths, resized)
                    paths.insert(0, r"W:\Development\dev.www.hdc.lsuhsc.edu\root")
                    copyImage(paths, resized)
        else:
            for file in files:
                if os.path.splitext(file)[1] in [".jpg", ".png"]:
                    imagebytes = iio.imread(os.path.join(navPagesRoot, root, file))
                    resized = (resize(imagebytes, (160,160)) * 255).astype(np.uint8)
                    paths = starting_paths + ["icons", space_subber.sub("_", file)]
                    copyImage(paths, resized)
                    paths.insert(0, r"W:\Development\dev.www.hdc.lsuhsc.edu\root")
                    copyImage(paths, resized)
                    pass
def add_about_us_icon(src: Union[str, os.PathLike], dst: Union[str, os.PathLike]):
    image = iio.imread(src)
    resized = (resize(image, (160, 160)) * 255).astype(np.uint8)
    iio.imwrite(dst, resized)
    pass

def manipulate(filename: str):
    with open(os.path.join("html_source", filename)) as scratch:
        soup = BeautifulSoup(scratch, "html.parser")
        #Do stuff here

        with open(os.path.join("html_output", filename), "w") as output:
            output.truncate(0)
            output.write(str(soup))

def list_to_grid(classes_on_containers: list[str] = None, classes_on_rows: list[str] = None):
    if classes_on_containers is None:
        classes_on_containers = []
    if classes_on_rows is None:
        classes_on_rows = []
    for file in os.listdir("html_source"):
        source_soup = BeautifulSoup(open(os.path.join("html_source", file), encoding="utf-8"), "html.parser")
        unstyled_lists = [_list for _list in source_soup("ul", class_="list-unstyled") if isinstance(_list, Tag)]
        for _list in unstyled_lists:
            _list.name = "div"
            _list["class"].remove("list-unstyled")
            items = [item for item in _list("li", recursive=False) if isinstance(item, Tag)]
            for item in items:
                item.name = "div"
        for container in [container for container in source_soup(class_="container-fluid") if isinstance(container, Tag)]:
            container["role"] = "grid"
            for container_class in classes_on_containers:
                if container_class not in container["class"]:
                    container["class"].append(container_class)
        for row in [row for row in source_soup(class_="row") if isinstance(row, Tag)]:
            row["role"] = "row"
            for row_class in classes_on_rows:
                if row_class not in row["class"]:
                    row["class"].append(row_class)
            for col in [col for col in row(True, recursive=False) if isinstance(col, Tag)]:
                col["role"] = "gridcell"
                term = col.find(role="term")
                if term is not None and isinstance(term, Tag):
                    term.name = "h3"
                    del term["role"]
                    definitions = [p for p in term.find_next_siblings(role="definition") if isinstance(p, Tag)]
                    for definition in definitions:
                        del definition["role"]
                        if "aria-labelledby" in definition.attrs.keys():
                            del definition["aria-labelledby"]
                elif col.find("img", class_="container-fluid") is None and col.find("h3") is None:
                    if "class" not in col.attrs.keys():
                        col["class"] = ["align-self-center"]
                    elif "align-self-center" not in col["class"]:
                        col["class"].append("align-self-center")
        with open(os.path.join("html_output", file), "w", encoding="utf-8") as output_stream:
            output_stream.truncate(0)
            output_stream.write(str(source_soup))


def write_image_alt_to_json_init():
    alt_dict: dict[str, str] = {}
    for root, dirs, images in os.walk("images"):
        for image in images:
            alt_dict[os.path.normpath('/' + os.path.join(root, image)).replace("\\", "/")] = ""
    for file in os.listdir("html_output"):
        soup = BeautifulSoup(open(os.path.join("html_output", file), "html.parser"))
        for image in soup("img"):
            if image["alt"] != "":
                alt_dict[image["src"]] = image["alt"]
    with open("image_alts.json", "w", encoding="utf-8") as alts_json:
        alts_json.truncate(0)
        alts_json.write(json.dumps(alt_dict, indent=5))


if __name__ == "__main__":
    write_image_alt_to_json_init()