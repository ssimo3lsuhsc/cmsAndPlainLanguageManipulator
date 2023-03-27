from typing import Union, Any

from bs4 import BeautifulSoup
import os.path
import os
import imageio.v3 as iio
from skimage.transform import resize, rescale
import numpy as np
import numpy.typing as npt
import re
import shutil

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






if __name__ == "__main__":
    dst = r"images\plain_lang\icons\About_Us_page"
    shutil.copytree(r"C:\Users\ssimo3\OneDrive - LSUHSC\Outreach OneDrive\01 HDC\Web\Icons\About Us page", dst, copy_function=add_about_us_icon)
    renamable_directories = [(root, dirs + files) for root, dirs, files in os.walk(dst, topdown=False)]
    for root, nodes in renamable_directories:
        for node in nodes:
            os.rename(os.path.join(root, node), os.path.abspath(os.path.join(root, space_subber.sub("_", node))))
