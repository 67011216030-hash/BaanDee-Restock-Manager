# 📦 BaanDee Stockout Risk & Restock Manager

โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชา โดยต่อยอดจากระบบ BaanDee Living เดิม ให้กลายเป็น **"ระบบตรวจสอบความเสี่ยงสินค้าขาดสต็อกและจัดการใบสั่งเติมสินค้า"** แบบครบวงจร (Full-stack MVP)

## ✨ ผลงานที่ทีมของเราพัฒนาเพิ่มเติม (Team's Contributions)

โปรเจกต์นี้ครอบคลุมการทำงานตั้งแต่ Data Engineering ไปจนถึง Frontend และ Testing:

1. **Data Engineering (`scripts/generate_supplier_data.py`)**
   - สร้างสคริปต์จำลองแหล่งข้อมูลใหม่ (Supplier Catalog) 
   - ตั้งใจฝังปัญหาคุณภาพข้อมูล (Data Quality Issues) เช่น วันที่กำกวม (Ambiguous Dates), รหัสไม่ตรงรูปแบบ, และค่าตัวเลขที่ติดลบ

2. **Data Cleaning & Quarantine (`src/data_prep.py`)**
   - เขียนกฎการทำความสะอาดข้อมูลซัพพลายเออร์
   - สร้างระบบ **Quarantine** เพื่อคัดแยกข้อมูลซัพพลายเออร์ที่มีปัญหาออกไปเก็บไว้ต่างหาก (Safeguard) ป้องกันไม่ให้ระบบนำข้อมูลที่ผิดพลาดไปใช้งานต่อ

3. **Backend & API (`api/main.py` & `src/api_client.py`)**
   - สร้าง FastAPI endpoint ใหม่เพื่อดึงข้อมูลซัพพลายเออร์
   - สร้างระบบ **CRUD** สำหรับใบสั่งเติมสินค้า (Restock Requests) โดยสามารถบันทึกและดึงข้อมูลกลับมาจากไฟล์ JSON ได้จริง

4. **Frontend Logic & UI (`src/app.py` & `src/evidence.py`)**
   - พัฒนาหน้าจอเว็บแอปพลิเคชันด้วย Gradio
   - วาง Logic ประเมินความเสี่ยงสต็อก โดยตรวจสอบข้อมูลซัพพลายเออร์ที่ถูก Quarantine
   - หากข้อมูลซัพพลายเออร์มีปัญหา ระบบจะล็อกสถานะใบสั่งซื้อเป็น `Hold for Review (Supplier Error)` อัตโนมัติเพื่อความปลอดภัย

5. **Unit Testing (`tests/test_restock_manager.py`)**
   - เขียนชุดทดสอบด้วย `pytest` จำนวน 5 กรณี (Test Cases)
   - ครอบคลุมการทดสอบ Quarantine, API Response (200 & 404), และการทำ CRUD
   - **สถานะ:** 5 Passed (100% Success)

## 🚀 วิธีรันโปรเจกต์ (How to run)

1. เปิด Terminal และเปิดใช้งาน Virtual Environment: `.\.venv\Scripts\activate`
2. สร้างข้อมูลและคลีนข้อมูล: 
   - `python scripts/generate_supplier_data.py`
   - `python src/data_prep.py`
3. รัน API (เปิด Terminal ที่ 1): `python -m uvicorn api.main:app --host 127.0.0.1 --port 8000`
4. รันหน้าเว็บ (เปิด Terminal ที่ 2): `python -m src.app`
5. รันชุดทดสอบ: `pytest tests/test_restock_manager.py -v`