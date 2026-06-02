/**
 * Trekko LGPD Consent — shared script for standalone static pages.
 *
 * Must be loaded synchronously (no defer/async) BEFORE any GA4/Ads scripts
 * so Consent Mode v2 defaults are applied before measurement fires.
 *
 * Responsibilities:
 *  1. Read persisted consent from localStorage (12-month TTL)
 *  2. Apply Consent Mode v2 defaults (denied until user chooses)
 *  3. Conditionally load GA4
 *  4. Render the consent banner if no prior choice exists
 */
(function () {
  'use strict';

  /* ── 1. Read persisted consent ── */
  var KEY = 'trekko_lgpd_consent';
  var stored = null;
  try {
    var raw = localStorage.getItem(KEY);
    if (raw) {
      var parsed = JSON.parse(raw);
      var TWELVE_MONTHS_MS = 365 * 24 * 60 * 60 * 1000;
      if (parsed && parsed.ts && (Date.now() - new Date(parsed.ts).getTime()) < TWELVE_MONTHS_MS) {
        stored = parsed;
      } else {
        localStorage.removeItem(KEY);
      }
    }
  } catch (e) {}

  /* ── 2. Consent state API ── */
  window.TrekkoConsent = {
    _state: stored,
    has: function () { return !!this._state; },
    analytics: function () { return !!(this._state && this._state.analytics); },
    ads: function () { return !!(this._state && this._state.ads); },
    save: function (analytics, ads) {
      this._state = { analytics: !!analytics, ads: !!ads, ts: new Date().toISOString() };
      try { localStorage.setItem(KEY, JSON.stringify(this._state)); } catch (e) {}
    }
  };

  /* ── 3. Consent Mode v2 defaults ── */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  var analyticsStorage = stored && stored.analytics ? 'granted' : 'denied';
  var adStorage        = stored && stored.ads       ? 'granted' : 'denied';
  gtag('consent', 'default', {
    analytics_storage:  analyticsStorage,
    ad_storage:         adStorage,
    ad_user_data:       adStorage,
    ad_personalization: adStorage,
    wait_for_update:    stored ? 0 : 500
  });

  /* ── 4. Consent update helper (called by banner) ── */
  window._trekkoApplyConsent = function (analytics, ads) {
    window.TrekkoConsent.save(analytics, ads);
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        analytics_storage:  analytics ? 'granted' : 'denied',
        ad_storage:         ads       ? 'granted' : 'denied',
        ad_user_data:       ads       ? 'granted' : 'denied',
        ad_personalization: ads       ? 'granted' : 'denied'
      });
    }
  };

  /* ── 5. Conditionally load GA4 ── */
  var cfg = window.TREKKO_CONFIG || {};
  var ga4Id = cfg.GA4_ID || 'G-S816P190VN';

  function loadGA4() {
    if (window._ga4Loaded) return;
    window._ga4Loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ga4Id;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtagInner() { window.dataLayer.push(arguments); }
    window.gtag = window.gtag || gtagInner;
    window.gtag('js', new Date());
    window.gtag('config', ga4Id, { send_page_view: true });
  }

  if (stored && stored.analytics) {
    loadGA4();
  } else {
    var origApply = window._trekkoApplyConsent;
    window._trekkoApplyConsent = function (analytics, ads) {
      if (typeof origApply === 'function') origApply(analytics, ads);
      if (analytics) loadGA4();
    };
  }

  /* ── 6. Inject banner styles + HTML if no consent yet ── */
  if (stored) return; /* user already chose — no banner needed */

  var style = document.createElement('style');
  style.textContent = [
    '#trekko-consent-wrap*,#trekko-consent-wrap*::before,#trekko-consent-wrap*::after{box-sizing:border-box;margin:0;padding:0}',
    '#trekko-consent-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:99998;display:none}',
    '#trekko-consent-wrap{position:fixed;bottom:0;left:0;right:0;z-index:99999;font-family:"Inter",system-ui,sans-serif;font-size:14px;line-height:1.5;color:#1a1a19}',
    '#trekko-consent-banner{background:#fff;border-top:3px solid #2D6A4F;box-shadow:0 -4px 24px rgba(0,0,0,.12);padding:20px 24px;display:none}',
    '#trekko-consent-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;gap:24px;flex-wrap:wrap}',
    '.trekko-consent-text{flex:1 1 280px}',
    '.trekko-consent-text strong{font-size:15px;color:#0d542b;display:block;margin-bottom:4px}',
    '.trekko-consent-text p{color:#34322d;font-size:13px}',
    '.trekko-consent-text a{color:#2D6A4F;text-decoration:underline}',
    '.trekko-consent-btns{display:flex;gap:10px;flex-wrap:wrap;align-items:center;flex-shrink:0}',
    '.trekko-consent-btns button{cursor:pointer;border-radius:8px;font-size:13px;font-weight:600;padding:9px 18px;border:none;transition:opacity .15s;white-space:nowrap}',
    '.trekko-consent-btns button:hover{opacity:.85}',
    '#trekko-btn-accept{background:#2D6A4F;color:#fff}',
    '#trekko-btn-reject{background:#f8f8f7;color:#1a1a19;border:1px solid #ccc}',
    '#trekko-btn-custom{background:transparent;color:#2D6A4F;text-decoration:underline;font-weight:500;padding:9px 4px}',
    '#trekko-consent-settings{background:#fff;border-top:3px solid #2D6A4F;box-shadow:0 -4px 24px rgba(0,0,0,.15);padding:24px;display:none;max-height:80vh;overflow-y:auto}',
    '#trekko-consent-settings h3{font-size:16px;font-weight:700;color:#0d542b;margin-bottom:16px}',
    '.trekko-pref-row{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px solid #f0f0ee}',
    '.trekko-pref-row:last-of-type{border-bottom:none}',
    '.trekko-pref-info strong{font-size:14px;color:#1a1a19;display:block;margin-bottom:2px}',
    '.trekko-pref-info p{font-size:12px;color:#858481}',
    '.trekko-always-on{font-size:11px;font-weight:600;color:#258651;background:#e8f5ee;padding:4px 10px;border-radius:20px;white-space:nowrap;flex-shrink:0;margin-top:2px}',
    '.trekko-toggle{position:relative;display:inline-block;width:44px;height:24px;flex-shrink:0;cursor:pointer}',
    '.trekko-toggle input{opacity:0;width:0;height:0}',
    '.trekko-slider{position:absolute;inset:0;background:#ccc;border-radius:24px;transition:background .2s}',
    '.trekko-slider::before{content:"";position:absolute;width:18px;height:18px;left:3px;top:3px;background:#fff;border-radius:50%;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.2)}',
    '.trekko-toggle input:checked+.trekko-slider{background:#2D6A4F}',
    '.trekko-toggle input:checked+.trekko-slider::before{transform:translateX(20px)}',
    '.trekko-settings-btns{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}',
    '#trekko-btn-save{background:#2D6A4F;color:#fff;border:none;border-radius:8px;font-size:13px;font-weight:600;padding:10px 22px;cursor:pointer;transition:opacity .15s}',
    '#trekko-btn-save:hover{opacity:.85}',
    '#trekko-btn-back{background:transparent;color:#2D6A4F;border:1px solid #2D6A4F;border-radius:8px;font-size:13px;font-weight:600;padding:10px 18px;cursor:pointer;transition:opacity .15s}',
    '#trekko-btn-back:hover{opacity:.75}',
    '@media(max-width:600px){#trekko-consent-inner{flex-direction:column;align-items:stretch}.trekko-consent-btns{justify-content:stretch}.trekko-consent-btns button{flex:1;text-align:center}#trekko-btn-custom{flex:100%;text-align:center}}'
  ].join('');
  document.head.appendChild(style);

  function injectBanner() {
    var overlay = document.createElement('div');
    overlay.id = 'trekko-consent-overlay';
    overlay.setAttribute('aria-hidden', 'true');

    var wrap = document.createElement('div');
    wrap.id = 'trekko-consent-wrap';
    wrap.innerHTML = [
      '<div id="trekko-consent-banner" role="dialog" aria-modal="true" aria-label="Preferências de privacidade e cookies">',
        '<div id="trekko-consent-inner">',
          '<div class="trekko-consent-text">',
            '<strong>Sua privacidade importa</strong>',
            '<p>Usamos cookies para analytics e personalização de anúncios, em conformidade com a LGPD. Saiba mais em nossa <a href="/politica-de-cookies" target="_blank" rel="noopener">Política de Cookies</a>. Você tem controle total sobre suas preferências.</p>',
          '</div>',
          '<div class="trekko-consent-btns">',
            '<button id="trekko-btn-custom" type="button">Gerenciar preferências</button>',
            '<button id="trekko-btn-reject" type="button">Recusar não essenciais</button>',
            '<button id="trekko-btn-accept" type="button">Aceitar todos</button>',
          '</div>',
        '</div>',
      '</div>',
      '<div id="trekko-consent-settings" role="dialog" aria-modal="true" aria-label="Configurar cookies">',
        '<h3>Configurar cookies</h3>',
        '<div class="trekko-pref-row">',
          '<div class="trekko-pref-info"><strong>Essenciais</strong><p>Necessários para o funcionamento do site. Não podem ser desativados.</p></div>',
          '<span class="trekko-always-on" aria-label="Sempre ativo">Sempre ativo</span>',
        '</div>',
        '<div class="trekko-pref-row">',
          '<div class="trekko-pref-info"><strong>Analytics (GA4)</strong><p>Dados anônimos sobre uso do site para melhorarmos a experiência.</p></div>',
          '<label class="trekko-toggle" aria-label="Ativar Analytics"><input type="checkbox" id="trekko-chk-analytics"><span class="trekko-slider"></span></label>',
        '</div>',
        '<div class="trekko-pref-row">',
          '<div class="trekko-pref-info"><strong>Publicidade (Google Ads)</strong><p>Permitem exibir anúncios relevantes e medir conversões de campanhas.</p></div>',
          '<label class="trekko-toggle" aria-label="Ativar Publicidade"><input type="checkbox" id="trekko-chk-ads"><span class="trekko-slider"></span></label>',
        '</div>',
        '<div class="trekko-settings-btns">',
          '<button id="trekko-btn-back" type="button">← Voltar</button>',
          '<button id="trekko-btn-save" type="button">Salvar preferências</button>',
        '</div>',
      '</div>'
    ].join('');

    document.body.appendChild(overlay);
    document.body.appendChild(wrap);

    var bannerEl   = document.getElementById('trekko-consent-banner');
    var settingsEl = document.getElementById('trekko-consent-settings');
    var chkAnalytics = document.getElementById('trekko-chk-analytics');
    var chkAds       = document.getElementById('trekko-chk-ads');

    function showBanner() {
      bannerEl.style.display   = 'block';
      overlay.style.display    = 'none';
      settingsEl.style.display = 'none';
    }

    function showSettings() {
      chkAnalytics.checked     = true;
      chkAds.checked           = true;
      bannerEl.style.display   = 'none';
      settingsEl.style.display = 'block';
      overlay.style.display    = 'block';
    }

    function applyAndClose(analytics, ads) {
      if (typeof window._trekkoApplyConsent === 'function') {
        window._trekkoApplyConsent(analytics, ads);
      }
      bannerEl.style.display   = 'none';
      settingsEl.style.display = 'none';
      overlay.style.display    = 'none';
    }

    document.getElementById('trekko-btn-accept').addEventListener('click', function () { applyAndClose(true, true); });
    document.getElementById('trekko-btn-reject').addEventListener('click', function () { applyAndClose(false, false); });
    document.getElementById('trekko-btn-custom').addEventListener('click', showSettings);
    document.getElementById('trekko-btn-back').addEventListener('click', showBanner);
    document.getElementById('trekko-btn-save').addEventListener('click', function () { applyAndClose(chkAnalytics.checked, chkAds.checked); });

    setTimeout(showBanner, 600);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBanner);
  } else {
    injectBanner();
  }
})();
