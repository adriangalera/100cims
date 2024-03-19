import json


def markdown(cims):
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
            if cim["fet"]:
                fet = ":white_check_mark:"
            readme_fd.write(f"| {name_with_link} | {area} | {alt}| {fet} | \n")
        readme_fd.write("</div>")


if __name__ == '__main__':
    with open("data/100cims/cims.json") as cims_fd:
        cims = json.load(cims_fd)
        cims = sorted(cims, key=lambda cim: cim["name"])
        markdown(cims)
