/**
 * TwoSuns website leads -> Google Sheet
 * Deploy: Deploy > New deployment > Web app > Execute as Me > Access: Anyone.
 */

var SHEET_ID = '1bODdvYpF5zzvHMLIkF5vcjxvsjctsvAYv9VQWQ7ZAhY';

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
    var p = (e && e.parameter) ? e.parameter : {};

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp','Form','Campaign','Name','Email',
                       'Company','Job Title','Message','Page']);
    }

    sheet.appendRow([
      new Date(),
      p.form      || '',
      p.campaign  || '',
      p.name      || '',
      p.email     || '',
      p.company   || '',
      p.job_title || '',
      p.message   || '',
      p.page      || ''
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('TwoSuns lead endpoint is running.');
}

/** Run this once from the editor to check it can write to the sheet. */
function testWrite() {
  doPost({ parameter: {
    form: 'Setup test', campaign: 'setup', name: 'Test Row',
    email: 'test@twosuns.ai', company: 'TwoSuns', job_title: '',
    message: 'If you can see this row, the script works.', page: 'setup'
  }});
}
