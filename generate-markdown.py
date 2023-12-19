import json
from bs4 import BeautifulSoup


def extract_name_from_html_link(html_link):
    soup = BeautifulSoup(html_link, features='html.parser')
    return soup.findAll('a')[0].text


def extract_url_from_html_link(html_link):
    soup = BeautifulSoup(html_link, features='html.parser')
    return soup.findAll('a')[0].get("href")


def load_cims():
    cims = []
    with open("cims.json") as cims_fd:
        cims_raw = json.load(cims_fd)["data"]
        for cim_raw in cims_raw:
            cims.append({
                "name": extract_name_from_html_link(cim_raw[0]),
                "link": extract_url_from_html_link(cim_raw[0]),
                "area": cim_raw[1],
                "height": cim_raw[2]
            })
    return cims


def load_fets():
    fets = []
    with open("fets.txt") as fets_fd:
        for line in fets_fd.readlines():
            fets.append(line.strip())
    return fets


def cims_fets(cims, fets):
    cims_name_lower = [c["name"].lower() for c in cims]
    fets_lower = [f.lower() for f in fets]
    fets = []
    for fet in fets_lower:
        index = cims_name_lower.index(fet)
        fets.append(cims[index]["name"])
    return fets


def markdown(cims, fets):
    cims = sorted(cims, key=lambda x: x["name"])
    fets = cims_fets(cims, fets)
    markdown_template = f"""
# 100cims
https://www.feec.cat/activitats/100-cims/

## Listat
<div class="cims">

| Cim | Area | Alçària | Fet |
| --- | -----| ------- | --- |
"""

    with open("README.md", 'w') as readme_fd:
        readme_fd.write(markdown_template)
        for cim in cims:
            name = cim["name"]
            link = cim["link"]
            name_with_link = f"[{name}]({link})"
            area = cim["area"]
            alt = cim["height"]
            fet = ""
            if name in fets:
                fet = ":white_check_mark:"
            readme_fd.write(f"| {name_with_link} | {area} | {alt}| {fet} | \n")
        readme_fd.write("</div>")


if __name__ == '__main__':
    cims = load_cims()
    fets = load_fets()
    markdown(cims, fets)
