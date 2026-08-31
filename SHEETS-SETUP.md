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

## One tab per call to action

Every lead is written twice on purpose. The first tab in the workbook stays the
master, the single place to see the whole pipeline in date order. A second copy
goes to a tab named after the call to action that produced it, created the first
time a lead arrives from that button, so the workbook only grows as real demand
does.

The site has eleven distinct calls to action today. `Discuss Your Needs` is the
general one and appears on every page; the rest are specific, so their tabs are
the interesting ones. A lead with no campaign value lands in `Unattributed`.

Set `ALSO_MASTER = false` in the script if you would rather have no master tab
and no duplication.

## Attachments

The discuss form accepts a file up to 4 MB. `sheets-script.gs` decodes it,
saves it to a Drive folder called **TwoSuns Website Leads, attachments**, and
writes the link into the Attachment column. The folder is created on first use.

Files stay **private to the account that owns the script**. Share them
deliberately rather than putting a lead's document behind a public link.

If a file ever fails to save the lead is still recorded, with the reason in the
Attachment column instead of a link.

**After changing the script you must redeploy, or the website keeps hitting the
old version:** Deploy > Manage deployments > pencil icon > Version: New version
> Deploy. Keep the same deployment so the URL does not change.

## Getting the leads into Excel

In the sheet: **File → Download → Microsoft Excel (.xlsx)**. Or keep it live in
Excel with **Data → Get Data → From Web** pointed at the sheet's published link.
