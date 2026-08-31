/**
 * TwoSuns website leads -> Google Sheet, with attachments saved to Drive.
 * Deploy: Deploy > New deployment > Web app > Execute as Me > Access: Anyone.
 *
 * The discuss form sends attachment_name and attachment_b64. The base64 arrives
 * already stripped of its data URL prefix, so it decodes directly.
 *
 * A lead is never lost to an attachment problem: saving runs in its own try,
 * and if it fails the reason is written into the Attachment column while the
 * row is appended as normal.
 */

var SHEET_ID = '1bODdvYpF5zzvHMLIkF5vcjxvsjctsvAYv9VQWQ7ZAhY';
var FOLDER_NAME = 'TwoSuns Website Leads, attachments';
var MAX_BYTES = 6 * 1024 * 1024;   // the form caps at 4 MB, this is the backstop

var HEADERS = ['Timestamp', 'Form', 'Campaign', 'Name', 'Email',
               'Company', 'Job Title', 'Message', 'Page', 'Attachment'];

var MIME = {
  pdf: 'application/pdf', txt: 'text/plain', csv: 'text/csv',
  png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif',
  doc: 'application/msword',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  xls: 'application/vnd.ms-excel',
  xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  ppt: 'application/vnd.ms-powerpoint',
  pptx: 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  zip: 'application/zip', dwg: 'image/vnd.dwg'
};

function mimeFor(name) {
  var ext = String(name).split('.').pop().toLowerCase();
  return MIME[ext] || 'application/octet-stream';
}

/** The folder attachments land in, created on first use. */
function leadFolder() {
  var it = DriveApp.getFoldersByName(FOLDER_NAME);
  return it.hasNext() ? it.next() : DriveApp.createFolder(FOLDER_NAME);
}

/**
 * Decode one attachment into Drive and return its link.
 * Files stay private to this account. Share them deliberately rather than
 * putting a lead's document behind a public link.
 */
function saveAttachment(name, b64, who) {
  var bytes = Utilities.base64Decode(b64);
  if (bytes.length > MAX_BYTES) {
    return 'not saved, ' + Math.round(bytes.length / 1048576) + ' MB exceeds the limit';
  }
  var stamp = Utilities.formatDate(new Date(), 'UTC', 'yyyy-MM-dd HHmm');
  var safe = String(who || 'lead').replace(/[^\w .-]/g, '').slice(0, 40);
  var blob = Utilities.newBlob(bytes, mimeFor(name), stamp + ' ' + safe + ' ' + name);
  return leadFolder().createFile(blob).getUrl();
}

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
    var p = (e && e.parameter) ? e.parameter : {};

    // write the header row, or extend an older one that predates this column
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
    } else if (sheet.getLastColumn() < HEADERS.length) {
      sheet.getRange(1, HEADERS.length).setValue(HEADERS[HEADERS.length - 1]);
    }

    var attachment = '';
    if (p.attachment_name && p.attachment_b64) {
      try {
        attachment = saveAttachment(p.attachment_name, p.attachment_b64, p.name);
      } catch (err) {
        attachment = 'save failed (' + p.attachment_name + '): ' + String(err);
      }
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
      p.page      || '',
      attachment
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true, attachment: !!attachment }))
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

/** Run once from the editor to prove the sheet write and the Drive write both work. */
function testWrite() {
  var b64 = Utilities.base64Encode('If you can open this file, attachment saving works.');
  doPost({ parameter: {
    form: 'Setup test', campaign: 'setup', name: 'Test Row',
    email: 'test@twosuns.ai', company: 'TwoSuns', job_title: '',
    message: 'Delete this row and its attachment once you have checked them.',
    page: 'setup',
    attachment_name: 'attachment-check.txt', attachment_b64: b64
  }});
}
