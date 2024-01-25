import requests
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QStyleFactory
from PyQt5.QtGui import QColor 
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QFont

class GoogleSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Widgets
        self.query_label = QLabel('Enter your query:')
        self.query_input = QLineEdit()
        self.query_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")
        self.query_input.setFont(QFont('Arial', 12))


        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        self.search_button.setFont(QFont('Arial', 12))
        

        self.email_label = QLabel('Enter recipient email addresses (comma-separated):')
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")
        self.email_input.setFont(QFont('Arial', 12))


        self.send_button = QPushButton('Send Emails')
        self.send_button.clicked.connect(self.send_emails)
        self.send_button.setFont(QFont('Arial', 12))
        

        self.result_display = QTextEdit()
        self.result_display.setStyleSheet("background-color: #353535; color: #FFFFFF;")
        self.result_display.setFont(QFont('Arial', 12))


        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.query_label)
        layout.addWidget(self.query_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

        self.setWindowTitle('DigiCrawler')
        self.setGeometry(300, 300, 500, 400)

        # Set dark gray theme
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)



    def search(self):
        # Fetch user query
        user_query = self.query_input.text()

        # Fetch search results from Google
        search_results = fetch_google_results(user_query)

        if search_results:
            # Display search results in the GUI
            result_text = ""
            for index, item in enumerate(search_results, start=1):
                result_text += f"Result {index}:\nTitle: {item.get('title')}\nLink: {item.get('link')}\nSnippet: {item.get('snippet')}\n\n"

            self.result_display.setPlainText(result_text)
        else:
            self.result_display.setPlainText("Failed to retrieve search results.")

    def send_emails(self):
        # Get recipient email addresses from the GUI
        recipient_emails = self.email_input.text().split(',')

        # Store email addresses in a CSV file
        with open('Email_List.csv', 'w', newline='') as csvfile:
            fieldnames = ['email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for email in recipient_emails:
                writer.writerow({'email': email.strip()})

        # Define email content
        email_subject = f"Google Search Results for '{self.query_input.text()}'"
        email_body = f"Here are the search results:\n\n{self.result_display.toPlainText()}"

        # Send emails to addresses from the CSV file
        send_emails(recipient_emails, email_subject, email_body)



# Function to fetch search results from Google API
def fetch_google_results(query):
    google_api_key = 'AIzaSyAnlkwEZq2Ut_lFNSeshyRStrLpvEZb0kU'  
    google_search_engine_id = '71ea9a1b1dd854cc3'  
    google_url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_search_engine_id}&q={query}"

    response = requests.get(google_url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return None

# Function to send emails
def send_emails(email_addresses, subject, body):
    sender_email = 'misaamane573@gmail.com'
    password = 'exfx rkzi uaoc wgyk'

    for receiver_email in email_addresses:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)

    print("Emails sent successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = GoogleSearchApp()
    ex.show()
    sys.exit(app.exec_())

