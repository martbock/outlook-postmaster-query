from dotenv import load_dotenv
import os
import csv
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    print('hi ' + os.getenv('APP_NAME'))


def no_env():
    print('you have no env!')


if __name__ == '__main__':
    try:
        load_dotenv()
        main()
    except:
        no_env()
        exit(1)
