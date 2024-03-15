from playwright.sync_api import sync_playwright
import json

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.feec.cat/activitats/100-cims/")
        cims_esencials = page.evaluate('() => cims_essencials')
        cims_repte = page.evaluate('() => cims_repte')
        all_cims = []
        all_cims.extend(cims_esencials)
        all_cims.extend(cims_repte)
        with open('raw-data/cims-extra.json', 'w') as f:
            json.dump(
                sorted(all_cims, key=lambda cim: cim["nombre"]), f)
        browser.close()
