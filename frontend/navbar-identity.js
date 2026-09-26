// navbar-identity.js — shared admin identity for the navbar.
// Requires config.js (API_BASE) to be loaded first, and a
// <span id="navUser">Loading...</span> placeholder already in the DOM.
// Populates it with the real logged-in admin's name and redirects to
// login if the session is missing, expired, or not an admin.
// Also wires up a real logout (POST /auth/logout) on #logoutLink, if present,
// so the session cookie is actually cleared instead of just navigating away.
(function () {
  async function loadNavAdminName() {
    const el = document.getElementById('navUser');
    if (!el) return;
    try {
      const response = await fetch(`${API_BASE}/api/v1/auth/me`, { credentials: 'include' });
      if (!response.ok) throw new Error(`auth/me returned ${response.status}`);
      const me = await response.json();
      if (me.user.role !== 'ADMIN') {
        window.location.href = 'login.html';
        return;
      }
      const admin = me.admin || {};
      el.textContent = `${admin.first_name || ''} ${admin.last_name || ''}`.trim() || me.user.email;
    } catch (err) {
      window.location.href = 'login.html';
    }
  }

  function wireLogout() {
    const link = document.getElementById('logoutLink');
    if (!link) return;
    link.addEventListener('click', async function (e) {
      e.preventDefault();
      try {
        await fetch(`${API_BASE}/api/v1/auth/logout`, { method: 'POST', credentials: 'include' });
      } catch (err) {
        console.error('Logout request failed:', err);
      }
      window.location.href = 'login.html';
    });
  }

  loadNavAdminName();
  wireLogout();
})();
