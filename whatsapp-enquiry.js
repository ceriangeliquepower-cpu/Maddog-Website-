/* WhatsApp enquiry pop-up (28 Oct 2026).
   Every "chat on WhatsApp" link to Maddog's number first opens a short form (name, mobile, email optional, what
   they're interested in, message optional). On "Continue to WhatsApp" the details are saved as a website lead
   (type 'whatsapp' -> a New enquiry in the Admin Dashboard) and WhatsApp opens with their message typed in.
   10 Nov 2026: the form then shows "Almost done — tap Send in WhatsApp" with a "WhatsApp didn't open?" button,
   because the lead is saved before they send (some never press Send).
   Self-contained: no libraries. Include once per page: <script src="/whatsapp-enquiry.js" defer></script> */
(function () {
  'use strict';
  var NUMBER = '27634421690';
  var SUPABASE = 'https://mthjfihctiluqllpegnr.supabase.co/rest/v1/leads';
  var KEY = 'sb_publishable_VjcQHDkyEWXohoVwpDxhMw_Tu6fZBO9'; // public key (the same one the contact form uses)
  var INTERESTS = ['Free trial class', 'MMA', 'BJJ', 'Kickboxing', 'Boxing', 'Women’s Boxing', 'Wrestling', 'Rebounding', 'Kids classes',
    'Personal training', 'Recovery (sauna & ice bath)', 'Physiotherapy', 'Something else'];

  var css = '' +
    '.wae-back{box-sizing:border-box;position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.72);display:flex;align-items:center;justify-content:center;padding:16px;padding-top:max(16px,env(safe-area-inset-top));padding-bottom:max(16px,env(safe-area-inset-bottom))}' +
    '.wae{box-sizing:border-box;width:100%;max-width:440px;max-height:calc(100dvh - 32px);overflow-y:auto;background:#0F0F0F;border:1px solid rgba(201,168,76,.35);border-top:3px solid #C9A84C;color:#F5F0E8;font-family:"Barlow Condensed",sans-serif;padding:26px 22px 22px;position:relative;box-shadow:0 24px 60px rgba(0,0,0,.6)}' +
    '.wae h2{font-family:"Bebas Neue",sans-serif;font-weight:400;font-size:30px;letter-spacing:.04em;margin:0 0 4px;color:#F5F0E8}' +
    '.wae p.wae-sub{margin:0 0 16px;font-size:15px;color:rgba(245,240,232,.7);line-height:1.4}' +
    '.wae-x{position:absolute;top:10px;right:10px;width:36px;height:36px;border:0;background:none;color:rgba(245,240,232,.7);font-size:26px;line-height:1;cursor:pointer}' +
    '.wae label{display:block;font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#C9A84C;margin:12px 0 6px}' +
    '.wae input,.wae select,.wae textarea{width:100%;box-sizing:border-box;background:#080808;border:1px solid rgba(245,240,232,.18);color:#F5F0E8;font-family:"Barlow Condensed",sans-serif;font-size:16px;padding:11px 12px;border-radius:2px;-webkit-appearance:none;appearance:none}' +
    '.wae select{background-image:linear-gradient(45deg,transparent 50%,#C9A84C 50%),linear-gradient(135deg,#C9A84C 50%,transparent 50%);background-position:calc(100% - 18px) 50%,calc(100% - 13px) 50%;background-size:5px 5px;background-repeat:no-repeat;padding-right:34px}' +
    '.wae textarea{min-height:76px;resize:vertical}' +
    '.wae input:focus,.wae select:focus,.wae textarea:focus{outline:none;border-color:#C9A84C}' +
    '.wae-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}' +
    '.wae-row label{margin-top:12px}' +
    '.wae-bad{border-color:#e0705c !important}' +
    '.wae-err{color:#f3a08f;font-size:14px;margin:10px 0 0}' +
    '.wae-go{margin-top:18px;width:100%;border:0;background:#25D366;color:#fff;font-family:"Bebas Neue",sans-serif;font-size:20px;letter-spacing:.08em;padding:13px 16px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px}' +
    '.wae-go:hover{background:#1fbd5a}' +
    '.wae-go svg{width:22px;height:22px;fill:#fff}' +
    '.wae-small{font-size:12.5px;color:rgba(245,240,232,.55);margin:12px 0 0;line-height:1.45}' +
    '.wae-small a{color:#C9A84C}' +
    '.wae p.wae-sub strong{color:#F5F0E8}' +
    '.wae-done{margin-top:10px;width:100%;border:1px solid rgba(245,240,232,.25);background:none;color:#F5F0E8;font-family:"Bebas Neue",sans-serif;font-size:18px;letter-spacing:.08em;padding:11px 16px;cursor:pointer}' +
    '.wae-done:hover{border-color:#C9A84C}' +
    '.wae-trap{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}' +
    '@media(max-width:420px){.wae-row{grid-template-columns:1fr;gap:0}.wae{padding:22px 16px 18px}.wae h2{font-size:26px}}';

  var WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.69.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.42"/></svg>';

  function el(html) { var d = document.createElement('div'); d.innerHTML = html; return d.firstChild; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var lastFocus = null, back = null;

  function close() {
    if (!back) return;
    back.parentNode.removeChild(back); back = null;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function open(presetText) {
    if (back) return;
    lastFocus = document.activeElement;
    var opts = INTERESTS.map(function (i) { return '<option>' + esc(i) + '</option>'; }).join('');
    back = el('<div class="wae-back" role="dialog" aria-modal="true" aria-labelledby="wae-title">' +
      '<form class="wae" novalidate>' +
      '<button type="button" class="wae-x" aria-label="Close">×</button>' +
      '<h2 id="wae-title">Chat on WhatsApp</h2>' +
      '<p class="wae-sub">Tell us a little about you, then we’ll open WhatsApp with your message ready to send.</p>' +
      '<div class="wae-row"><div><label for="wae-first">First name</label><input id="wae-first" name="first_name" autocomplete="given-name" required></div>' +
      '<div><label for="wae-last">Surname</label><input id="wae-last" name="last_name" autocomplete="family-name" required></div></div>' +
      '<label for="wae-phone">Mobile number</label><input id="wae-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="e.g. 082 123 4567" required>' +
      '<label for="wae-email">Email (optional)</label><input id="wae-email" name="email" type="email" autocomplete="email">' +
      '<label for="wae-interest">I’m interested in</label><select id="wae-interest" name="interest" required><option value="">Choose…</option>' + opts + '</select>' +
      '<label for="wae-msg">Your message (optional)</label><textarea id="wae-msg" name="message" placeholder="Anything you’d like to ask?"></textarea>' +
      '<input class="wae-trap" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<p class="wae-err" role="alert" hidden></p>' +
      '<button type="submit" class="wae-go">' + WA_ICON + 'Continue to WhatsApp</button>' +
      '<p class="wae-small">We save your details so our team can reply to you and follow up. See our <a href="/privacy-policy.html" target="_blank" rel="noopener">privacy policy</a>.</p>' +
      '</form></div>');
    document.body.appendChild(back);
    document.body.style.overflow = 'hidden';
    var form = back.querySelector('form');
    if (presetText) form.message.value = presetText;
    back.addEventListener('click', function (e) { if (e.target === back) close(); });
    back.querySelector('.wae-x').addEventListener('click', close);
    form.addEventListener('submit', function (e) { e.preventDefault(); send(form); });
    setTimeout(function () { form.first_name.focus(); }, 30);
  }

  function send(form) {
    var v = function (n) { return (form[n].value || '').trim(); };
    var missing = [];
    [['first_name', 'first name'], ['last_name', 'surname'], ['phone', 'mobile number'], ['interest', 'what you’re interested in']].forEach(function (f) {
      var bad = !v(f[0]) || (f[0] === 'phone' && v('phone').replace(/\D/g, '').length < 9);
      form[f[0]].classList.toggle('wae-bad', bad);
      if (bad) missing.push(f[1]);
    });
    var email = v('email');
    var emailBad = email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
    form.email.classList.toggle('wae-bad', !!emailBad);
    if (emailBad) missing.push('a valid email (or leave it empty)');
    var err = form.querySelector('.wae-err');
    if (missing.length) { err.textContent = 'Please add your ' + missing.join(', ') + '.'; err.hidden = false; return; }
    err.hidden = true;

    var text = 'Hi Maddog, I’m ' + v('first_name') + ' ' + v('last_name') + '. I’m interested in ' + v('interest') + '.' + (v('message') ? ' ' + v('message') : '');
    var url = 'https://wa.me/' + NUMBER + '?text=' + encodeURIComponent(text);

    // Save the enquiry (keepalive: it still goes through while WhatsApp opens). Robots fill the hidden box: skip them.
    if (!v('website')) {
      try {
        fetch(SUPABASE, {
          method: 'POST', keepalive: true,
          headers: { apikey: KEY, Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
          body: JSON.stringify({ type: 'whatsapp', first_name: v('first_name'), last_name: v('last_name'), phone: v('phone'), email: email || null,
            interest: v('interest'), message: v('message') || null, source: 'website_whatsapp' })
        }).catch(function () {});
      } catch (e) { /* never block WhatsApp */ }
      try { if (window.gtag) window.gtag('event', 'generate_lead', { method: 'whatsapp_form' }); } catch (e) { /* analytics optional */ }
    }
    // The lead is saved, but the message only reaches Maddog once they tap Send in WhatsApp: say so, and keep a
    // button in case WhatsApp didn't open (pop-up blocked, WhatsApp Web not signed in). It stays when they come back.
    done(url, v('first_name'));
    openWhatsApp(url);
  }

  // Phones: open WhatsApp in the same tab (the app takes over); computers: a new tab for WhatsApp Web / Desktop
  function openWhatsApp(url) {
    if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) window.location.href = url;
    else window.open(url, '_blank', 'noopener');
  }

  function done(url, name) {
    var box = back.querySelector('.wae');
    box.innerHTML =
      '<button type="button" class="wae-x" aria-label="Close">×</button>' +
      '<h2 id="wae-title">Almost done, ' + esc(name) + '</h2>' +
      '<p class="wae-sub">Your message is typed in WhatsApp. <strong>Tap Send in WhatsApp</strong> so it reaches us.</p>' +
      '<button type="button" class="wae-go wae-again">' + WA_ICON + 'WhatsApp didn’t open? Tap here</button>' +
      '<button type="button" class="wae-done">Done</button>' +
      '<p class="wae-small">No WhatsApp? We have your number and will contact you, or call us on <a href="tel:+27634421690">063 442 1690</a>.</p>';
    box.querySelector('.wae-x').addEventListener('click', close);
    box.querySelector('.wae-done').addEventListener('click', close);
    box.querySelector('.wae-again').addEventListener('click', function () { openWhatsApp(url); });
    box.querySelector('.wae-again').focus();
  }

  function init() {
    if (!document.getElementById('wae-css')) { var s = document.createElement('style'); s.id = 'wae-css'; s.textContent = css; document.head.appendChild(s); }
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href*="wa.me/' + NUMBER + '"], a[href*="api.whatsapp.com/send?phone=' + NUMBER + '"]');
      if (!a || e.ctrlKey || e.metaKey || e.shiftKey) return;
      e.preventDefault();
      var m = (a.getAttribute('href') || '').match(/[?&]text=([^&]+)/);
      open(m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '');
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
