document.addEventListener('DOMContentLoaded', () => {
  // If already logged in, redirect
  const user = JSON.parse(localStorage.getItem('careerfit_user') || 'null');
  if (user) window.location.href = 'dashboard.html';

  const loginTab = document.getElementById('loginTab');
  const signupTab = document.getElementById('signupTab');
  const loginForm = document.getElementById('loginForm');
  const signupForm = document.getElementById('signupForm');
  const loginError = document.getElementById('loginError');
  const signupError = document.getElementById('signupError');
  const signupSuccess = document.getElementById('signupSuccess');

  // Tab switching
  loginTab.addEventListener('click', () => {
    loginTab.classList.add('active');
    signupTab.classList.remove('active');
    loginForm.classList.add('active');
    signupForm.classList.remove('active');
    clearMessages();
  });

  signupTab.addEventListener('click', () => {
    signupTab.classList.add('active');
    loginTab.classList.remove('active');
    signupForm.classList.add('active');
    loginForm.classList.remove('active');
    clearMessages();
  });

  function clearMessages() {
    [loginError, signupError, signupSuccess].forEach(el => {
      if (el) { el.style.display = 'none'; el.textContent = ''; }
    });
  }

  function showError(el, msg) {
    el.textContent = msg;
    el.style.display = 'block';
    el.classList.add('shake');
    setTimeout(() => el.classList.remove('shake'), 600);
  }

  function showSuccess(el, msg) {
    el.textContent = msg;
    el.style.display = 'block';
  }

  function setLoading(btn, loading) {
    if (loading) {
      btn.disabled = true;
      btn.dataset.original = btn.textContent;
      btn.innerHTML = '<span class="spinner"></span> Processing...';
    } else {
      btn.disabled = false;
      btn.textContent = btn.dataset.original || 'Submit';
    }
  }

  // Login
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessages();
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const btn = loginForm.querySelector('button[type="submit"]');

    if (!email || !password) return showError(loginError, 'Please fill all fields');

    setLoading(btn, true);
    try {
      const data = await window.CareerFitAPI.login(email, password);
      localStorage.setItem('careerfit_user', JSON.stringify(data.user));
      window.location.href = 'dashboard.html';
    } catch (err) {
      showError(loginError, err.message);
    } finally {
      setLoading(btn, false);
    }
  });

  // Signup
  signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessages();
    const name = document.getElementById('signupName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;
    const btn = signupForm.querySelector('button[type="submit"]');

    if (!name || !email || !password || !confirm) return showError(signupError, 'Please fill all fields');
    if (password !== confirm) return showError(signupError, 'Passwords do not match');
    if (password.length < 6) return showError(signupError, 'Password must be at least 6 characters');

    setLoading(btn, true);
    try {
      await window.CareerFitAPI.signup(name, email, password);
      showSuccess(signupSuccess, '✅ Account created! Please login.');
      signupForm.reset();
      setTimeout(() => {
        loginTab.click();
        document.getElementById('loginEmail').value = email;
      }, 1500);
    } catch (err) {
      showError(signupError, err.message);
    } finally {
      setLoading(btn, false);
    }
  });

  // Demo login hint
  const demoBtn = document.getElementById('demoLogin');
  if (demoBtn) {
    demoBtn.addEventListener('click', () => {
      document.getElementById('loginEmail').value = 'demo@careerfit.ai';
      document.getElementById('loginPassword').value = 'demo123';
    });
  }
});
