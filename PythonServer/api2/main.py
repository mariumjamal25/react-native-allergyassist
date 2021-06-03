from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"Greetings": "Welcome to blah blah"}

class Scan(BaseModel):
    image: str

@app.post("/sendData")
async def scan_Image(Data:Scan):
    import json
    import cv2
    import pytesseract
    import re

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    imagestr = Data.image
    # test = "C:\Users\Abc\Downloads\test8.jpeg"
    image = cv2.imread(r"C:\Users\Abc\Downloads\test8.jpeg")
    print(image)
    text = pytesseract.image_to_string(image) 

    Gluten = ['malt', 'malt flavor', 'malt extract', 'malt vinegar', 'brewer’s yeast', 'wheat', 'barley', 'rye', 'dextrin (wheat)', 
            'wheat starch', 'malted barley flour', 'malted milk', 'malt syrup', 'malt flavoring', 'wheat starch', 'bran', 'bread crumbs', 'bulgur', 'cereal extract', 'couscous', 'cracker meal', 'durum', 'einkorn', 'emmer', 
            'farina', 'flour', 'matzoh', 'matzoh meal', 'pasta', 'seitan', 'semolina', 'spelt', 'gluten', 'malt', 'sprouted', 
            'modified food starch', 'soy sauce', 'surimi', 'vegetable starch', 'purpose flour', 'wheat flour', 'farro', 'flour',
            'kamut', 'maida', 'triticale', 'triticum', 'kamut', 'khorasan wheat', 'malt', 'malt extract', 'matzo', 'matzo meal',
            'matzoh', 'matzah', 'matza', 'noodles', 'wheat berries', 'wheat bran', 'whole wheat bread', 'whole wheat flour', 
            'wheat germ', 'wheat germ oil', 'wheat protein isolate', 'wheat starch', 'wheat sprouts', 'sprouted wheat', 
            'wheat grass']
    Lactose = ['dry milk solids', 'lactose', 'lactose monohydrate', 'milk']
    Nuts = ['peanuts', 'peanut grits', 'treenuts', 'cashews', 'walnuts', 'almonds', 'pecans', 'pistachios', 'brazil nuts', 'hazelnuts', 
            'macadamias', 'almonds', 'mixed nuts', 'ground nuts', 'praline', 'baci', 'hazelnuts', 'satay sauce', 'marzipan', 
            'peanut flour', 'chestnuts', 'peanut butter', 'peanut paste', 'cashew nut paste', 'nutella spread', 'peanut oil']
    Shellfish = ['barnacle', 'crab', 'crawfish', 'crawdad', 'crayfish', 'ecrevisse', 'krill', 'lobster', 'langouste', 'langoustine',
                'moreton bay bugs', 'scampi', 'tomalley', 'prawns', 'shrimp', 'crevette', 'bouillabaisse', 'cuttlefish ink', 
                'glucosamine', 'fish stock', 'seafood flavoring', 'crab extract', 'clam extract', 'fish sauce', 'surimi',
                'abalone', 'clams', 'cherrystone', 'geoduck', 'littleneck', 'pismo', 'quahog', 'cockle', 'limpet', 'lapas',
                'opihi', 'mussels', 'octopus', 'oysters', 'periwinkle', 'sea cucumber', 'sea urchin', 'scallops', 'snails', 
                'escargot', 'squid', 'calamari', 'whelk', 'turban shell']
    Fish = ['anchovies', 'bass', 'catfish', 'cod', 'flounder', 'grouper', 'haddock', 'hake', 'halibut', 'herring', 'mahi mahi', 
            'perch', 'pike', 'pollock', 'salmon', 'scrod', 'swordfish', 'sole', 'snapper', 'tilapia', 'trout', 'tuna', 
            'caesar salad dressing', 'worcestershire sauce', 'ceviche', 'caviar', 'cioppino', 'fish stew', 'nam pla', 
            'thai fish sauce', 'bouillabaisse', 'fumet', 'fish stock', 'surimi', 'pissaladière', 'omega-3', 'caponata', 
            'eggplant relish']
    Wheat = ['bran', 'bread crumbs', 'bulgur', 'cereal extract', 'couscous', 'cracker meal', 'durum', 'einkorn', 'emmer', 
            'farina', 'flour', 'matzoh', 'matzoh meal', 'pasta', 'seitan', 'semolina', 'spelt', 'gluten', 'malt', 'sprouted', 
            'modified food starch', 'soy sauce', 'surimi', 'vegetable starch', 'purpose flour', 'wheat flour', 'farro', 'flour',
            'kamut', 'maida', 'triticale', 'triticum', 'kamut', 'khorasan wheat', 'malt', 'malt extract', 'matzo', 'matzo meal',
            'matzoh', 'matzah', 'matza', 'noodles', 'wheat berries', 'wheat bran', 'whole wheat bread', 'whole wheat flour', 
            'wheat germ', 'wheat germ oil', 'wheat protein isolate', 'wheat starch', 'wheat sprouts', 'sprouted wheat', 
            'wheat grass']

    text = text.lower()
    index = text.find("ingredient")
    text = text[index:len(text)]
    res = re.split('[,:&\n]', text)

    str1=""
    str2=""
    str3=""
    str4=""
    str5=""
    str6=""


    count = 0
    for j in res:
        word = j.strip()
        if(len(word)<50):
            if(count<40):
                if(len(word)>1):
                    gluten = any(word in string for string in Gluten)
                    if(gluten==True):
                        str1 = "Gluten,"
                    lactose = any(word in string for string in Lactose)
                    if(lactose==True):
                        str2 = "Lactose,"
                    nuts = any(word in string for string in Nuts)
                    if(nuts==True):
                        str3= "Nuts,"
                    shellfish = any(word in string for string in Shellfish)
                    if(shellfish==True):
                        str4 = "Shellfish,"
                    fish = any(word in string for string in Fish)
                    if(fish==True):
                        str5 = "Fish,"
                    wheat = any(word in string for string in Wheat)
                    if(wheat==True):
                        str6 = "Wheat,"
                    if(gluten==False and lactose==False and nuts==False and shellfish==False and fish==False and wheat==False):
                        count+=1

    message = str1 + "" + str2 + "" + str3 + "" + str4 + "" + str5 + "" + str6 
    if(message.isspace()):
        message = "No Allergies"
    
    print(message)
    
    return json.dumps(message)
