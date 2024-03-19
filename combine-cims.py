import json
from bs4 import BeautifulSoup
import glob
import gpxpy
import unicodedata


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


def normalize(text):
    text = remove_text_between_parenthesis(text)
    text = unicodedata.normalize('NFKD', text)
    text = text.replace(u"c\u0327", "ç")
    return text.strip()


def remove_text_between_parenthesis(text):
    start = text.find("(")
    end = text.find(")")
    if start != -1 and end != -1:
        return text[0:start]
    return text


def extract_url_from_html_link(html_link):
    soup = BeautifulSoup(html_link, features='html.parser')
    return soup.findAll('a')[0].get("href")


def load_fets():
    fets = []
    with open("data/fets.txt") as fets_fd:
        for line in fets_fd.readlines():
            fets.append(line.strip())
    return fets


def load_cims_info():
    cims_by_link = {}
    with open("raw-data/cims-info.json") as cims_fd:
        cims_raw = json.load(cims_fd)["data"]
        for cim_raw in cims_raw:
            cims_by_link[extract_url_from_html_link(cim_raw[0])] = {
                "area": cim_raw[1], "height": cim_raw[2]}
    return cims_by_link


def load_cims_extra():
    cims_by_link = {}
    with open("raw-data/cims-extra.json") as cims_fd:
        cims_extra = json.load(cims_fd)
        for cim in cims_extra:
            cims_by_link[cim["url"]] = {
                "name": cim["nombre"],
                "lat": cim["lat"],
                "lng": cim["lang"]
            }
    return cims_by_link


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


def cent_cims_fets(cims, fets):
    cims_name_lower = [c["name"].lower() for c in cims]
    fets_lower = [f.lower() for f in fets]
    fets = []
    for fet in fets_lower:
        index = cims_name_lower.index(fet)
        cims[index]["fet"] = True
    return fets


def mendikat_cims_fets(cims, fets):
    fets_lower = [f.lower() for f in fets]
    fets = []
    for fet in fets_lower:
        fet = remove_text_between_parenthesis(fet).strip()

        name_variations = generate_name_variations(fet)

        found = False
        for cim in cims:
            for cim_name in cim["possible_names"]:
                for name_variation in name_variations:
                    cim_name_lower = cim_name.strip().lower()
                    print(name_variation + " vs "+cim_name_lower)

                    if cim_name_lower == name_variation or name_variation in cim_name_lower:
                        cim["fet"] = True
                        found = True
                        break

        if not found:
            raise ValueError(fet + " not found!")

    return fets


if __name__ == '__main__':
    mendikat_cims = load_mendikat_cims()
    print(len(mendikat_cims))

    cims = []
    fets = load_fets()
    mendikat_cims = load_mendikat_cims()
    mendikat_fets = mendikat_cims_fets(mendikat_cims, fets)
    """
    cent_cims_info_by_link = load_cims_info()
    cent_cims_extra_by_link = load_cims_extra()

    for link in cent_cims_info_by_link:
        cim_info = cent_cims_info_by_link[link]
        cim_extra = cent_cims_extra_by_link[link]
        cim = cim_info | cim_extra
        cim["link"] = link
        cim["fet"] = False
        cims.append(cim)

    cent_cims_fets(cims, fets)

    with open("data/100-cims.json", 'w') as cims_fd:
        json.dump(cims, cims_fd, indent=4)
    """
    with open("data/tot-cims.json", 'w') as cims_fd:
        json.dump(mendikat_cims, cims_fd, indent=4)
