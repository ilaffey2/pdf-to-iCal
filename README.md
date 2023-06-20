# PDF to iCal Event Generator

This application is designed to extract date-related events from a PDF file and generate corresponding iCal events.

## Description

The application utilizes OpenAI's GPT models to identify and parse dates from the uploaded PDF. After the extraction, it generates iCal events corresponding to the identified dates and allows users to download an `.ics` file, which can be imported to any calendar app that supports the iCal format.

## Prerequisites

Ensure you have Python 3.6+ and pip installed.

To install required Python packages, use the following command:

```bash
pip install -r requirements.txt
```

## Setup
This application relies on OpenAI's GPT-3 and GPT-4 models. To use these models, you need to obtain an API key from OpenAI and define it in a .env file in the root directory of this project. The file should have the following format:

```bash
OPENAI_API_KEY=your_api_key_here
```

Replace your_api_key_here with your actual OpenAI API key.

## How to Run

To run this Streamlit app locally, navigate to the root directory of this project in your terminal and run:

```bash
streamlit run app.py
```

After running the command, you'll see a local URL in your command prompt. Open that URL in your browser to use the application.

## Usage

1. Upload a PDF file using the file uploader interface.
2. After successful upload, the application will process the PDF file and create iCal events.
3. Once the iCal file is created, you can download it using the "Download iCal file" button.