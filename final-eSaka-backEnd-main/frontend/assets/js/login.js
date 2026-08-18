const form = document.getElementById('loginForm');
const emailField = document.getElementById('emailField');
const passwordField = document.getElementById('passwordField');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const formStatus = document.getElementById('formStatus');

// Explicit paths gamit ang './dashboards/'
const ACCOUNTS = {
  // AEW Role
  'aew': { pass: 'password123', page: './dashboards/aew.html' },
  'aew_user': { pass: 'password123', page: './dashboards/aew.html' },
  'aew@esaka.ph': { pass: 'password123', page: './dashboards/aew.html' },

  // DA-RFO Officer
  'da': { pass: 'password123', page: './dashboards/da.html' },
  'da_officer': { pass: 'password123', page: './dashboards/da.html' },
  'da@esaka.ph': { pass: 'password123', page: './dashboards/da.html' },

  // Municipal Coordinator
  'municipal': { pass: 'password123', page: './dashboards/municipal.html' },
  'lgu_officer': { pass: 'password123', page: './dashboards/municipal.html' },
  'municipal@esaka.ph': { pass: 'password123', page: './dashboards/municipal.html' },

  // Provincial Coordinator
  'provincial': { pass: 'password123', page: './dashboards/provincial.html' },
  'provincial@esaka.ph': { pass: 'password123', page: './dashboards/provincial.html' },

  // System Administrator
  'admin': { pass: 'password123', page: './dashboards/system-admin.html' },
  'sysadmin': { pass: 'password123', page: './dashboards/system-admin.html' },
  'admin@esaka.ph': { pass: 'password123', page: './dashboards/system-admin.html' }
};

function setError(fieldEl, isInvalid){
  fieldEl.classList.toggle('has-error', isInvalid);
  fieldEl.querySelector('input').classList.toggle('invalid', isInvalid);
}

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const userInput = emailInput.value.trim().toLowerCase();
  const password = passwordInput.value.trim();

  let hasError = false;

  if (userInput === ''){
    setError(emailField, true);
    hasError = true;
  } else {
    setError(emailField, false);
  }

  if (password === ''){
    setError(passwordField, true);
    hasError = true;
  } else {
    setError(passwordField, false);
  }

  if (hasError){
    formStatus.textContent = '';
    formStatus.classList.remove('show');
    return;
  }

  const account = ACCOUNTS[userInput];

  if (account && account.pass === password) {
    formStatus.className = 'form-status show';
    formStatus.textContent = 'Login successful! Redirecting...';

    setTimeout(() => {
      window.location.href = account.page;
    }, 600);
  } else {
    formStatus.className = 'form-status error show';
    formStatus.textContent = 'Invalid username or password.';
  }
});