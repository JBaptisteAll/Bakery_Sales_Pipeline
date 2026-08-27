from fastapi import FastAPI, Header, HTTPException

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