document.addEventListener('DOMContentLoaded', () => {
  const defaultLang = 'en';
  const supportedLangs = ['en', 'ko', 'ja', 'zh'];
  
  // Initialize Language
  initLanguage();

  function initLanguage() {
    let savedLang = localStorage.getItem('drk_lang');
    
    if (savedLang && supportedLangs.includes(savedLang)) {
      applyLanguage(savedLang);
    } else {
      detectLocationAndSetLang();
    }
    
    // Bind switcher
    const switcher = document.getElementById('lang-switcher');
    if (switcher) {
      switcher.addEventListener('change', (e) => {
        const newLang = e.target.value;
        localStorage.setItem('drk_lang', newLang);
        applyLanguage(newLang);
      });
    }
  }

  async function detectLocationAndSetLang() {
    try {
      // Free IP geolocation
      const response = await fetch('https://ipapi.co/json/');
      if (response.ok) {
        const data = await response.json();
        const country = data.country_code; // e.g. KR, JP, CN
        
        let detectedLang = defaultLang;
        if (country === 'KR') detectedLang = 'ko';
        else if (country === 'JP') detectedLang = 'ja';
        else if (country === 'CN' || country === 'TW' || country === 'HK') detectedLang = 'zh';
        
        localStorage.setItem('drk_lang', detectedLang);
        applyLanguage(detectedLang);
        return;
      }
    } catch (e) {
      console.warn('IP detection failed, falling back to browser language');
    }
    
    // Fallback to browser language
    const browserLang = navigator.language.slice(0, 2);
    let finalLang = supportedLangs.includes(browserLang) ? browserLang : defaultLang;
    localStorage.setItem('drk_lang', finalLang);
    applyLanguage(finalLang);
  }

  function applyLanguage(lang) {
    if (!translations[lang]) return;
    
    const dict = translations[lang];
    document.documentElement.lang = lang;
    
    // Update elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        // If it's HTML, we need to use innerHTML (e.g. for hero_title)
        if (dict[key].includes('<')) {
          el.innerHTML = dict[key];
        } else {
          el.textContent = dict[key];
        }
      }
    });
    
    // Update switcher select if exists
    const switcher = document.getElementById('lang-switcher');
    if (switcher) {
      switcher.value = lang;
    }
  }
});
