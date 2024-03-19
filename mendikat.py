import json
import glob
import gpxpy
import unicodedata

"""
def generate_name_variations(cim_fet):
    name_variations = [cim_fet]
    if "del" in cim_fet:
        name_variations.append(cim_fet.replace("del", "de"))
    if "de " in cim_fet:
        name_variations.append(cim_fet.replace("de ", ""))
    if "l'" in cim_fet:
        name_variations.append(cim_fet.replace("l'", "l' "))
    if "d'" in cim_fet:
        name_variations.append(cim_fet.replace("d'", "d' "))
    if "pic" in cim_fet:
        name_variations.append(cim_fet.replace("pic", "tuc"))

    return [normalize(text) for text in name_variations]
"""


def normalize(text):
    text = remove_text_between_parenthesis(text)
    text = unicodedata.normalize('NFKD', text)
    text = text.replace(u"c\u0327", "ç")
    normalized = text.strip()
    return normalized


def remove_text_between_parenthesis(text):
    start = text.find("(")
    end = text.find(")")
    if start != -1 and end != -1:
        return text[0:start]
    return text


def load_fets():
    fets = []
    with open("data/mendikat/fets.txt") as fets_fd:
        for line in fets_fd.readlines():
            fets.append(normalize(line))
    return fets


def load_mendikat_cims():
    mendikat_cims_file = glob.glob('raw-data/mendikat-*.gpx')
    cims = []
    for file in mendikat_cims_file:
        with open(file, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            for wpt in gpx.waypoints:
                name = normalize(wpt.name)
                possible_names = [name]
                if wpt.comment:
                    for possible in wpt.comment.split(","):
                        possible_names.append(normalize(possible))

                cim = {
                    "name": name,
                    "lat": wpt.latitude,
                    "lng": wpt.longitude,
                    "area": "",  # TODO: read from metadata
                    "link": wpt.link,
                    "height": wpt.elevation,
                    "possible_names": possible_names,
                    "fet": False
                }
                cims.append(cim)

    return cims


def mendikat_cims_fets(cims, fets):
    for fet in fets:
        found = False
        for cim in cims:
            for cim_name in cim["possible_names"]:
                cim_name_lower = cim_name.lower()
                fet_lower = fet.lower()
                if cim_name_lower == fet_lower or fet_lower in cim_name_lower:
                    cim["fet"] = True
                    found = True
                    break
        if not found:
            raise ValueError(fet + " not found!")

    return fets


if __name__ == '__main__':
    cims = load_mendikat_cims()
    fets = load_fets()
    mendikat_cims_fets(cims, fets)
    with open("data/mendikat/cims.json", 'w') as cims_fd:
        json.dump(cims, cims_fd, indent=4)
