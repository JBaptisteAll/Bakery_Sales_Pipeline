import requests 
import logging
import time


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def recuperer_avec_retry(url: str, max_tentatives: int = 3) -> list[dict] | None:
    """Fetch data from a URL, retrying on transient network errors.

    Args:
        url: URL of the API endpoint to request.
        max_tentatives: Maximum number of retry attempts on timeout
            or connection errors.

    Returns:
        The parsed JSON response as a list of dicts, or None if all
        attempts failed or the server returned an HTTP error.
    """

    for tentative in range(1, max_tentatives + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return(response.json())
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            logger.warning(f"Tentative {tentative}/{max_tentatives} échouée")
            if tentative < max_tentatives:
                time.sleep(2 ** tentative)  # 2s, 4s, 8s...
        except requests.exceptions.HTTPError as e:
                logger.error(f"Erreur HTTP : {e}")
    logger.error("Échec définitif après plusieurs tentatives")
    return None
        


"""
# httpbin.org/delay/10 répond après 10 secondes → va timeout avec timeout=5
resultat = recuperer_avec_retry("https://httpbin.org/delay/10", max_tentatives=3)
print(resultat)

"""

# Et vérifie que le cas normal marche toujours
produits = recuperer_avec_retry("https://fakestoreapi.com/products")
print(len(produits) if produits else "Échec")
