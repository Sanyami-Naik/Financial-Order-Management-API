from pydantic import BaseModel
from typing import List
import sqlite3
from fastapi import FastAPI

app = FastAPI()


class Order(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str


db = sqlite3.connect(':memory:', check_same_thread=False)
cursor = db.cursor()
cursor.execute('''CREATE TABLE orders (symbol TEXT, price REAL, quantity INTEGER, order_type TEXT)''')

@app.post("/orders")
def create_order(order: Order):
    cursor.execute("INSERT INTO orders (symbol, price, quantity, order_type) VALUES (?, ?, ?, ?)",
                   (order.symbol, order.price, order.quantity, order.order_type))
    db.commit()
    return {"message": "Order created successfully"}

@app.get("/orders", response_model=List[Order])
def get_orders():
    cursor.execute("SELECT symbol, price, quantity, order_type FROM orders")
    rows = cursor.fetchall()
    return [Order(symbol=row[0], price=row[1], quantity=row[2], order_type=row[3]) for row in rows]


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}