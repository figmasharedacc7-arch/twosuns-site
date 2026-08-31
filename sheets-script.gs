/**
 * TwoSuns website leads -> Google Sheet, one tab per call to action.
 * Deploy: Deploy > Manage deployments > pencil > New version > Deploy.
 * Use the SAME deployment, or the URL changes and the website stops reaching it.
 *
 * Every lead is written twice on purpose: once to the master tab, which stays
 * the single place to see the whole pipeline, and once to a tab named after the
 * call to action that produced it. Tabs are created the first time a lead
 * arrives from that call to action, so the sheet only grows as real demand does.
 * Set ALSO_MASTER to false if you would rather have no master tab.
 *
 * The discuss form sends attachment_name and attachment_b64, base64 already
 * stripped of its data URL prefix. Attachments go to Drive and the link is
 * written into the Attachment column.
 *
 * A lead is never lost to a downstream problem: attachment saving and per-tab
 * routing each run in their own try, and the master write still happens.
 */

var SHEET_ID = '1bODdvYpF5zzvHMLIkF5vcjxvsjctsvAYv9VQWQ7ZAhY';
var FOLDER_NAME = 'TwoSuns Website Leads, attachments';
var ALSO_MASTER = true;
var FALLBACK_TAB = 'Unattributed';
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

/** Sheets refuses these in a tab name, and caps the length at 100. */
function tabNameFor(campaign) {
  var n = String(campaign || '').replace(/[:\\\/\?\*\[\]]/g, ' ').trim();
  n = n.replace(/\s+/g, ' ').slice(0, 90);
  return n || FALLBACK_TAB;
}

/** A tab with the header row in place, created if this is its first lead. */
function tabByName(book, name) {
  var sheet = book.getSheetByName(name);
  if (!sheet) {
    sheet = book.insertSheet(name);
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
  }
  return sheet;
}

/** Header row present, and older nine column rows brought up to date. */
function ensureHeaders(sheet) {
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
  } else if (sheet.getLastColumn() < HEADERS.length) {
    sheet.getRange(1, HEADERS.length).setValue(HEADERS[HEADERS.length - 1]);
  }
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
    var book = SpreadsheetApp.openById(SHEET_ID);
    var p = (e && e.parameter) ? e.parameter : {};

    var attachment = '';
    if (p.attachment_name && p.attachment_b64) {
      try {
        attachment = saveAttachment(p.attachment_name, p.attachment_b64, p.name);
      } catch (err) {
        attachment = 'save failed (' + p.attachment_name + '): ' + String(err);
      }
    }

    var row = [
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
    ];

    // the master tab is the existing first sheet, whatever it is called, so the
    // history already in it stays where people expect to find it
    if (ALSO_MASTER) {
      var master = book.getSheets()[0];
      ensureHeaders(master);
      master.appendRow(row);
    }

    // routing must never cost us the lead, so it is attempted after the master
    var tab = tabNameFor(p.campaign);
    var routed = '';
    try {
      var target = tabByName(book, tab);
      if (!ALSO_MASTER || target.getSheetId() !== book.getSheets()[0].getSheetId()) {
        target.appendRow(row);
      }
      routed = tab;
    } catch (err) {
      routed = 'routing failed: ' + String(err);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true, tab: routed, attachment: !!attachment }))
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

/** Run once from the editor to prove the master write, the routing and Drive. */
function testWrite() {
  var b64 = Utilities.base64Encode('If you can open this file, attachment saving works.');
  doPost({ parameter: {
    form: 'Setup test', campaign: 'Discuss Your Needs', name: 'Test Row',
    email: 'test@twosuns.ai', company: 'TwoSuns', job_title: '',
    message: 'Delete this row from both tabs, and its attachment from Drive.',
    page: 'setup',
    attachment_name: 'attachment-check.txt', attachment_b64: b64
  }});
}
