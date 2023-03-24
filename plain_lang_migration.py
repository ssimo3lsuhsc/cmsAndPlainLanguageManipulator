import shutil
import os
import os.path as ospath
import posixpath
from bs4 import BeautifulSoup
import requests
import re

dev_root = r'W:\Development\dev.www.hdc.lsuhsc.edu\root'
prod_root = r'W:\Production\www.hdc.lsuhsc.edu'

for file in [file for file in os.listdir(dev_root) if re.fullmatch(r"plain_lang_.*\.aspx", file)]:
    shutil.copy2(ospath.join(dev_root, file), prod_root)
    xml_file = re.sub("\.aspx$", ".xml", file)
    shutil.copy2(ospath.join(dev_root, "LSUCMS", xml_file), ospath.join(prod_root, "LSUCMS"))
    soup = BeautifulSoup(requests.get("https://dev.www.hdc.lsuhsc.edu/" + file).text)
    for image in [image for image in soup("img") if str(image["src"]).startswith("/images/")]:
        image_filename = posixpath.basename(image["src"])
        shutil.copy(os.path.join(dev_root, "images", image_filename), os.path.join(prod_root, "images"))

