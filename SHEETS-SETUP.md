# Connecting the website forms to a Google Sheet

Leads land as rows in a Google Sheet in real time. Open it in Google Sheets or
download as Excel (.xlsx) any time. Free, no third-party service.

## One-time setup (about 5 minutes)

**1. Create the sheet**
- Go to sheets.google.com, create a blank spreadsheet
- Name it something like `TwoSuns Website Leads`
- In row 1, add these headers exactly, one per column:

  `Timestamp` · `Form` · `Campaign` · `Name` · `Email` · `Company` · `Job Title` · `Message` · `Page`

**2. Add the script**
- In that sheet: **Extensions → Apps Script**
- Delete whatever is in the editor, paste the code from `sheets-script.gs`
  (in this same folder), then click the save icon

**3. Deploy it**
- Click **Deploy → New deployment**
- Click the gear next to "Select type" → choose **Web app**
- Set **Execute as:** Me
- Set **Who has access:** **Anyone**  ← important, or the website cannot post to it
- Click **Deploy**, then **Authorize access** and approve the permission prompt
  (it will warn the app is unverified; that is expected for your own script,
  choose Advanced → Go to project)
- Copy the **Web app URL**. It looks like:
  `https://script.google.com/macros/s/AKfycb....../exec`

**4. Send me that URL** and I will switch the forms over to it.

## What happens until then

The forms keep posting to the existing email bridge, so no lead is ever lost
during the switchover. Once the URL is in, every submission writes a row to the
sheet AND still emails info@twosuns.ai as a backup.

## Getting the leads into Excel

In the sheet: **File → Download → Microsoft Excel (.xlsx)**. Or keep it live in
Excel with **Data → Get Data → From Web** pointed at the sheet's published link.
