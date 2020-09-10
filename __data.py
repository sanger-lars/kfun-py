import os, json, re

def read_config():
    """Henter config.txt og returnerer obj med sti:, ignore_dir:, ignore_ext: og font_size:"""
    #try:
    with open('config.txt') as json_file:
        data = json.load(json_file)
    return data
    #except: return "null"


def read_data_json(filnavn='data.json'):
    """Henter data.json og returnerer """
    try:
        with open(filnavn, "r") as json_file:
            data = json.load(json_file)
        return data
    except: return "null"  


def gem(startpath, datafilnavn='data.json'):
    def filter(files, cfg):
	    return [val for val in files
		    #if not val[-3:].lower() in ["mp3","wav", "wma", "m4a","jpg","zip", "txt", "doc","lng","mcg","nfo","csv","old"]
		    if re.search("\."+cfg['use_ext'], val,re.IGNORECASE)
            ]

    cfg = read_config()
    matches = {}
    matches['sange'] = []
    for path2, folders, files in os.walk(startpath):
        if path2.split("\\")[-1] in cfg['ignore_dir']:
            continue
        for filename in filter(files, cfg):
            matches['sange'].append({
                'name': filename,
                'link': path2.split(startpath)[1]})
                
    with open(datafilnavn, 'w') as outfile:
        json.dump(matches, outfile, ensure_ascii=False)
    
    print(f"{len(matches['sange'])} sange startende fra {startpath} er nu gemt i {datafilnavn}.")
    

def find_sang(arr, tekst):
    """Finder tekst i array og returnerer dictionary med liste: og links:
    Arguments:
        arr - array med data fra read_data()
        tekst - Tekst der skal søges efter
    """
    liste = []
    links = []
    regx = re.compile(tekst, re.IGNORECASE)
    for index, sang in enumerate(arr['sange']):
        if regx.findall(sang['name']) != []:
            liste.append(sang['name'])
            links.append(sang['link'])
    return {'liste': liste, 'links': links}
