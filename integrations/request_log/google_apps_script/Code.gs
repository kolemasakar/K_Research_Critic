const SPREADSHEET_ID = '1icDvAkPx43s7568iZkANBCriz8UaanB4kMITO-icLaU';
const SHEET_NAME = 'Звернення';
const TIME_ZONE = 'Europe/Kyiv';

function doGet() {
  return jsonResponse_({ ok: true, service: 'krc-request-log', status: 'ready' });
}

function doPost(e) {
  try {
    const payload = parsePayload_(e);
    const topic = normalizeTopic_(payload.topic);
    if (!topic) {
      return jsonResponse_({ ok: false, error: 'topic_required' });
    }

    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_NAME);
      if (!sheet) {
        throw new Error('sheet_not_found');
      }

      const requestNumber = Math.max(1, sheet.getLastRow());
      const now = new Date();
      const date = Utilities.formatDate(now, TIME_ZONE, 'dd.MM.yyyy');
      const time = Utilities.formatDate(now, TIME_ZONE, 'HH:mm:ss');

      sheet.appendRow([
        requestNumber,
        date,
        time,
        'none',
        topic,
      ]);

      return jsonResponse_({
        ok: true,
        request_number: requestNumber,
        date: date,
        time: time,
        user_name: 'none',
        request_topic: topic,
      });
    } finally {
      lock.releaseLock();
    }
  } catch (err) {
    return jsonResponse_({ ok: false, error: String(err && err.message ? err.message : err) });
  }
}

function parsePayload_(e) {
  if (!e || !e.postData || !e.postData.contents) return {};
  try {
    return JSON.parse(e.postData.contents);
  } catch (err) {
    return {};
  }
}

function normalizeTopic_(value) {
  if (typeof value !== 'string') return '';
  return value.replace(/\s+/g, ' ').trim().slice(0, 160);
}

function jsonResponse_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
