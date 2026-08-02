(function() {
  const ICAL_URLS = [
    'https://calendar.google.com/calendar/ical/[구글계정1]%40gmail.com/public/basic.ics',
    'https://calendar.google.com/calendar/ical/[구글계정2]%40gmail.com/public/basic.ics'
  ];
  
  const PROXY_URL = 'https://api.allorigins.win/raw?url=';
  let activeEvent = null;
  let updateInterval;
  let fetchInterval;
  
  function updateClockAndStatus() {
    const badges = document.querySelectorAll('.status-badge');
    if (!badges.length) return;
    
    const now = new Date();
    
    // KST Time string
    const timeString = new Intl.DateTimeFormat('en-US', {
      timeZone: 'Asia/Seoul',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    }).format(now);
    
    const kstNow = new Date(now.toLocaleString("en-US", { timeZone: "Asia/Seoul" }));
    const kstHour = kstNow.getHours();
    const kstMinute = kstNow.getMinutes();
    const kstMonth = kstNow.getMonth() + 1;
    const kstDate = kstNow.getDate();
    const kstDay = kstNow.getDay(); // 0=Sun, 6=Sat
    
    // Determine status
    let statusColor = 'green';
    let statusText = 'Available';
    
    // 1. Ongoing Event
    if (activeEvent) {
      statusColor = 'red';
      statusText = 'In a Meeting'; // activeEvent.title could also be used here
    } else {
      // 2. Holidays & Weekends
      const isWeekend = (kstDay === 0 || kstDay === 6);
      const isHoliday = checkKoreanHoliday(kstMonth, kstDate);
      
      if (isWeekend || isHoliday) {
        statusColor = 'orange';
        statusText = 'Off Duty';
      } else {
        // Weekdays
        const timeValue = kstHour + kstMinute / 60;
        
        if (timeValue >= 23 || timeValue < 8) {
          statusColor = 'orange';
          statusText = 'Sleeping';
        } else if (timeValue >= 8 && timeValue < 10) {
          statusColor = 'orange';
          statusText = 'Getting Ready';
        } else if (timeValue >= 10 && timeValue <= 18.5) { // 18.5 is 18:30
          statusColor = 'green';
          statusText = 'Working';
        } else {
          statusColor = 'green';
          statusText = 'Available';
        }
      }
    }
    
    badges.forEach(badge => {
      const dot = badge.querySelector('.status-dot');
      const timeEl = badge.querySelector('.status-time');
      const textEl = badge.querySelector('.status-text');
      
      if (dot) dot.setAttribute('data-status', statusColor);
      if (timeEl) timeEl.textContent = `KST ${timeString}`;
      if (textEl) textEl.textContent = `(${statusText})`;
    });
  }
  
  function checkKoreanHoliday(month, date) {
    const holidays = {
      '1-1': true,   // 신정
      '3-1': true,   // 삼일절
      '5-5': true,   // 어린이날
      '6-6': true,   // 현충일
      '8-15': true,  // 광복절
      '10-3': true,  // 개천절
      '10-9': true,  // 한글날
      '12-25': true  // 성탄절
    };
    return !!holidays[`${month}-${date}`];
  }
  
  async function fetchCalendar() {
    let currentEvent = null;
    const now = new Date();
    
    for (const url of ICAL_URLS) {
      try {
        if(url.includes('[구글계정')) continue; // Skip placeholder
        
        let response = await fetch(url).catch(() => null);
        if (!response || !response.ok) {
          response = await fetch(PROXY_URL + encodeURIComponent(url));
        }
        
        if (response && response.ok) {
          let text = '';
          if (response.url.includes('allorigins.win')) {
            const json = await response.json();
            text = json.contents;
          } else {
            text = await response.text();
          }
          
          const events = parseICal(text);
          
          for (const ev of events) {
            if (ev.start <= now && now <= ev.end) {
              currentEvent = ev;
              break;
            }
          }
        }
      } catch (e) {
        console.error('Failed to fetch calendar:', e);
      }
      
      if (currentEvent) break;
    }
    
    activeEvent = currentEvent;
    updateClockAndStatus();
  }
  
  function parseICal(icsData) {
    const lines = icsData.split(/\r\n|\n|\r/);
    const events = [];
    let currentEvent = null;
    
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];
      // Handle folded lines
      while (i + 1 < lines.length && (lines[i+1].startsWith(' ') || lines[i+1].startsWith('\t'))) {
        i++;
        line += lines[i].substring(1);
      }
      
      if (line.startsWith('BEGIN:VEVENT')) {
        currentEvent = {};
      } else if (line.startsWith('END:VEVENT') && currentEvent) {
        if (currentEvent.start && currentEvent.end) {
          events.push(currentEvent);
        }
        currentEvent = null;
      } else if (currentEvent) {
        if (line.startsWith('DTSTART')) {
          currentEvent.start = parseICalDate(line);
        } else if (line.startsWith('DTEND')) {
          currentEvent.end = parseICalDate(line);
        } else if (line.startsWith('SUMMARY:')) {
          currentEvent.title = line.substring(8);
        }
      }
    }
    return events;
  }
  
  function parseICalDate(line) {
    const valueStr = line.split(':')[1];
    if (!valueStr) return new Date();
    
    const value = valueStr.trim();
    if (value.length === 8) {
      // YYYYMMDD
      const y = parseInt(value.substring(0,4), 10);
      const m = parseInt(value.substring(4,6), 10) - 1;
      const d = parseInt(value.substring(6,8), 10);
      
      return new Date(y, m, d);
    }
    
    // YYYYMMDDTHHMMSSZ or YYYYMMDDTHHMMSS
    if (value.length >= 15) {
      const y = parseInt(value.substring(0,4), 10);
      const m = parseInt(value.substring(4,6), 10) - 1;
      const d = parseInt(value.substring(6,8), 10);
      const h = parseInt(value.substring(9,11), 10);
      const min = parseInt(value.substring(11,13), 10);
      const s = parseInt(value.substring(13,15), 10);
      
      if (value.endsWith('Z')) {
        return new Date(Date.UTC(y, m, d, h, min, s));
      } else {
        return new Date(y, m, d, h, min, s);
      }
    }
    return new Date();
  }

  // Initialization
  function init() {
    updateClockAndStatus();
    fetchCalendar();
    
    updateInterval = setInterval(updateClockAndStatus, 1000);
    fetchInterval = setInterval(fetchCalendar, 5 * 60 * 1000);
  }
  
  function cleanup() {
    if (updateInterval) clearInterval(updateInterval);
    if (fetchInterval) clearInterval(fetchInterval);
  }
  
  window.addEventListener('beforeunload', cleanup);
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
