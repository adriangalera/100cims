import json
from shapely import from_geojson, get_parts, geometry, intersection


def get_tracks():
    with open('raw-data/tracks.geojson') as fd:
        geojson_str = fd.read()
        shape = from_geojson(geojson_str, on_invalid="raise")
        return get_parts(shape)


def detected_not_done_cims(cims, tracks):
    new_fets = []
    for cim in cims:
        for track in tracks:
            p = geometry.Point(cim["lng"], cim["lat"])
            p2 = p.buffer(0.0003)
            if not intersection(track, p2).is_empty and not cim["fet"]:
                cim_name = cim["name"]
                cim["fet"] = True
                print("Detected not done cim: "+cim_name)
                new_fets.append(cim["name"])

    return new_fets


def load_fets_cent_cims():
    fets = []
    with open("data/100cims/fets.txt") as fets_fd:
        for line in fets_fd.readlines():
            fets.append(line.strip())
    return fets


def load_fets_mendikat():
    fets = []
    with open("data/mendikat/fets.txt") as fets_fd:
        for line in fets_fd.readlines():
            fets.append(line.strip())
    return fets


if __name__ == '__main__':
    tracks = get_tracks()
    with open('data/100cims/cims.json') as fd:
        cent_cims = json.load(fd)
    with open('data/mendikat/cims.json') as fd:
        mendikat = json.load(fd)

    fets_cent_cims = load_fets_cent_cims()
    fets_mendikat = load_fets_mendikat()

    print("Checking 100 cims ...")
    new_cim_cent_cims = detected_not_done_cims(cent_cims, tracks)
    print("Checking mendikat ...")
    new_cim_mendikat = detected_not_done_cims(mendikat, tracks)

    with open('data/100cims/cims.json', 'w') as fd:
        json.dump(cent_cims, fd, indent=4)

    with open('data/mendikat/cims.json', 'w') as fd:
        json.dump(mendikat, fd, indent=4)

    if new_cim_cent_cims:
        fets_cent_cims.extend(new_cim_cent_cims)
        with open('data/100cims/fets.txt', 'w') as fd:
            for fet in fets_cent_cims:
                fd.write(fet+"\n")

    if new_cim_mendikat:
        fets_mendikat.extend(new_cim_mendikat)
        with open('data/mendikat/fets.txt', 'w') as fd:
            for fet in fets_mendikat:
                fd.write(fet+"\n")
