from playwright.sync_api import sync_playwright
import json
import glob
import getpass
import os


def download_mendikat():
    regions = [210, 221, 225, 230, 243, 304, 303, 302, 301, 305, 401]
    user = input("Mendikat.net username: ")
    passwd = getpass.getpass(prompt="Password: ")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(is_mobile=False)
        page = context.new_page()
        page.goto("https://www.mendikat.net/")
        # login
        page.get_by_text("Acceder").click()

        page.wait_for_selector('[placeholder="Usuario"]')
        page.wait_for_selector('[placeholder="Contraseña"]')

        page.fill('[placeholder="Usuario"]', user)
        page.fill('[placeholder="Contraseña"]', passwd)

        page.wait_for_timeout(1_000)

        page.get_by_role("button", name="Acceder").click()
        page.get_by_text("Perfil").click()
        first = True

        for region_id in regions:
            url = f"https://www.mendikat.net/com/region/{region_id}"
            page.goto(url)
            page.wait_for_url(url)
            page.evaluate(
                "() => document.querySelectorAll('ins').forEach( (el) => el.style.display = 'none' )")

            if first:
                page.get_by_text("Consentir").click()
                first = False

            area = page.wait_for_selector(
                "#app > div > main > div > div.section-title > h2").inner_text()
            page.get_by_text("Waypoints").click()
            page.get_by_text("Descargar").click()

            page.locator("#modal-download-conditions___BV_modal_footer_").get_by_text(
                "Acepto las condiciones").click()

            with page.expect_download() as download_info:
                page.locator(
                    "#modal-download-conditions___BV_modal_footer_").get_by_text("Descargar").click()
                download = download_info.value
                download.save_as(f"raw-data/mendikat/{area}.zip")
                print(f"{area} data downloaded")

    # now unzip all files
    zip_files = glob.glob('raw-data/mendikat/*.zip')
    for zip_file in zip_files:
        area = zip_file.split(".zip")[0].split(
            "/")[-1].replace(" ", "-").lower()
        new_file = f"raw-data/mendikat/{area}.gpx"
        os.system(f"unzip -q \"{zip_file}\" -d raw-data/mendikat/")
        os.system(f"mv raw-data/mendikat/mendikat-waypoints.gpx {new_file}")


def download_feec_data():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.feec.cat/activitats/100-cims/")
        cims_esencials = page.evaluate('() => cims_essencials')
        cims_repte = page.evaluate('() => cims_repte')
        all_cims = []
        all_cims.extend(cims_esencials)
        all_cims.extend(cims_repte)
        with open('raw-data/100cims/cims-extra.json', 'w') as f:
            json.dump(
                sorted(all_cims, key=lambda cim: cim["nombre"]), f)
        browser.close()


if __name__ == '__main__':
    download_feec_data()
    download_mendikat()
