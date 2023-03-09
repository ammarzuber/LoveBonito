
import mysql.connector
import pandas as pd
import smtplib


# set up email parameters
sender_email = "sender@yahoo.com"
sender_password = "1234"
receiver_email = "ammarzuber3@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port =  465

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="singapore_taxi",
  port = 3306
)


# Retrieve data from database
query = """
SELECT *
FROM cities_taxi

"""
df = pd.read_sql_query(query, conn)







low_availability = df[df["taxi_available"] < 10]

if not low_availability.empty:
    # compose email message
    subject = "Low Availability Alert"
    body = "The following areas are below the low availability threshold:\n\n" + low_availability.to_string(index=False)
    message = f"Subject: {subject}\n\n{body}"
    to = "ammarzuber3@gmail.com"

    # send email


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "ammarzuber3@gmail.com"
    msg['from'] = user
    password = "1234"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()