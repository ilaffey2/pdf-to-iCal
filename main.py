import ics
import json
import streamlit as st
from datetime import datetime, timedelta
import tempfile

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.document_loaders import PyPDFLoader

from dotenv import load_dotenv
load_dotenv()

from helpers import parse_shitty_gpt_turbo

st.title('PDF to iCal')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())

    loader = PyPDFLoader(tfile.name)
    all_pages = loader.load_and_split()

    gpt3 = ChatOpenAI(model_name="gpt-3.5-turbo")
    gpt4 = ChatOpenAI(model_name="gpt-4")

    date_pages = []

    for page in all_pages:
        message = HumanMessage(content=page.page_content)
        response = gpt3.predict_messages([SystemMessage(content="You are a classifying model for text containing dates. You return a boolean that indicates whether a given piece of text contains dates."),
            HumanMessage(content="Return true if the text contains dates. Return false if it does not. Only respond using booleans. Do not include any other justification of your reasoning. Your response should be one word, do not use punctuation or capitilization"), message])
        if parse_shitty_gpt_turbo(text=response.content):
            date_pages.append(page)

    raw_responses = []
    for page in date_pages:
        message = HumanMessage(content=page.page_content)
        response = gpt4.predict_messages([SystemMessage(content="You are a scheduling assistant model. You will be given a piece of text containing dates. Generate events for them in iCal format. The current year is 2023. Only respond in json."),                              
        HumanMessage(content='''Generate iCal events from any date in the following text. Include datetime info as well as description and title. Return these iCal events as a list of json formatted iCal events. Ensure they are parseable by python json.loads. If there are no dates, you can return a boolean false in json form.

       Sample response: {
      "BEGIN": "VEVENT",
      "DTSTART": "20230105T000000",
      "SUMMARY": "Organizations and Organization Design",
      "DESCRIPTION": "Session 2: Organizations and Organization Design. Read Daft Chapter 1 prior to class.",
      "END": "VEVENT"
    }'''), message])
        raw_responses.append(response.content)

    ical_dates = []
    for raw_response in raw_responses:
        try:
            ical_dates.extend(json.loads(raw_response))
        except:
            pass

    calendar = ics.Calendar()

    for ical_date in ical_dates:
        print(ical_date)
        event = ics.Event()
        event.name = ical_date.get("SUMMARY")

        dtstart_key = next((key for key in ical_date.keys() if "DTSTART" in key), None)
        if dtstart_key is not None:
            dtstart = datetime.strptime(ical_date.get(dtstart_key), "%Y%m%dT%H%M%S")    
            event.begin = dtstart
        else:
            # Handle error here if DTSTART is not in the dictionary
            pass

        dtend_key = next((key for key in ical_date.keys() if "DTEND" in key), None)
        if dtend_key is not None:
            # Add 1 hour to the start time to get the end time
            dtend = dtstart + timedelta(hours=1)
            event.end = dtend
        else:
            # Handle error here if DTEND is not in the dictionary
            pass

        event.description = ical_date.get("DESCRIPTION")

        calendar.events.add(event)


    # Now write the calendar to an iCal file
    with open('my_calendar.ics', 'w') as my_file:
        my_file.writelines(calendar)

    st.success('iCal created successfully')
    st.download_button(
        label="Download iCal file",
        data=open('my_calendar.ics', 'r').read(),
        file_name='my_calendar.ics',
        mime='text/calendar',
    )
