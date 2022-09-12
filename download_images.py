import os
import pandas as pd
from tqdm import tqdm
import time

art_df = pd.read_csv("artworks_dataset.csv")
art_df.dropna(inplace=True)

downloaded_filenames = set(os.listdir("artic-images-resized/"))
image_filenames = list(art_df["image_id"])
print(len(downloaded_filenames))

counts = 0
for image_id in tqdm(image_filenames):
    counts += 1
    # Continous request start causing 403 error
    # so adding a sleep time in between
    if counts % 100 == 0:
        time.sleep(30)
    if "{}.jpg" not in downloaded_filenames:
        command = "wget -O artic-images/{}.jpg https://www.artic.edu/iiif/2/{}/full/843,/0/default.jpg".format(image_id, image_id)
        res = os.system(command)
