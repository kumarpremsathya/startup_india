import sys
import smtplib
import traceback
from config import startup_india_config
from email.mime.text import MIMEText
from functions import log
from functions import get_data_count_database
from email.mime.multipart import MIMEMultipart


def send_email(subject, message):
    try:
        # # Email configuration
        # sender_email = 'probepoc2023@gmail.com'
        # receiver_email = 'probepoc2023@gmail.com'
        # password = 'rovqljwppgraopla'

        # # Email content
        # msg = MIMEMultipart()
        # msg['From'] = sender_email
        # msg['To'] = receiver_email
        # msg['Subject'] = f"Manual intervention required for {subject}"
        # msg.attach(MIMEText(str(message), 'plain'))

        # # Connect to the SMTP server
        # with smtplib.SMTP('smtp.gmail.com', 587) as server:
        #     server.starttls()
        #     server.login(sender_email, password)
        #     server.send_message(msg)
        pass

    except Exception as e:
        startup_india_config.log_list[1] = "Failure"
        startup_india_config.log_list[4] = get_data_count_database.get_data_count_database()
        startup_india_config.log_list[5] = "error in sending mail part"
        print(startup_india_config.log_list)
        log.insert_log_into_table(startup_india_config.log_list)
        startup_india_config.log_list = [None] * 8
        traceback.print_exc()
        print(e)
        sys.exit("script error")
