from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from .api_client import fetch_inventory, fetch_supplier, fetch_restock_request

ROOT = Path(__file__).resolve().parents[1]
CP = ROOT / "data" / "checkpoints"

def _row_dict(row: pd.Series) -> dict:
    return {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

def build_stockout_risk_evidence(product_id: str, base_url: str | None = None) -> dict:
    inventory_df = pd.read_csv(CP / "inventory_snapshot_clean.csv", dtype=str)
    products_df = pd.read_csv(CP / "products_clean.csv", dtype=str)

    pid = product_id.strip().upper()
    evidence = {"product_id": pid}

    # 1. เช็กข้อมูลสินค้าพื้นฐาน
    prod_match = products_df.loc[products_df["product_id"] == pid]
    if prod_match.empty:
        return {"product_id": pid, "found": False, "error": "Product not found in master catalog"}
    evidence["product_info"] = _row_dict(prod_match.iloc[0])

    # 2. เช็กข้อมูลซัพพลายเออร์ (ดึงจาก API)
    sup_api = fetch_supplier(pid, base_url=base_url)
    if sup_api.ok:
        evidence["supplier"] = sup_api.data
    else:
        evidence["supplier"] = {"error": sup_api.error or "Supplier not found or unverified"}

    # 3. เทียบยอดสต็อก (ไฟล์เช้า vs API สด)
    snap_match = inventory_df.loc[inventory_df["product_id"] == pid]
    evidence["snapshot_qty"] = int(snap_match.iloc[0]["available_qty"]) if not snap_match.empty else 0
    evidence["snapshot_time"] = snap_match.iloc[0]["as_of"] if not snap_match.empty else "N/A"

    api_inv = fetch_inventory(pid, base_url=base_url)
    evidence["current_qty"] = int(api_inv.data["available_qty"]) if api_inv.ok else evidence["snapshot_qty"]
    evidence["current_time"] = api_inv.data.get("as_of", "N/A") if api_inv.ok else "API Unavailable"

    # 4. ประเมินความเสี่ยงและกฎการสั่ง (Restock Policy)
    risk_level = "Safe"
    reorder_point = 0
    if sup_api.ok:
        try:
            reorder_point = int(sup_api.data.get("reorder_point", 0))
            if evidence["current_qty"] <= reorder_point:
                risk_level = "High Risk (Below Reorder Point)"
            elif evidence["current_qty"] <= reorder_point * 1.5:
                risk_level = "Warning (Nearing Reorder Point)"
        except ValueError:
            risk_level = "Unknown (Invalid Supplier Data)"
    else:
        risk_level = "Blocked (Unverified Supplier)"

    evidence["risk_assessment"] = {
        "level": risk_level,
        "reorder_point": reorder_point,
        "decision": "draft_restock" if "Risk" in risk_level else "no_action_needed"
    }

    # 5. ดึงประวัติการขอสั่งเติม (ถ้ามี)
    request_id = f"REQ-{pid}"
    hist_api = fetch_restock_request(request_id, base_url=base_url)
    evidence["existing_request"] = hist_api.data if hist_api.ok else None

    return evidence