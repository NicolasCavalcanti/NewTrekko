/**
 * Trekko Analytics — Centralized tracking layer
 *
 * Architecture:
 *   - Primary channel: window.dataLayer (consumed by GTM when configured)
 *   - Fallback channel: gtag() direct calls (active GA4 script, no GTM needed)
 *   - Public API: window.TrekkoAnalytics.*
 *
 * Configuration (set in each page before this script):
 *   window.TREKKO_CONFIG = { GTM_ID: 'GTM-XXXXXXX', GA4_ID: 'G-XXXXXXXXXX', ADS_ID: 'AW-XXXXXXXXX' }
 *
 * Privacy rules enforced here:
 *   - NEVER send email, phone, CPF, CNPJ or free-form user text to analytics
 *   - Only boolean/categorical metadata is forwarded (state, city, has_cadastur, difficulty…)
 */
(function (win, doc) {
  'use strict';

  // ─── Helpers ──────────────────────────────────────────────────────────────

  win.dataLayer = win.dataLayer || [];

  var cfg = win.TREKKO_CONFIG || {};
  var hasGTM = !!cfg.GTM_ID;

  function safe(fn) {
    try { fn(); } catch (e) { /* never break the site */ }
  }

  function dlPush(obj) {
    safe(function () { win.dataLayer.push(obj); });
  }

  /**
   * Core dispatcher.
   * Skips silently when the user has not yet granted analytics consent
   * (Google Consent Mode v2 also blocks collection at the network level,
   * but we avoid filling dataLayer with events that won't be processed).
   * With GTM: pushes to dataLayer only (GTM forwards to GA4/Ads).
   * Without GTM: pushes to dataLayer AND fires gtag() directly.
   */
  function dispatch(eventName, params) {
    if (!eventName) return;
    /* honour analytics consent — window.TrekkoConsent is set in index.html */
    var consent = win.TrekkoConsent;
    if (consent && consent.has && consent.has() && !consent.analytics()) return;
    safe(function () {
      var payload = Object.assign({}, params || {});
      payload.event = eventName;
      dlPush(payload);
      if (!hasGTM && typeof win.gtag === 'function') {
        win.gtag('event', eventName, params || {});
      }
    });
  }

  // ─── Page type resolver ───────────────────────────────────────────────────

  function getPageType(path) {
    path = path || win.location.pathname;
    if (!path || path === '/') return 'home';
    if (/^\/trilha\//.test(path))                    return 'trail_detail';
    if (/^\/guia\//.test(path))                      return 'guide_detail';
    if (path === '/trilhas')                          return 'trail_listing';
    if (path === '/guias')                            return 'guide_listing';
    if (path === '/guias/ativar-perfil')              return 'guide_activation_landing';
    if (/^\/trilhas\/(sao-paulo|rio-de-janeiro|minas-gerais|espirito-santo|bahia|parana|santa-catarina|rio-grande-do-sul)/.test(path)) return 'trail_state_landing';
    if (/^\/trilhas\//.test(path))                   return 'trail_intent_landing';
    if (/^\/blog\//.test(path))                      return 'blog_detail';
    if (path === '/blog')                             return 'blog_listing';
    if (path === '/contato')                         return 'contact';
    if (path === '/sobre')                           return 'about';
    if (/\/(politica|termos|editorial)/.test(path)) return 'institutional';
    return 'other';
  }

  // ─── Public API ───────────────────────────────────────────────────────────

  /**
   * Generic event — use for one-off events not covered by named helpers.
   * @param {string} eventName  snake_case event name
   * @param {Object} [params]   additional parameters (no PII)
   */
  function trackEvent(eventName, params) {
    dispatch(eventName, params);
  }

  /**
   * Page view — call on every route change (SPA) or static page load.
   */
  function trackPageView(params) {
    safe(function () {
      var path = (params && params.page_path) || win.location.pathname;
      dispatch('page_view', {
        page_path:     path,
        page_title:    (params && params.page_title)    || doc.title,
        page_location: (params && params.page_location) || win.location.href,
        page_referrer: (params && params.page_referrer) || doc.referrer || '',
        page_type:     (params && params.page_type)     || getPageType(path),
        content_group: (params && params.content_group) || getPageType(path)
      });
    });
  }

  /** Individual trail page opened. */
  function trackTrailView(trail) {
    dispatch('trail_view', {
      trail_id:       trail.trail_id      || trail.id       || '',
      trail_slug:     trail.trail_slug    || trail.slug     || '',
      trail_name:     trail.trail_name    || trail.name     || '',
      state:          trail.state         || trail.uf        || '',
      city:           trail.city                            || '',
      region:         trail.region                         || '',
      difficulty:     trail.difficulty                     || '',
      distance_km:    trail.distance_km   || trail.distanceKm || '',
      elevation_gain: trail.elevation_gain                 || '',
      guide_required: !!(trail.guide_required || trail.guideRequired),
      page_type:      'trail_detail'
    });
  }

  /** Individual guide profile page opened. */
  function trackGuideView(guide) {
    dispatch('guide_profile_view', {
      guide_id:       guide.guide_id   || guide.id   || '',
      guide_name:     guide.guide_name || guide.name || '',
      state:          guide.state      || guide.uf   || '',
      city:           guide.city                     || '',
      regions_served: guide.regions_served || guide.regionsServed || '',
      cadastur_status: guide.cadastur_status || (guide.cadastur ? 'active' : 'none'),
      profile_status:  guide.profile_status  || guide.profileStatus || '',
      page_type:       'guide_detail'
    });
  }

  /** User clicked WhatsApp link to contact a guide. PRIMARY CONVERSION. */
  function trackWhatsappClick(data) {
    dispatch('click_whatsapp_guide', {
      guide_id:    data.guide_id   || '',
      guide_name:  data.guide_name || '',
      state:       data.state      || '',
      city:        data.city       || '',
      trail_id:    data.trail_id   || '',
      trail_name:  data.trail_name || '',
      source_page: data.source_page || win.location.pathname,
      page_type:   data.page_type   || getPageType()
    });
  }

  /** First interaction with a form (focus/input). */
  function trackFormStart(formName, extra) {
    dispatch('form_start_' + formName, Object.assign({
      form_name:   formName,
      source_page: win.location.pathname,
      page_type:   getPageType()
    }, extra || {}));
  }

  /**
   * Form submitted successfully (call ONLY after confirmed server success).
   * PRIMARY CONVERSION for guide activation.
   */
  function trackFormSubmit(formName, data) {
    dispatch('form_submit_' + formName, Object.assign({
      form_name:   formName,
      source_page: win.location.pathname,
      page_type:   getPageType()
    }, data || {}));
  }

  /** Trail search performed. */
  function trackSearch(data) {
    dispatch('search_trail', {
      search_term:   data.search_term   || '',
      state:         data.state         || '',
      city:          data.city          || '',
      difficulty:    data.difficulty    || '',
      results_count: data.results_count || 0,
      page_type:     data.page_type     || getPageType()
    });
  }

  /** User applied trail filter. */
  function trackFilter(data) {
    dispatch('filter_trails', {
      filter_type:     data.filter_type     || '',
      filter_value:    data.filter_value    || '',
      state:           data.state           || '',
      difficulty:      data.difficulty      || '',
      distance_range:  data.distance_range  || '',
      experience_type: data.experience_type || '',
      results_count:   data.results_count   || 0,
      page_type:       data.page_type       || getPageType()
    });
  }

  /** Trail card clicked in a listing or landing page. */
  function trackTrailCardClick(data) {
    dispatch('click_trail_card', {
      trail_id:    data.trail_id   || '',
      trail_name:  data.trail_name || '',
      trail_slug:  data.trail_slug || '',
      state:       data.state      || '',
      city:        data.city       || '',
      position:    data.position   || 0,
      source_page: data.source_page || win.location.pathname,
      page_type:   data.page_type   || getPageType()
    });
  }

  /** Guide card clicked. */
  function trackGuideCardClick(data) {
    dispatch('click_guide_card', {
      guide_id:       data.guide_id      || '',
      guide_name:     data.guide_name    || '',
      state:          data.state         || '',
      city:           data.city          || '',
      position:       data.position      || 0,
      profile_status: data.profile_status || '',
      source_page:    data.source_page   || win.location.pathname,
      page_type:      data.page_type     || getPageType()
    });
  }

  /** User submitted a lead request form. PRIMARY CONVERSION. */
  function trackLeadGuideRequest(data) {
    dispatch('lead_guide_request', {
      trail_id:     data.trail_id    || '',
      trail_name:   data.trail_name  || '',
      state:        data.state       || '',
      city:         data.city        || '',
      request_type: data.request_type || '',
      source_page:  data.source_page || win.location.pathname,
      page_type:    data.page_type   || getPageType()
    });
  }

  /** Guide started the signup/activation flow. Microconversion. */
  function trackGuideSignupStart(data) {
    dispatch('guide_signup_start', {
      cta_text:    data.cta_text   || '',
      source_page: data.source_page || win.location.pathname,
      page_type:   data.page_type   || getPageType()
    });
  }

  /** Guide completed activation. PRIMARY CONVERSION. */
  function trackGuideSignupComplete(data) {
    dispatch('guide_signup_complete', {
      guide_id:    data.guide_id   || '',
      state:       data.state      || '',
      city:        data.city       || '',
      has_cadastur: !!data.has_cadastur,
      source_page: data.source_page || win.location.pathname,
      page_type:   data.page_type   || getPageType()
    });
  }

  /** User saved/favourited a trail. */
  function trackSaveTrail(data) {
    dispatch('save_trail', {
      trail_id:   data.trail_id   || '',
      trail_name: data.trail_name || '',
      state:      data.state      || '',
      city:       data.city       || '',
      page_type:  data.page_type  || getPageType()
    });
  }

  // ─── Core Web Vitals (auto-initialised) ──────────────────────────────────
  // Sends LCP, CLS, INP, FCP, TTFB to GA4 as 'web_vitals' events.
  // These populate the GA4 Core Web Vitals report and feed into the linked
  // Search Console coverage once GA4 ↔ GSC integration is active.

  function initCoreWebVitals() {
    if (!win.PerformanceObserver) return;

    function sendVital(name, value) {
      var thresholds = {
        LCP:  [2500, 4000],
        CLS:  [0.1,  0.25],
        INP:  [200,  500],
        FCP:  [1800, 3000],
        TTFB: [800,  1800]
      };
      var t = thresholds[name] || [0, 0];
      var rating = value <= t[0] ? 'good' : value <= t[1] ? 'needs-improvement' : 'poor';
      dispatch('web_vitals', {
        metric_name:   name,
        metric_value:  Math.round(name === 'CLS' ? value * 1000 : value),
        metric_rating: rating,
        page_type:     getPageType(),
        page_path:     win.location.pathname
      });
    }

    // LCP — largest contentful paint
    safe(function () {
      var lcpValue = 0;
      var obs = new PerformanceObserver(function (list) {
        var entries = list.getEntries();
        lcpValue = entries[entries.length - 1].startTime;
      });
      obs.observe({ type: 'largest-contentful-paint', buffered: true });
      doc.addEventListener('visibilitychange', function () {
        if (doc.visibilityState === 'hidden') { obs.disconnect(); if (lcpValue) sendVital('LCP', lcpValue); }
      }, { once: true });
    });

    // CLS — cumulative layout shift (session-windowed per spec)
    safe(function () {
      var clsValue = 0, sessionValue = 0, sessionEntries = [];
      var obs = new PerformanceObserver(function (list) {
        list.getEntries().forEach(function (entry) {
          if (entry.hadRecentInput) return;
          var last = sessionEntries[sessionEntries.length - 1];
          var first = sessionEntries[0];
          if (sessionValue && last && entry.startTime - last.startTime < 1000
              && first && entry.startTime - first.startTime < 5000) {
            sessionValue += entry.value;
            sessionEntries.push(entry);
          } else {
            sessionValue = entry.value;
            sessionEntries = [entry];
          }
          if (sessionValue > clsValue) clsValue = sessionValue;
        });
      });
      obs.observe({ type: 'layout-shift', buffered: true });
      doc.addEventListener('visibilitychange', function () {
        if (doc.visibilityState === 'hidden') { obs.disconnect(); sendVital('CLS', clsValue); }
      }, { once: true });
    });

    // INP — interaction to next paint (replaces FID as of March 2024)
    safe(function () {
      var inpValue = 0;
      var obs = new PerformanceObserver(function (list) {
        list.getEntries().forEach(function (entry) {
          var duration = entry.duration;
          if (duration > inpValue) inpValue = duration;
        });
      });
      obs.observe({ type: 'event', durationThreshold: 16, buffered: true });
      doc.addEventListener('visibilitychange', function () {
        if (doc.visibilityState === 'hidden') { obs.disconnect(); if (inpValue) sendVital('INP', inpValue); }
      }, { once: true });
    });

    // FCP + TTFB — available after load via Performance API
    safe(function () {
      function reportPaintAndTTFB() {
        var navEntries = performance.getEntriesByType('navigation');
        if (navEntries.length) {
          var nav = navEntries[0];
          var ttfb = nav.responseStart - nav.requestStart;
          if (ttfb >= 0) sendVital('TTFB', ttfb);
        }
        performance.getEntriesByType('paint').forEach(function (entry) {
          if (entry.name === 'first-contentful-paint') sendVital('FCP', entry.startTime);
        });
      }
      if (doc.readyState === 'complete') {
        setTimeout(reportPaintAndTTFB, 0);
      } else {
        win.addEventListener('load', function () { setTimeout(reportPaintAndTTFB, 0); });
      }
    });
  }

  // ─── Scroll depth (auto-initialised) ─────────────────────────────────────

  function initScrollDepth() {
    var reached50 = false;
    var reached90 = false;
    var path = win.location.pathname;
    var pageType = getPageType(path);

    win.addEventListener('scroll', function () {
      safe(function () {
        var scrolled = win.scrollY + win.innerHeight;
        var total = doc.documentElement.scrollHeight || doc.body.scrollHeight || 1;
        var pct = scrolled / total;
        if (!reached50 && pct >= 0.5) {
          reached50 = true;
          dispatch('scroll_50', { page_type: pageType, page_path: path, content_group: pageType });
        }
        if (!reached90 && pct >= 0.9) {
          reached90 = true;
          dispatch('scroll_90', { page_type: pageType, page_path: path, content_group: pageType });
        }
      });
    }, { passive: true });
  }

  // ─── SPA routing listener ─────────────────────────────────────────────────
  // Intercepts React Router history changes to fire page_view on each navigation.

  function initSPARouting() {
    var prevPath = win.location.pathname;

    function onRouteChange() {
      safe(function () {
        var path = win.location.pathname;
        if (path === prevPath) return;
        prevPath = path;

        // Small delay lets the new page's <title> update before we read it
        setTimeout(function () {
          trackPageView({
            page_path:     path,
            page_title:    doc.title,
            page_location: win.location.href,
            page_referrer: '',
            page_type:     getPageType(path)
          });
        }, 50);
      });
    }

    var origPush    = history.pushState;
    var origReplace = history.replaceState;

    history.pushState = function () {
      origPush.apply(this, arguments);
      onRouteChange();
    };
    history.replaceState = function () {
      origReplace.apply(this, arguments);
      onRouteChange();
    };
    win.addEventListener('popstate', onRouteChange);
  }

  // ─── Bootstrap ────────────────────────────────────────────────────────────

  initCoreWebVitals();
  initScrollDepth();
  initSPARouting();

  // ─── Expose public API ────────────────────────────────────────────────────

  win.TrekkoAnalytics = {
    trackEvent:             trackEvent,
    trackPageView:          trackPageView,
    trackTrailView:         trackTrailView,
    trackGuideView:         trackGuideView,
    trackWhatsappClick:     trackWhatsappClick,
    trackFormStart:         trackFormStart,
    trackFormSubmit:        trackFormSubmit,
    trackSearch:            trackSearch,
    trackFilter:            trackFilter,
    trackTrailCardClick:    trackTrailCardClick,
    trackGuideCardClick:    trackGuideCardClick,
    trackLeadGuideRequest:  trackLeadGuideRequest,
    trackGuideSignupStart:  trackGuideSignupStart,
    trackGuideSignupComplete: trackGuideSignupComplete,
    trackSaveTrail:         trackSaveTrail,
    getPageType:            getPageType
  };

}(window, document));
