import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPSender:
    sender = ''
    password = ''
    
    @classmethod
    def load_auth(cls, filepath: str = 'auth/hooni-smtp.txt'):
        with open(filepath) as file:
            cls.sender = file.readline().split('=')[1].strip()
            cls.password = file.readline().split('=')[1].strip()
        if cls.sender is None or cls.password is None:
            raise Exception('Auth file does not contain valid information.')

    @classmethod
    def send_mail(cls,
                  receiver: str = 'gnstjdok@cau.ac.kr',
                  subject: str = '[Kei] Works',
                  message: str = '',
                  debug: bool = False):
        msg = MIMEMultipart()
        
        msg['From'] = cls.sender
        msg['To'] = receiver
        msg['Subject'] = subject

        # 이메일 본문 추가
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            # SMTP 서버에 연결
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # TLS 암호화 활성화
            server.login(cls.sender, cls.password)  # Gmail 계정으로 로그인
            text = msg.as_string()

            # 이메일 전송
            server.sendmail(cls.sender, receiver, text)
            if debug:
                print("Mail has been sent.")
                
        except Exception as e:
            print(f"Error has been occurred: {e}")
            
        finally:
            # SMTP 서버 연결 종료
            server.quit()