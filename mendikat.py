import json
import glob
import gpxpy
import unicodedata


def normalize(text):
    text = remove_text_between(text)
    text = unicodedata.normalize('NFKD', text)
    text = text.replace(u"c\u0327", "ç")
    text = text.replace(u"o\u0301", "ó")
    text = text.replace(u"\u0301", "'")
    normalized = text.strip()
    return normalized


def remove_text_between(text, char_start='(', char_end=')'):
    start = text.find(char_start)
    end = text.find(char_end)
    if start != -1 and end != -1:
        return text[0:start] + text[end+1:]
    return text


def text_between(text, char_start='(', char_end=')'):
    start = text.find(char_start)
    end = text.find(char_end)
    if start != -1 and end != -1:
        return text[start+1:end]
    return None


def load_fets():
    fets = []
    with open("data/mendikat/fets.txt") as fets_fd:
        for line in fets_fd.readlines():
            fets.append(normalize(line))
    return fets


def load_mendikat_cims():
    mendikat_cims_file = glob.glob('raw-data/mendikat/*.gpx')
    cims = []
    for file in mendikat_cims_file:
        with open(file, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            for wpt in gpx.waypoints:
                name = normalize(wpt.name)

                cim = {
                    "name": name,
                    "lat": wpt.latitude,
                    "lng": wpt.longitude,
                    "area": "",  # TODO: read from metadata
                    "link": wpt.link,
                    "height": wpt.elevation,
                    "fet": False
                }
                cims.append(cim)
    # Remove all duplicated cims (same name, lat,lng)
    seen_cims = []
    unique_cims = []
    for cim in cims:
        cim_descriptor = cim["name"]+str(cim["lat"])+str(cim["lng"])
        included = cim_descriptor in seen_cims
        if not included:
            seen_cims.append(cim_descriptor)
            unique_cims.append(cim)

    return unique_cims


def mendikat_cims_fets(cims, fets):
    for fet in fets:
        founds = []
        for cim in cims:
            cim_name = cim["name"]
            cim_name_lower = cim_name.lower()
            fet_lower = fet.lower()
            fet_norm = remove_text_between(
                fet_lower, char_start='[', char_end=']').strip()
            if cim_name_lower == fet_norm:
                founds.append(cim)

        if not founds:
            raise ValueError(fet + " not found!")
        elif len(founds) > 1:
            found_candidate = False
            msg = [str(found["name"] + " " + str(found["height"]))
                for found in founds]
            # Extract height
            height_txt = text_between(remove_text_between(
                fet), char_start='[', char_end=']')
            if height_txt:
                height = float(height_txt)
                # Find a candidate with the same height
                for f in founds:
                    if f["height"] == height:
                        f["fet"] = True
                        found_candidate = True
                        break
            if not found_candidate:
                raise ValueError(
                    f"More than one found for {fet}. Candidates: {msg}")
        else:
            founds[0]["fet"] = True


if __name__ == '__main__':
    cims = load_mendikat_cims()
    fets = load_fets()
    mendikat_cims_fets(cims, fets)
    with open("data/mendikat/cims.json", 'w') as cims_fd:
        json.dump(cims, cims_fd, indent=4)
