from shop.models import Brand, Generic, Medicine, Place
import random

brands = {
    "Beximco Pharma",
    "ACI Limited",
    "The ACME Laboratories Ltd",
    "Beacon Pharmaceuticals",
    "Incepta Pharmaceuticals",
    "Renata Limited",
    "Square Pharmaceuticals",
    "Orion Pharma"
}

brand_id = []

generics = {
    "Aceclofenac",
    "Aciclovir",
    "Adapalene",
    "Albendazole",
    "Allylestrenol",
    "Ambroxol",
    "Aspirin"
}

generic_id = []

places = {
    'A1',
    'A2',
    'B1',
    'B2'
}

place_id = []

medecines = [
    ["Flexi", 10, 12, "tablet", 10],
    ["Napa", 10, 12, "tablet", 10],
    ["Tylace", 10, 12, "tablet", 10],
    ["Virux", 10, 12, "tablet", 10],
    ["Virux Tablet", 10, 12, "tablet", 10],
    ["Virux HR", 10, 12, "tablet", 10],
    ["Fona", 10, 12, "tablet", 10],
    ["Almex", 10, 12, "tablet", 10],
    ["Esloric", 10, 12, "tablet", 10],
    ["Geston", 10, 12, "tablet", 10],
    ["Entacyd", 10, 12, "tablet", 10],
    ["Ambrisan 5", 10, 12, "tablet", 10],
    ["Ambrox", 10, 12, "tablet", 10],
    ["Tryptin", 10, 12, "tablet", 10],
    ["Apsol", 10, 12, "tablet", 10]
]

def run():
    print("------------ Load user data -------------")
    Brand.objects.all().delete()
    Generic.objects.all().delete()
    Place.objects.all().delete()
    Medicine.objects.all().delete()
    # Add user
    for i in brands:
        brand = Brand.objects.create(name=i)
        brand_id.append(brand.id)

    # Add Generic
    for i in generics:
        generic = Generic.objects.create(name=i)
        generic_id.append(generic.id)
    
    # Add place
    for i in places:
        place = Place.objects.create(name=i)
        place_id.append(place.id)

    for i in medecines:
        name = i[0]
        buy_price = i[1]
        sell_price = i[2]
        type = i[3]
        quantity = i[4]
        generic = random.randint(generic_id[0],generic_id[-1])
        brand = random.randint(brand_id[0],brand_id[-1])
        place = random.randint(place_id[0],place_id[-1])
        Medicine.objects.create(name=name, buy_price=buy_price, sell_price=sell_price, type=type, quantity=quantity, generic_id=generic, brand_id=brand, place_id=place)

    print("------------ End user data -------------")
    return