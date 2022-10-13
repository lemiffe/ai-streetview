from PIL import Image
import glob
import os
import sys
import re
import glob

path = os.path.dirname(os.path.abspath(__file__))
img_path_wildcard = os.path.join(path, "..", "public", "game", "*.png")
img_paths = glob.glob(img_path_wildcard)

if len(img_paths) == 0:
    print("Nothing to convert")
    sys.exit()

for img_path in img_paths:
    print("Converting", img_path)
    img = Image.open(img_path)
    img = img.convert('RGB')
    img.save(re.sub(r'\.png$', '.jpg', img_path))
    print("Deleting", img_path)
    if os.path.exists(img_path):
        os.remove(img_path)
    else:
        print(img_path, "does not exist")

game_file = os.path.join(path, "..", "src", "mapset.js")
print("Replacing .png with .jpg in", game_file)
fin = open(game_file, "rt")
data = fin.read()
data = data.replace('.png', '.jpg')
fin.close()
fin = open(game_file, "wt")
fin.write(data)
fin.close()
