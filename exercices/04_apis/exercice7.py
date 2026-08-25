import requests 
import logging
import time


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def recuperer_toutes_pages(url: str, headers: dict, limit: int = 10, max_iterations: int = 50) -> list[dict] | None:
    """Fetch data from a URL.

    Args:
        url: URL of the API endpoint to request.

    Returns:
        The parsed JSON response as a list of dicts, or None if all
        attempts failed or the server returned an HTTP error.
    """

    skip = 0
    tentative = 0
    tous_les_produits = []

    logger.info("Pipeline lancé")

    while True:
        if tentative >= max_iterations:
            break
        try:
            response = requests.get(f"{url}?limit={limit}&skip={skip}", headers=headers)
            skip += limit
            tentative += 1
            response.raise_for_status()
            data = response.json()
            tous_les_produits.extend(data["products"])
            logger.info(f"Page récupérée : {skip}/{len(tous_les_produits)} produits")
            if skip >= data["total"]:
                break
        except requests.exceptions.ConnectionError:
            logger.warning(f"Tentative {tentative}/{max_iterations} échouée")
            break
        except requests.exceptions.Timeout:
            break
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erreur HTTP : {e}")
            break
    
    return(tous_les_produits)
        


if __name__ == "__main__":
    headers = {"Authorization": "Bearer fake-token-12345"}
    produits = recuperer_toutes_pages("https://dummyjson.com/products", headers, limit=20)
    print(f"Total récupéré : {len(produits) if produits else 0}")


