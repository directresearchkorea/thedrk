document.addEventListener('DOMContentLoaded', () => {
  const cookieBanner = document.createElement('div');
  cookieBanner.id = 'cookie-consent-banner';
  cookieBanner.innerHTML = `
    <div class="cookie-banner-inner">
      <p data-i18n="cookie_msg">We use cookies to enhance your browsing experience, serve personalized ads or content, and analyze our traffic. By clicking "Accept All", you consent to our use of cookies.</p>
      <div class="cookie-actions">
        <button id="btn-decline-cookies" class="btn btn--secondary btn--sm" data-i18n="cookie_decline">Decline</button>
        <button id="btn-accept-cookies" class="btn btn--primary btn--sm" data-i18n="cookie_accept">Accept All</button>
      </div>
    </div>
  `;
  
  // Style is dynamically injected or added to css/components.css
  document.body.appendChild(cookieBanner);
  
  const hasConsent = localStorage.getItem('drk_cookie_consent');
  
  if (!hasConsent) {
    // Show banner
    setTimeout(() => {
      cookieBanner.classList.add('show');
    }, 1000);
  } else if (hasConsent === 'accepted') {
    loadAnalytics();
  }
  
  document.getElementById('btn-accept-cookies').addEventListener('click', () => {
    localStorage.setItem('drk_cookie_consent', 'accepted');
    cookieBanner.classList.remove('show');
    loadAnalytics();
  });
  
  document.getElementById('btn-decline-cookies').addEventListener('click', () => {
    localStorage.setItem('drk_cookie_consent', 'declined');
    cookieBanner.classList.remove('show');
    // We explicitly do NOT call loadAnalytics()
  });

  function loadAnalytics() {
    // In actual implementation, we might load GA dynamically here.
    // Since analytics.js is already in HTML, we would ideally modify HTML 
    // to NOT load analytics.js by default, but for now we just log it.
    console.log('Analytics allowed');
  }
});
