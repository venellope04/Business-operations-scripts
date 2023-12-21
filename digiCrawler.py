import requests
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to fetch search results from Google API
def fetch_google_results(query):
    google_api_key = 'AIzaSyAnlkwEZq2Ut_lFNSeshyRStrLpvEZb0kU'  # Replace with your Google API key
    google_search_engine_id = '71ea9a1b1dd854cc3'  # Replace with your Google Search Engine ID
    google_url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_search_engine_id}&q={query}"

    response = requests.get(google_url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return None

# Function to send emails
def send_emails(email_addresses, subject, body):
    sender_email = 'dishasarvaiya4@gmail.com'
    password = 'disha2134'

    for receiver_email in email_addresses:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)

    print("Emails sent successfully!")

# Main execution
if __name__ == "__main__":
    # Fetch search results from Google
    user_query = input("Enter your query: ")
    search_results = fetch_google_results(user_query)

    if search_results:
        # Display search results
        for index, item in enumerate(search_results, start=1):
            print(f"Result {index}:")
            print(f"Title: {item.get('title')}")
            print(f"Link: {item.get('link')}")
            print(f"Snippet: {item.get('snippet')}")
            print()

        # Read email addresses from a CSV file
        email_addresses = []
        with open('email_list.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                email_addresses.append(row['email'])

        # Define email content
        email_subject = f"Google Search Results for '{user_query}'"
        email_body = f"Here are the search results:\n\n"
        for idx, result in enumerate(search_results, start=1):
            email_body += f"Result {idx}:\nTitle: {result.get('title')}\nLink: {result.get('link')}\nSnippet: {result.get('snippet')}\n\n"

        # Send emails to addresses from the CSV file
        send_emails(email_addresses, email_subject, email_body)
    else:
        print("Failed to retrieve search results.")
