อธิบายการทำงานของโค้ด
โค้ดนี้เป็นแอปพลิเคชันสำหรับการรับรู้เสียง (Speech Recognition) โดยใช้ PyQt5 สำหรับสร้าง GUI และใช้ speech_recognition สำหรับแปลงเสียงเป็นข้อความ ตัวแอปพลิเคชันมีการทำงานดังนี้:

1. การนำเข้าโมดูลที่จำเป็น
    sys: สำหรับการใช้งานกับคำสั่งระบบ
    PyQt5.QtWidgets, PyQt5.QtGui, PyQt5.QtCore: สำหรับการสร้างหน้าต่างและการจัดการ GUI
    speech_recognition as sr: สำหรับการแปลงเสียงเป็นข้อความ
2. สร้างคลาส SpeechRecognitionThread
- เป็นคลาสที่สืบทอดจาก QThread เพื่อทำงานในการรับรู้เสียงในเธรดแยก
- มีสัญญาณ speech_recognized เพื่อส่งข้อความที่ถูกแปลงแล้วกลับไปยัง GUI
- ในเมทอด run จะเปิดไมโครโฟนเพื่อฟังและแปลงเสียงเป็นข้อความโดยใช้ Google Speech Recognition API
เมทอด stop_listening จะหยุดการฟังเสียง
3. สร้างคลาส SpeechRecognitionApp
 เป็นคลาสที่สืบทอดจาก QWidget เพื่อสร้าง GUI
- ในเมทอด initUI จะทำการตั้งค่าหน้าต่างและสร้างวิดเจ็ตต่าง ๆ เช่น ปุ่ม, รูปภาพ, และ QTextEdit สำหรับแสดงข้อความ
- มีเมทอด start_recognition เพื่อเริ่มการรับรู้เสียงโดยเริ่มเธรด SpeechRecognitionThread
- มีเมทอด stop_recognition เพื่อหยุดการรับรู้เสียง
- มีเมทอด update_text เพื่ออัปเดตข้อความที่ได้รับการแปลงเสียงเป็นข้อความลงใน QTextEdit
- มีเมทอด save_text_to_file เพื่อบันทึกข้อความที่แปลงได้เป็นไฟล์ recorded_text.txt
4. เมนฟังก์ชัน
  เริ่มแอปพลิเคชัน PyQt ด้วย QApplication
  สร้างอินสแตนซ์ของ SpeechRecognitionApp
  เรียกเมทอด show เพื่อแสดงหน้าต่าง
  รันลูปหลักของแอปพลิเคชันด้วย app.exec_()
โค้ดนี้สร้างอินเทอร์เฟซที่ใช้งานง่ายสำหรับการรับรู้เสียง โดยมีการจัดการเริ่มและหยุดการฟังเสียง และการบันทึกข้อความที่ได้รับการแปลงเป็นไฟล์.
