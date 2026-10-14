from fastapi.testclient import TestClient
import pandas as pd
from pathlib import Path

# ดึงแอป API ของเรามาทดสอบ
from api.main import app
client = TestClient(app)

ROOT = Path(__file__).resolve().parents[1]

# Test Case 1: ทดสอบว่าข้อมูลซัพพลายเออร์ที่พัง ถูกกักกัน (Quarantine) จริงไหม
def test_supplier_data_quarantine():
    quarantine_file = ROOT / "data" / "checkpoints" / "quarantine_suppliers.csv"
    df = pd.read_csv(quarantine_file)
    # ต้องมีข้อมูลที่ถูกคัดออกอย่างน้อย 1 รายการ (เช่น วันที่กำกวม หรือ ค่าติดลบ)
    assert len(df) > 0
    assert "SR-002" in df["supplier_record_id"].values # ซัพพลายเออร์ที่วันที่พัง

# Test Case 2: ทดสอบ API ดึงข้อมูลซัพพลายเออร์ที่สำเร็จ (Success)
def test_get_supplier_success():
    # SKU-KT-104 เป็นข้อมูลที่คลีนแล้ว ต้องดึงได้สถานะ 200
    response = client.get("/suppliers/SKU-KT-104")
    assert response.status_code == 200
    assert response.json()["supplier_name"] == "Thai Kitchenware Co."

# Test Case 3: ทดสอบ API ดึงข้อมูลที่ไม่มีอยู่จริง (Not Found)
def test_get_supplier_not_found():
    response = client.get("/suppliers/SKU-UNKNOWN")
    assert response.status_code == 404
    assert response.json()["detail"] == "Supplier not found"

# Test Case 4: ทดสอบ API การสร้างและบันทึกใบสั่งเติม (Create/Update)
def test_save_restock_request():
    payload = {
        "product_id": "SKU-BD-220",
        "order_qty": 50,
        "notes": "Test ordering from pytest",
        "status": "Draft"
    }
    response = client.post("/restock/REQ-SKU-BD-220-TEST", json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["order_qty"] == 50

# Test Case 5: ทดสอบ API การเรียกดูใบสั่งเติมที่เพิ่งสร้าง (Read)
def test_get_saved_restock_request():
    response = client.get("/restock/REQ-SKU-BD-220-TEST")
    assert response.status_code == 200
    assert response.json()["notes"] == "Test ordering from pytest"