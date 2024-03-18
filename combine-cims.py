import json
from bs4 import BeautifulSoup
import glob
import gpxpy


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
    mendikat_cims_file = glob.glob('raw-data/mendikat-waypoints.gpx*')
    cims = []
    for file in mendikat_cims_file:
        with open(file, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            for wpt in gpx.waypoints:
                name = remove_text_between_parenthesis(wpt.name).strip()
                possible_names = [name]
                if wpt.comment:
                    possible_names.extend([remove_text_between_parenthesis(
                        possible).strip() for possible in wpt.comment.split(",")])

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
        found = False
        for cim in cims:
            for cim_name in cim["possible_names"]:
                cim_name_lower = cim_name.lower()
                print(fet + " vs "+cim_name_lower)

                if cim_name_lower == fet or fet in cim_name_lower:
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
    with open("data/mendikat-cims.json", 'w') as cims_fd:
        json.dump(mendikat_cims, cims_fd, indent=4)
