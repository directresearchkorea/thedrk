/* ============================================
   Direct Research Korea — Analytics
   GA4 + Custom Event Tracking
   ============================================ */

// --- GA4 Configuration ---
// Replace 'G-XXXXXXXXXX' with your actual GA4 Measurement ID
const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';

// Load Google Analytics
(function() {
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_MEASUREMENT_ID, {
    'send_page_view': true,
    'cookie_flags': 'SameSite=None;Secure'
  });
})();

// --- Custom Event Tracking ---

document.addEventListener('DOMContentLoaded', () => {

  // 1. CTA Button Click Tracking
  document.querySelectorAll('[data-track-cta]').forEach(btn => {
    btn.addEventListener('click', () => {
      const ctaName = btn.getAttribute('data-track-cta');
      gtag('event', 'cta_click', {
        'event_category': 'engagement',
        'event_label': ctaName,
        'cta_name': ctaName,
        'page_location': window.location.href
      });
    });
  });

  // 2. Scroll Depth Tracking
  const scrollDepths = [25, 50, 75, 100];
  const trackedDepths = new Set();

  window.addEventListener('scroll', () => {
    const scrollPercent = Math.round(
      (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
    );

    scrollDepths.forEach(depth => {
      if (scrollPercent >= depth && !trackedDepths.has(depth)) {
        trackedDepths.add(depth);
        gtag('event', 'scroll_depth', {
          'event_category': 'engagement',
          'event_label': `${depth}%`,
          'percent_scrolled': depth,
          'page_location': window.location.href
        });
      }
    });
  }, { passive: true });

  // 3. Blog Post Read Time Tracking
  if (document.querySelector('[data-track-readtime]')) {
    const startTime = Date.now();
    
    window.addEventListener('beforeunload', () => {
      const timeSpent = Math.round((Date.now() - startTime) / 1000);
      const postTitle = document.querySelector('h1')?.textContent || 'Unknown';
      
      // Use sendBeacon for reliable tracking on page exit
      const data = JSON.stringify([{
        name: 'read_time',
        params: {
          event_category: 'content',
          event_label: postTitle,
          time_seconds: timeSpent,
          page_location: window.location.href
        }
      }]);
      
      navigator.sendBeacon(
        `https://www.google-analytics.com/mp/collect?measurement_id=${GA_MEASUREMENT_ID}&api_secret=YOUR_API_SECRET`,
        data
      );
    });
  }

  // 4. Outbound Link Click Tracking
  document.querySelectorAll('a[href^="http"]').forEach(link => {
    const url = new URL(link.href);
    if (url.hostname !== window.location.hostname) {
      link.addEventListener('click', () => {
        gtag('event', 'outbound_click', {
          'event_category': 'engagement',
          'event_label': link.href,
          'link_url': link.href,
          'link_text': link.textContent.trim()
        });
      });
    }
  });

  // 5. Form Submission Tracking
  document.querySelectorAll('form[data-track-form]').forEach(form => {
    form.addEventListener('submit', () => {
      const formName = form.getAttribute('data-track-form');
      gtag('event', 'form_submit', {
        'event_category': 'conversion',
        'event_label': formName,
        'form_name': formName
      });
    });
  });

  // 6. Category Filter Click Tracking
  document.querySelectorAll('[data-track-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const filterName = btn.getAttribute('data-track-filter');
      gtag('event', 'filter_click', {
        'event_category': 'engagement',
        'event_label': filterName,
        'filter_name': filterName
      });
    });
  });

  // 7. Insight Card Click Tracking
  document.querySelectorAll('[data-track-insight]').forEach(card => {
    card.addEventListener('click', () => {
      const insightTitle = card.getAttribute('data-track-insight');
      gtag('event', 'insight_click', {
        'event_category': 'content',
        'event_label': insightTitle,
        'insight_title': insightTitle
      });
    });
  });
});

// --- Performance Monitoring ---
if ('PerformanceObserver' in window) {
  // Track Core Web Vitals
  const observer = new PerformanceObserver((list) => {
    list.getEntries().forEach(entry => {
      gtag('event', 'web_vitals', {
        'event_category': 'performance',
        'event_label': entry.name,
        'metric_name': entry.name,
        'metric_value': Math.round(entry.startTime),
        'non_interaction': true
      });
    });
  });
  
  observer.observe({ type: 'paint', buffered: true });
}
