import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDateTime
import speech_recognition as sr

class SpeechRecognitionThread(QThread):
    speech_recognized = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_listening = False

    def run(self):
        with sr.Microphone() as source:
            self.is_listening = True
            while self.is_listening:
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio, language='th')
                    self.speech_recognized.emit(text)
                except sr.UnknownValueError:
                    self.speech_recognized.emit("ไม่สามารถรับรู้เสียงได้")
                except sr.RequestError as e:
                    self.speech_recognized.emit(f"ผิดพลาดในการเรียกใช้ API: {e}")

    def stop_listening(self):
        self.is_listening = False

class SpeechRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread = None
        self.recorded_text = ""

    def initUI(self):
        self.setWindowTitle('Speech Recognition App')

        # กำหนดสีพื้นหลังของหน้าต่าง
        self.setStyleSheet("background-color: #f0f0f0;")

        self.setGeometry(100, 100, 600, 400)

        # สร้าง QLabel สำหรับแสดงรูปภาพ
        self.image_label = QLabel(self)
        pixmap = QPixmap('speech_recognition.png')  # เปลี่ยนเป็นที่อยู่ของรูปภาพที่คุณมี
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)  # จัดตำแหน่งรูปภาพตรงกลาง

        # สร้างปุ่ม
        self.record_button = QPushButton('เริ่มพูด', self)
        self.stop_button = QPushButton('หยุดพูด', self)
        self.save_button = QPushButton('บันทึกเป็นไฟล์', self)

        # กำหนดสีพื้นหลังและขนาดของปุ่ม
        self.record_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 16px; border: none; border-radius: 4px;")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; padding: 8px 16px; border: none; border-radius: 4px;")
        self.save_button.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 16px; border: none; border-radius: 4px;")

        # กำหนดรูปแบบของปุ่มเป็นรูปสี่เหลี่ยมจตุรัส
        self.record_button.setFixedWidth(120)  # กำหนดความกว้าง
        self.record_button.setFixedHeight(40)  # กำหนดความสูง

        self.stop_button.setFixedWidth(120)
        self.stop_button.setFixedHeight(40)

        self.save_button.setFixedWidth(120)
        self.save_button.setFixedHeight(40)

        # สร้าง QTextEdit สำหรับแสดงข้อความที่บันทึกไว้
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # เชื่อมต่อการคลิกปุ่มกับเมทอด
        self.record_button.clicked.connect(self.start_recognition)
        self.stop_button.clicked.connect(self.stop_recognition)
        self.save_button.clicked.connect(self.save_text_to_file)

        # เรียงลำดับ Layout ด้วย QHBoxLayout สำหรับปุ่ม
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_button)

        # เรียงลำดับ Layout หลักด้วย QVBoxLayout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)  # เพิ่มรูปภาพลงใน Layout
        main_layout.addLayout(button_layout)  # เพิ่มปุ่มลงใน Layout
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)

    def start_recognition(self):
        if not self.thread or not self.thread.isRunning():
            self.thread = SpeechRecognitionThread()
            self.thread.speech_recognized.connect(self.update_text)
            self.thread.start()

    def stop_recognition(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop_listening()

    def update_text(self, text):
        self.recorded_text += text + "\n"
        self.text_edit.setPlainText(self.recorded_text)

    def save_text_to_file(self):
        if self.recorded_text:
            try:
                # ดึงเวลาปัจจุบัน
                current_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
                # เปิดไฟล์ที่ต้องการเพิ่มข้อมูลเข้าไป
                with open('recorded_text.txt', 'a', encoding='utf-8') as f:
                    # เพิ่มข้อมูลที่ต้องการบันทึกไป
                    f.write(f"[{current_time}] {self.recorded_text}\n")
                QMessageBox.information(self, 'บันทึกสำเร็จ', 'บันทึกคำพูดเป็นไฟล์สำเร็จ')
            except Exception as e:
                QMessageBox.warning(self, 'เกิดข้อผิดพลาด', f'ไม่สามารถบันทึกไฟล์: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpeechRecognitionApp()
    ex.show()
    sys.exit(app.exec_())
