from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

HERE = Path(__file__).resolve().parent

def _load(name: str) -> dict:
    path = HERE / "fixtures" / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def _save(name: str, data: dict) -> None:
    path = HERE / "fixtures" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

ORDERS = _load("orders.json")
INVENTORY = _load("inventory.json")
TICKETS = _load("tickets.json")

# โหลดข้อมูลซัพพลายเออร์ที่คลีนแล้วมาเป็นฐานข้อมูลจำลองของ API
import pandas as pd
try:
    sup_df = pd.read_csv(HERE.parent / "data" / "checkpoints" / "supplier_catalog_clean.csv", dtype=str)
    SUPPLIERS = sup_df.set_index("product_id_clean").to_dict(orient="index")
except Exception:
    SUPPLIERS = {}

app = FastAPI(title="BaanDee Simulated Company API", version="1.0.0")

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "baandee-classroom-api"}

@app.get("/orders/{order_id}")
def get_order(order_id: str) -> dict:
    record = ORDERS.get(order_id.upper())
    if record is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return record

@app.get("/inventory/{product_id}")
def get_inventory(product_id: str) -> dict:
    record = INVENTORY.get(product_id.upper())
    if record is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return record

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str) -> dict:
    record = TICKETS.get(ticket_id.upper())
    if record is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return record

# --- ส่วนที่เพิ่มใหม่สำหรับโจทย์ Restock Manager (การทำ CRUD) ---

@app.get("/suppliers/{product_id}")
def get_supplier(product_id: str) -> dict:
    record = SUPPLIERS.get(product_id.upper())
    if record is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return record

# กำหนดโครงสร้างข้อมูลใบสั่งเติมสินค้า
class RestockRequest(BaseModel):
    product_id: str
    order_qty: int
    notes: str
    status: str

# API สำหรับบันทึก/สร้างใบสั่งเติมสินค้า (อัปเดตไฟล์ JSON)
@app.post("/restock/{request_id}")
def save_restock_request(request_id: str, req: RestockRequest) -> dict:
    db = _load("restock_requests.json")
    record = {
        "request_id": request_id.upper(),
        "product_id": req.product_id,
        "order_qty": req.order_qty,
        "notes": req.notes,
        "status": req.status,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    db[request_id.upper()] = record
    _save("restock_requests.json", db)
    return {"message": "Saved successfully", "data": record}

# API สำหรับเรียกดูใบสั่งเติมสินค้าเดิม
@app.get("/restock/{request_id}")
def get_restock_request(request_id: str) -> dict:
    db = _load("restock_requests.json")
    record = db.get(request_id.upper())
    if record is None:
        raise HTTPException(status_code=404, detail="Restock request not found")
    return record