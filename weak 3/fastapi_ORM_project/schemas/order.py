from pydantic import BaseModel
from typing import List


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]


class OrderItemResponse(OrderItemCreate):
    id: int

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    total_price: float
    status: str
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True