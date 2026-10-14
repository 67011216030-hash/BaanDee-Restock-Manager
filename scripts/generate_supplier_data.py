import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
GROUND_TRUTH = ROOT / "data" / "ground_truth"

def main():
    # สร้างแหล่งข้อมูลใหม่: แคตตาล็อกซัพพลายเออร์ พร้อมฝังปัญหา 4 จุด
    suppliers = [
        {"supplier_record_id": "SR-001", "product_reference": "SUP-KT104", "supplier_name": "Thai Kitchenware Co.", "reorder_point": 5, "lead_time_days": 3, "min_order_qty": 10, "contract_date": "2025-01-15"},
        # ปัญหา 1: วันที่กำกวม
        {"supplier_record_id": "SR-002", "product_reference": "SUP-BD220", "supplier_name": "Siam Bedding Ltd.", "reorder_point": 10, "lead_time_days": 5, "min_order_qty": 20, "contract_date": "07/08/2026"},
        # ปัญหา 2 & 3: รหัสไม่มาตรฐาน และค่าติดลบ
        {"supplier_record_id": "SR-003", "product_reference": " sku-0005 ", "supplier_name": "Bath & Beyond", "reorder_point": -2, "lead_time_days": 2, "min_order_qty": 15, "contract_date": "2025-06-20"},
        # ปัญหา 4: ค่าว่าง
        {"supplier_record_id": "SR-004", "product_reference": "SKU-0077", "supplier_name": "Siam Bedding Ltd.", "reorder_point": 15, "lead_time_days": None, "min_order_qty": 30, "contract_date": "2026-02-28"},
    ]
    pd.DataFrame(suppliers).to_csv(RAW / "supplier_catalog.csv", index=False)

    # สร้าง Crosswalk จับคู่รหัสสินค้า
    crosswalk = [
        {"source_system": "supplier_db", "raw_reference": "SUP-KT104", "canonical_product_id": "SKU-KT-104", "approved_by": "data_steward", "approved_at": "2026-07-31T08:30:00+07:00"},
        {"source_system": "supplier_db", "raw_reference": "SUP-BD220", "canonical_product_id": "SKU-BD-220", "approved_by": "data_steward", "approved_at": "2026-07-31T08:30:00+07:00"},
    ]
    pd.DataFrame(crosswalk).to_csv(GROUND_TRUTH / "product_reference_crosswalk.csv", index=False)
    
    print("✅ สร้างไฟล์ supplier_catalog.csv และ product_reference_crosswalk.csv สำเร็จ!")

if __name__ == "__main__":
    main()