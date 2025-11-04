from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4

app = FastAPI()

# Allow Angular dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Demo data -----
PRODUCTS = [
    {"id": "sofa-001", "name": "Cozy Sofa", "price": 799, "imageUrl": "https://picsum.photos/seed/sofa/400/240"},
    {"id": "chair-002", "name": "Oak Chair", "price": 149, "imageUrl": "https://picsum.photos/seed/chair/400/240"},
    {"id": "table-003", "name": "Glass Table", "price": 399, "imageUrl": "https://picsum.photos/seed/table/400/240"},
]

# ----- Schemas -----
class CartItem(BaseModel):
    productId: str
    quantity: int = Field(gt=0)

class CheckoutRequest(BaseModel):
    items: List[CartItem]
    customerName: str
    email: str

class CheckoutResponse(BaseModel):
    orderId: str
    total: int

# ----- Endpoints -----
@app.get("/api/products")
def list_products():
    return PRODUCTS

@app.post("/api/checkout", response_model=CheckoutResponse)
def checkout(payload: CheckoutRequest):
    print(payload)
    # naive price lookup
    total = 0
    for item in payload.items:
        p = next((x for x in PRODUCTS if x["id"] == item.productId), None)
        if not p:
            raise HTTPException(status_code=400, detail=f"Unknown product: {item.productId}")
        total += p["price"] * item.quantity

    return CheckoutResponse(orderId=str(uuid4()), total=total)


## source .venv/scripts/activate uvicorn main:app --reload