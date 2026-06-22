imagepath = "https://i.simpalsmedia.com/999.md/BoardImages/"
datapath = "https://999.md/"

def normalize(response):
    ads = response["data"]["searchAds"]["ads"]

    result = []

    for ad in ads:

        # цена
        price = "Не указана"
        if ad.get("price") and ad["price"].get("value"):
            price = ad["price"]["value"].get("value", "Не указана")

        # изображения
        image = None
        if ad.get("images") and ad["images"].get("value"):
            images = ad["images"]["value"]

            if isinstance(images, list) and len(images) > 0:
                image = imagepath + images[0]

        # комнаты
        rooms = "Не указано"
        if ad.get("subCategory"):
            rooms = ad["subCategory"]["title"]["translated"]

        result.append({
            "id": ad["id"],
            "title": ad["title"],
            "rooms": rooms,
            "price": price,
            "date": ad["reseted"],
            "link": f"{datapath}{ad['id']}",
            "image": image
        })

    return result