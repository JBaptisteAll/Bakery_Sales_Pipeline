from fastapi import FastAPI, Header, HTTPException
from typing import Literal
import random
from pydantic import BaseModel



app = FastAPI()


products = [{"id": 1, "name": "Croissant", "price": 1.2}, 
            {"id":2, "name":"Baguette", "price": 1.1}, 
            {"id":3, "name":"Beignet", "price": 1.5}, 
            {"id":4, "name":"Pain au chaocolat", "price": 1.3}]

@app.get("/products")
def get_products(authorization: str = Header(None), limit: int = 20, skip: int = 0):
    if authorization != "Bearer fake-token-12345":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    else:
        return {
                "products": products[skip:skip + limit],
                "total": len(products),
                "skip": skip,
                "limit": limit
                }



class Commandes (BaseModel):
    type_commande: Literal["en_ligne", "traiteur"]
    mode_livraison: Literal["retrait_boutique", "transporteur_externe", "livraison_interne"]

def generer_commande():
    type_commande = random.choice(["en_ligne", "traiteur"])
    mode_livraison = ""
    if type_commande == "traiteur":
        mode_livraison = "livraison_interne"
    else:
        mode_livraison = random.choice(["retrait_boutique", "transporteur_externe"])

    ma_commande = Commandes(type_commande=type_commande, mode_livraison=mode_livraison)
    return ma_commande
    
    
@app.get("/commandes")
def get_commande(authorization: str = Header(None)) -> Commandes:
    if authorization != "Bearer fake-token-12345":
            raise HTTPException(status_code=401, detail="Invalid or missing token")
    else:
        return generer_commande()