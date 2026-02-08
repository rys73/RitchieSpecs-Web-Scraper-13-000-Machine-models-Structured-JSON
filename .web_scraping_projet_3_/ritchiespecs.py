from playwright.async_api import async_playwright, TimeoutError
import asyncio, json, logging

BASE_URL = "https://www.ritchiespecs.com"
JSON_PATH = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_3_0\ritchiespecs.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Fonction de métier pour filtrer les types de machine non exploitables
def is_valid_machine_type(name: str) -> bool:
    # On ignore les catégories génériques comme "All xxx equipment"
    return not name.lower().startswith("all ")


async def scrape_ritchiespecs():
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 1 -> Récupération de la liste complète des fabricants
        logging.info("Chargement de la liste des fabricants")
        await page.goto(f"{BASE_URL}/manufacturers", timeout=60000)
        await page.wait_for_selector("li a[href^='/manufacturer/']")

        manufacturers = await page.locator("li a[href^='/manufacturer/']").all()
        logging.info(f"{len(manufacturers)} fabricants trouvés")

        for manufacturer in manufacturers:
            manufacturer_name = (await manufacturer.inner_text()).strip()
            manufacturer_href = await manufacturer.get_attribute("href")

            logging.info(f"Fabricant : {manufacturer_name}")

            try:
                manu_page = await context.new_page()
                await manu_page.goto(f"{BASE_URL}{manufacturer_href}", timeout=60000)
                await manu_page.wait_for_selector("a[href^='/equipment/'], a.machine-type")

                # 2 -> Accès à la page d'un fabricant et récupération des types de machines
                machines_types = await manu_page.locator("a[href^='/equipment/'], a.machine-type").all()

                for machine in machines_types:
                    machines_type = (await machine.inner_text()).strip()

                    # Filtre métier : on fait une exclusion des catégories non exploitables
                    if not is_valid_machine_type(machines_type):
                        continue # SKIP "All xxx equipement"

                    machine_href = await machine.get_attribute("href")

                    models_page = await context.new_page()

                    # 3 -> Accès à la page des modèles pour un type de machine
                    await models_page.goto(f"{BASE_URL}{machine_href}", timeout=60000)
                    await models_page.wait_for_selector("div.newtab_link")
                    model_elements = await models_page.locator("div.newtab_link").all()

                    # 4 -> 1 modèle = 1 entrée structurée dans le JSON
                    for model in model_elements:
                        model_name = (await model.inner_text()).strip()

                        results.append({
                            "manufacturer": manufacturer_name,
                            "machine_type": machines_type,
                            "model": model_name
                        })
                    await models_page.close()
                await manu_page.close()

            # Gestion des pages trop lentes sans bloquer tout le scraping
            except TimeoutError:
                logging.warning(f"Timeout pour le fabricant {manufacturer_name}")
            except Exception as e:
                logging.error(f"Erreur fabricant {manufacturer_name} : {e}")

        await browser.close()
    return results

async def main():
    data = await scrape_ritchiespecs()

    # Sauvegarde finale des données prêtes à être exploitées 
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logging.info(f"Extraction terminée : {len(data)} entrées")
    print(f"Fichier généré : ritchiespecs.json ({len(data)} lignes)")

if __name__ == "__main__":
    asyncio.run(main())

