import json
from bs4 import BeautifulSoup


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


def cims_fets(cims, fets):
    cims_name_lower = [c["name"].lower() for c in cims]
    fets_lower = [f.lower() for f in fets]
    fets = []
    for fet in fets_lower:
        index = cims_name_lower.index(fet)
        cims[index]["fet"] = True
    return fets


if __name__ == '__main__':
    cims = []
    fets = load_fets()
    cims_info_by_link = load_cims_info()
    cims_extra_by_link = load_cims_extra()

    for link in cims_info_by_link:
        cim_info = cims_info_by_link[link]
        cim_extra = cims_extra_by_link[link]
        cim = cim_info | cim_extra
        cim["link"] = link
        cim["fet"] = False
        cims.append(cim)

    cims_fets(cims, fets)

    with open("data/cims.json", 'w') as cims_fd:
        json.dump(cims, cims_fd, indent=4)
