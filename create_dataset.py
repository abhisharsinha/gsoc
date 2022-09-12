import json
import pandas as pd
from tqdm import tqdm


def get_art_objects():
    art_objects = []
    with open("artworks-api-response.jsonl", "r") as fp:
        for line in tqdm(fp.readlines()):
            try:
                art_obj = json.loads(line)
            # Only considering artworks with images
            if "data" in art_obj.keys() and "image_id" in art_obj["data"].keys():
                art_objects.append(art_obj)
    return art_objects


if __name__ == "__main__":
    art_objects = get_art_objects()
    print(len(art_objects))
    image_ids = []
    alt_texts = []
    art_ids = []
    artists = []
    titles = []
    for art in tqdm(art_objects):
        alttext = None
        artid = None
        imageid = None
        artist = None
        title = None
        try:
            # This will cause exception if no alt_text
            alttext = art["data"]["thumbnail"]["alt_text"]
            artid = art["data"]["id"]
            imageid = art["data"]["image_id"]
            title = art["data"]["title"]
            artist = art["data"]["artist_title"]
        except:
            # If any field is missing and causes exception
            # the field will be set to None in dataframe
            pass
        alt_texts.append(alttext)
        art_ids.append(artid)
        image_ids.append(imageid)
        artists.append(artist)
        titles.append(title)
    img_df = pd.DataFrame({"art_id": art_ids, "image_id": image_ids,
        "alt_text": alt_texts, "title": titles, "artist": artists})
    
    # Some descriptions were corrupted while scraping
    desc_df = pd.read_csv("descriptions.csv")
    full_df = img_df.merge(desc_df, on="art_id", how="outer")
    print("Shape of dataframe", full_df.shape)
    print("", full_df.count())
    full_df.to_csv("artworks_dataset.csv", index=False)
