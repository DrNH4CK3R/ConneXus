import google.generativeai as genai
import requests
from django.conf import settings

API_KEY = settings.GEMINI_API_KEY
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_event_report(event):
    # Construct the input for the model
    event_description = f"Event: {event['name']}, Date: {event['date']}, Description: {event['description']}"
    
    prompt = f"As an expert content writer, create an professional event report for the following event:\n{event_description}"
    
    # Generate the report using the Gemini model
    response = model.generate_content(prompt)
    
    if response:
        report = response.text
    else:
        report = 'Error generating report'
    
    return report