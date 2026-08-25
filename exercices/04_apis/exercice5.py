import requests 
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def recuperer_produits(url: str) -> list[dict] | None:
    """Fetch data from a URL.

    Args:
        url: URL of the API endpoint to request.

    Returns:
        The parsed JSON response as a list of dicts, or None if all
        attempts failed or the server returned an HTTP error.
    """

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return(response.json())
    except requests.exceptions.Timeout:
        logger.error("L'API a mis trop de temps à répondre")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Impossible de joindre le serveur")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erreur HTTP : {e}")
        return None



produits = recuperer_produits("https://fakestoreapi.com/products")
print(len(produits) if produits else "Échec")

"""

produits_invalide = recuperer_produits("https://fakestoreapi.com/produits-qui-nexistent-pas")
print(produits_invalide)
"""