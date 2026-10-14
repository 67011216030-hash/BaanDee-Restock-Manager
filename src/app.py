from __future__ import annotations
import os
from pathlib import Path
import gradio as gr
from src.evidence import build_stockout_risk_evidence
from src.api_client import save_restock

ROOT = Path(__file__).resolve().parents[1]

# โหลดข้อมูลเคสเพื่อโชว์ในแท็บที่ 1
def load_risk_case(product_id: str):
    evidence = build_stockout_risk_evidence(product_id.strip().upper())
    
    # ดึงค่ามาเติมในฟอร์มของแท็บที่ 2
    req_id = f"REQ-{evidence['product_id']}"
    hist = evidence.get("existing_request")
    
    if hist:
        # ถ้าเคยบันทึกไว้แล้ว ให้ดึงของเดิมมาโชว์
        return evidence, evidence["risk_assessment"], req_id, hist["order_qty"], hist["notes"], hist["status"], f"Loaded existing request: {req_id}"
    else:
        # ถ้ายังไม่เคยบันทึก ให้เสนอค่าเริ่มต้น
        suggested_qty = 0
        if evidence.get("supplier") and "error" not in evidence["supplier"]:
            suggested_qty = int(evidence["supplier"].get("min_order_qty", 0))
            
        status = "Draft"
        if "Blocked" in evidence.get("risk_assessment", {}).get("level", ""):
            status = "Hold for Review (Supplier Error)"
            
        return evidence, evidence["risk_assessment"], req_id, suggested_qty, "Auto-drafted based on risk level.", status, "No previous request found. Created draft."

# บันทึกข้อมูลใบสั่งเติมสินค้า
def submit_restock(req_id, qty, notes, status):
    payload = {
        "product_id": req_id.replace("REQ-", ""),
        "order_qty": int(qty),
        "notes": notes,
        "status": status
    }
    result = save_restock(req_id, payload)
    if result.ok:
        return f"✅ Success: Saved {req_id} at {result.data['data']['updated_at']}"
    return f"❌ Error: {result.error}"

def build_app() -> gr.Blocks:
    with gr.Blocks(title="BaanDee Stockout Risk & Restock Manager") as demo:
        gr.Markdown("# 📦 BaanDee Stockout Risk & Restock Manager")
        gr.Markdown("Classroom demonstration: **Team Final Project (Stockout Management)**")
        
        with gr.Row():
            # เราใช้ 2 SKU นี้เพราะอาจารย์ซ่อนลูกเล่นสต็อกไม่ตรงกันไว้ให้แล้ว
            product_selector = gr.Dropdown(
                choices=["SKU-KT-104", "SKU-BD-220"], 
                value="SKU-KT-104", 
                label="Select Product SKU to Inspect"
            )
            load_btn = gr.Button("🔍 Check Risk & Evidence", variant="primary")

        with gr.Tabs():
            # แท็บ 1: โชว์หลักฐานและการประเมินความเสี่ยง (อ่านอย่างเดียว)
            with gr.TabItem("1. Risk Assessment & Evidence"):
                with gr.Row():
                    risk_ui = gr.JSON(label="Risk Assessment & Policy Decision")
                    evidence_ui = gr.JSON(label="Raw Evidence (API vs Snapshot)")
                    
            # แท็บ 2: ฟอร์ม CRUD สำหรับสร้างและบันทึกใบสั่งเติมสินค้า (เขียนและอ่าน)
            with gr.TabItem("2. Create / Edit Restock Request (CRUD)"):
                gr.Markdown("### Create or Update Restock Request")
                gr.Markdown("Changes made here are saved via API and persist in the system.")
                with gr.Row():
                    req_id_ui = gr.Textbox(label="Request ID", interactive=False)
                    status_ui = gr.Dropdown(
                        choices=["Draft", "Pending Approval", "Approved", "Hold for Review (Supplier Error)"],
                        label="Status"
                    )
                with gr.Row():
                    qty_ui = gr.Number(label="Order Quantity", precision=0)
                    notes_ui = gr.Textbox(label="Notes / Justification", lines=2)
                
                save_btn = gr.Button("💾 Save Restock Request", variant="primary")
                save_status_ui = gr.Textbox(label="Save Status", interactive=False)

        # ผูกปุ่มเข้ากับฟังก์ชัน
        load_btn.click(
            fn=load_risk_case,
            inputs=[product_selector],
            outputs=[evidence_ui, risk_ui, req_id_ui, qty_ui, notes_ui, status_ui, save_status_ui]
        )
        
        save_btn.click(
            fn=submit_restock,
            inputs=[req_id_ui, qty_ui, notes_ui, status_ui],
            outputs=[save_status_ui]
        )

    return demo

if __name__ == "__main__":
    build_app().launch(server_name="127.0.0.1", server_port=7860, share=True)