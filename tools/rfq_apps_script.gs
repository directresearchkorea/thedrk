/**
 * Direct Research Korea (DRK) - Hardened RFQ Form Handler (Google Apps Script)
 *
 * 배포 방법:
 * 1. Google Apps Script 편집기에서 기존 Code.gs 내용을 이 코드로 교체합니다.
 * 2. 우측 상단 [배포] -> [새 배포] -> 유형: 웹 앱
 *    - 다음 사용자 권한으로 실행: 나
 *    - 액세스 권한이 있는 사용자: 모든 사용자
 * 3. 새로 발급된 웹 앱 URL의 배포 ID(/s/<여기>/exec)를 복사해
 *    contact/index.html 의 DEPLOYMENT_ID 값으로 교체 후 GitHub에 푸시합니다.
 *    (기존 유출된 배포는 [배포 관리]에서 보관 처리하면 봇의 직접 POST가 완전 차단됩니다.)
 */

const RECIPIENT_EMAIL = 'YOUR_RECIPIENT_EMAIL'; // Apps Script 편집기에서 실제 수신 이메일로 설정
const EXPECTED_FORM_TOKEN = 'drk-rfq-v2-2026';
const MIN_FILL_TIME_MS = 3000;        // 3초 미만 제출은 봇으로 간주
const MAX_FILL_TIME_MS = 86400000;    // 24시간 초과 타임스탬프 무효

function doPost(e) {
  try {
    const p = (e && e.parameter) ? e.parameter : {};

    const name = String(p.name || '').trim();
    const email = String(p.email || '').trim();
    const company = String(p.company || '').trim();
    const service = String(p.service || '').trim();
    const message = String(p.message || '').trim();
    const websiteUrl = String(p.website_url || '').trim();
    const formToken = String(p._form_token || '').trim();
    const loadedAt = Number(p._loaded_at || 0);
    const interacted = String(p._interacted || '').trim();

    const spamReason = detectSpam({
      name: name,
      email: email,
      company: company,
      service: service,
      message: message,
      websiteUrl: websiteUrl,
      formToken: formToken,
      loadedAt: loadedAt,
      interacted: interacted
    });

    if (spamReason) {
      logToSheet('Spam', [new Date(), spamReason, name, email, company, service, message]);
      // 봇이 차단 사실을 눈치채지 못하도록 정상 응답 형태로 반환
      return jsonResponse({ status: 'ok' });
    }

    // 정상 문의: 시트 기록 + 이메일 발송
    logToSheet('Inquiries', [new Date(), name, email, company, service, message]);

    const subject = '[DRK Website] New RFQ Inquiry Received - ' + name;
    const body = [
      'A new RFQ inquiry has been submitted.',
      '',
      '■ Name: ' + name,
      '■ Email: ' + email,
      '■ Company/Org: ' + (company || '(Not provided)'),
      '■ Research Type: ' + (service || '(Not selected)'),
      '■ Message:',
      message
    ].join('\n');

    MailApp.sendEmail({
      to: RECIPIENT_EMAIL,
      replyTo: email,
      subject: subject,
      body: body
    });

    return jsonResponse({ status: 'ok' });
  } catch (err) {
    return jsonResponse({ status: 'error', message: String(err) });
  }
}

function detectSpam(data) {
  // 1. 공유 폼 토큰 검증 (기존 유출 URL로 직접 POST 하는 봇 즉시 차단)
  if (data.formToken !== EXPECTED_FORM_TOKEN) {
    return 'invalid_token';
  }

  // 2. 허니팟 필드 검증
  if (data.websiteUrl !== '') {
    return 'honeypot_filled';
  }

  // 3. 사용자 상호작용 및 최소 작성 시간 검증
  if (data.interacted !== '1') {
    return 'no_interaction';
  }
  const now = Date.now();
  const elapsed = now - data.loadedAt;
  if (!data.loadedAt || isNaN(elapsed) || elapsed < MIN_FILL_TIME_MS || elapsed > MAX_FILL_TIME_MS) {
    return 'invalid_elapsed_time_' + elapsed;
  }

  // 4. 필수 항목 및 엄격한 이메일 형식 검증 ("QLD" 같은 비정상 이메일 차단)
  if (!data.name || !data.message || data.message.length < 10) {
    return 'missing_or_short_fields';
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(data.email)) {
    return 'invalid_email_format';
  }
  if (data.company && data.email.toLowerCase() === data.company.toLowerCase()) {
    return 'email_equals_company';
  }

  const combinedRaw = data.name + ' ' + data.message + ' ' + data.company;
  const combinedLower = combinedRaw.toLowerCase();

  // 5. 과도한 URL 포함 (콜드메일 영업 스팸의 데모 링크 + 수신거부 링크 패턴)
  const urlMatches = data.message.match(/https?:\/\/[^\s]+/gi) || [];
  if (urlMatches.length >= 2) {
    return 'too_many_urls';
  }

  // 6. 긴 16진수 코드 문자열
  if (/[a-f0-9]{25,}/i.test(combinedLower)) {
    return 'hex_code_pattern';
  }

  // 7. 스팸 및 콜드메일 영업 키워드
  const spamKeywords = [
    'boostleadgen',
    'unsubscribe',
    'opt-out',
    'opt out',
    'rebuilt your site',
    'redesigned your website',
    'website redesign',
    'real concept around them',
    'not a mockup',
    'call me back in the next',
    'call them in about',
    'our ai, on every call',
    '14 days free',
    'no credit card',
    'seo services',
    'rank on google',
    'first page of google',
    'backlinks',
    'bitcoin',
    ' btc ',
    'crypto',
    'casino',
    'telegra.ph',
    't.me/',
    'bit.ly/',
    'cloud mining',
    'withdrawal',
    'earn money',
    'viagra',
    '투자',
    '카지노',
    '코인',
    'volia saber el seu preu'
  ];
  for (var i = 0; i < spamKeywords.length; i++) {
    if (combinedLower.indexOf(spamKeywords[i]) !== -1) {
      return 'spam_keyword:' + spamKeywords[i];
    }
  }

  // 8. Google 사칭 체크
  if (data.company.toLowerCase().indexOf('google') !== -1 && data.email.toLowerCase().indexOf('google.com') === -1) {
    return 'fake_google';
  }

  // 9. 비정상 이름 체크
  if (/[0-9]/.test(data.name) || /(.)\1{3,}/.test(data.name)) {
    return 'suspicious_name';
  }

  return null;
}

function logToSheet(sheetName, row) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) return;
    let sheet = ss.getSheetByName(sheetName);
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
    }
    sheet.appendRow(row);
  } catch (e) {
    // 바인딩된 스프레드시트가 없는 독립 스크립트인 경우 무시
  }
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
