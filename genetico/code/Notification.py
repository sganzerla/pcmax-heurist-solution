from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os


class Notification:

    def __init__(self, path_credent: str):
        self.__data = self.__read_credential__(path_credent)
        self.__sender = self.__data[0]
        self.__pass = self.__data[1]
        self.__receivers = self.__data[2].split(",")
        self.__smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.__smtp.ehlo()
        self.__smtp.starttls()
        self.__auth = True
        try:
            self.__smtp.login(self.__sender, self.__pass)
        except:
            self.__auth = False
            print("Erro de autenticação.")
            print("\n1º - Diminua o nível de segurança do Gmail no link:")
            print("https://www.google.com/settings/security/lesssecureapps")
            print(
                "\n2º - Confira as credenciais nas 3 linhas se estão corretas no arquivo credentials:")
            print("emissor@somente.gmail.com")
            print("senha emissor")
            print("dest1@hotmail.com, dest2@yahoo.com, dest19@bol.com.br")

    def __read_credential__(self, file):
        return open(file, 'r').readlines()

    def send_message(self, subject="Report", text="", attachment=None):
        if not self.__auth:
            exit()

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        if attachment is not None:
            if type(attachment) is not list:
                attachment = [attachment]
            for one_attachment in attachment:
                with open(one_attachment, 'rb') as f:
                    file = MIMEApplication(
                        f.read(), name=os.path.basename(one_attachment))
                file['Content-Disposition'] = f'attachment; filename="{os.path.basename(one_attachment)}"'
                msg.attach(file)

        self.__smtp.sendmail(from_addr=self.__sender,
                             to_addrs=self.__receivers, msg=msg.as_string())
        self.__smtp.quit()