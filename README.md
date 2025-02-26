
# Timesheet Generator

This application was developed to generate timesheets in PDF format for employees of an organization based on a JSON file containing employee and holiday information. It allows you to choose the month and year, and download all the generated timesheets in a zip file.

## Features

- Upload a JSON file with employee and holiday data.
- Select the month and year to generate the timesheets.
- Generate PDFs with employee details, including:
  - Name, role, and department.
  - Identified holidays and weekends.
  - A signature line for the supervisor.
- Download all the generated PDFs in a ZIP file.

## Example JSON File

The JSON file should follow this format:

```json
{
  "organization": {
    "state": "Minas Gerais",
    "city": "Barbacena",
    "name": "Organization Name",
    "department": "Department",
    "supervisor": "Supervisor Name"
  },
  "employees": [
    {
      "name": "First Employee",
      "role": "Position"
    },
    {
      "name": "Second Employee",
      "role": "Position"
    }
  ],
  "holidays": {
    "january": [],
    "february": [],
    "march": [],
    "april": [],
    "may": [],
    "june": [],
    "july": [],
    "august": [14],
    "september": [],
    "october": [],
    "november": [],
    "december": [8]
  }
}
```

## How to Use

1. Visit the deployed Streamlit app [here](https://timesheet-generator.streamlit.app/).
2. Upload a valid JSON file.
3. Select the month and year.
4. Click on "Generate Timesheets" to download the PDF files as a zip.

## Streamlit Interface
![image](https://github.com/user-attachments/assets/9812bcbb-1a29-4bae-9eee-81792d3306e5)

## Timesheet Example
![image](https://github.com/user-attachments/assets/b5a1b476-debb-4468-93e9-fed01b124d51)

## Requirements

- Python 3.7+
- Streamlit
- ReportLab
- Other required packages are listed in `requirements.txt`.

