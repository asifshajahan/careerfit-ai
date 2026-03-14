document.addEventListener('DOMContentLoaded', () => {
  const user = JSON.parse(localStorage.getItem('careerfit_user') || 'null');
  if (!user) { window.location.href = 'index.html'; return; }

  // Set user info
  document.getElementById('userName').textContent = user.name;
  document.getElementById('userEmail').textContent = user.email;
  document.getElementById('userInitial').textContent = user.name.charAt(0).toUpperCase();

  // Logout
  document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('careerfit_user');
    window.location.href = 'index.html';
  });

  // Tab switching between Resume and Skills
  const tabs = document.querySelectorAll('.input-tab');
  const panels = document.querySelectorAll('.input-panel');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tab.dataset.panel).classList.add('active');
    });
  });

  // File upload drag & drop
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('resumeFile');
  const fileInfo = document.getElementById('fileInfo');

  dropZone.addEventListener('click', () => fileInput.click());

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });

  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) handleFileSelect(e.target.files[0]);
  });

  function handleFileSelect(file) {
    const allowed = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const allowedExt = ['.pdf', '.docx', '.doc'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedExt.includes(ext)) {
      showNotification('Only PDF and DOCX files are supported', 'error');
      return;
    }

    fileInput._file = file;
    fileInfo.innerHTML = `
      <div class="file-selected">
        <span class="file-icon">${ext === '.pdf' ? '📄' : '📝'}</span>
        <span class="file-name">${file.name}</span>
        <span class="file-size">${(file.size / 1024).toFixed(1)} KB</span>
        <button class="remove-file" onclick="removeFile()">✕</button>
      </div>
    `;
    dropZone.classList.add('has-file');
  }

  window.removeFile = () => {
    fileInput.value = '';
    fileInput._file = null;
    fileInfo.innerHTML = '';
    dropZone.classList.remove('has-file');
  };

  // Skills tags
  const skillInput = document.getElementById('skillInput');
  const skillTags = document.getElementById('skillTags');
  const addSkillBtn = document.getElementById('addSkillBtn');
  let skills = [];

  function addSkill(val) {
    const skill = val.trim().toLowerCase();
    if (skill && !skills.includes(skill)) {
      skills.push(skill);
      renderTags();
    }
  }

  function renderTags() {
    skillTags.innerHTML = skills.map((s, i) => `
      <span class="skill-tag">
        ${s}
        <button onclick="removeSkill(${i})">✕</button>
      </span>
    `).join('');
    document.getElementById('skillCount').textContent = `${skills.length} skill${skills.length !== 1 ? 's' : ''} added`;
  }

  window.removeSkill = (i) => {
    skills.splice(i, 1);
    renderTags();
  };

  addSkillBtn.addEventListener('click', () => {
    if (skillInput.value.trim()) {
      addSkill(skillInput.value);
      skillInput.value = '';
    }
  });

  skillInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      if (skillInput.value.trim()) {
        addSkill(skillInput.value.replace(',', ''));
        skillInput.value = '';
      }
    }
  });

  // Suggest common skills
  const suggestions = [
    'Python', 'JavaScript', 'React', 'Machine Learning', 'SQL',
    'Java', 'AWS', 'Docker', 'TensorFlow', 'Node.js',
    'Figma', 'Power BI', 'Excel', 'Tableau', 'Git'
  ];

  const suggestContainer = document.getElementById('skillSuggestions');
  suggestContainer.innerHTML = suggestions.map(s =>
    `<button class="suggest-chip" onclick="addSuggestedSkill('${s}')">${s}</button>`
  ).join('');

  window.addSuggestedSkill = (s) => {
    addSkill(s);
    document.querySelectorAll('.suggest-chip').forEach(chip => {
      if (chip.textContent === s) chip.classList.add('used');
    });
  };

  // PREDICT Button
  document.getElementById('predictBtn').addEventListener('click', async () => {
    const activeTab = document.querySelector('.input-tab.active').dataset.panel;
    const btn = document.getElementById('predictBtn');

    try {
      btn.disabled = true;
      btn.innerHTML = '<span class="btn-spinner"></span> Analyzing...';
      hideResult();

      let result;

      if (activeTab === 'resumePanel') {
        const file = fileInput._file || fileInput.files[0];
        if (!file) { showNotification('Please upload a resume first', 'error'); return; }
        const response = await window.CareerFitAPI.predictFromResume(file, user.email);
        result = response;
      } else {
        if (skills.length === 0) { showNotification('Please add at least one skill', 'error'); return; }
        const response = await window.CareerFitAPI.predictFromSkills(skills.join(', '), user.email);
        result = response;
      }

      displayResult(result);
    } catch (err) {
      showNotification(err.message || 'Prediction failed. Is the backend running?', 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<span>✦</span> Predict My Career';
    }
  });

  function hideResult() {
    document.getElementById('resultSection').style.display = 'none';
  }

  function displayResult(data) {
    const p = data.prediction;
    const resultSection = document.getElementById('resultSection');

    // Best career
    document.getElementById('bestCareer').textContent = p.best_career;
    document.getElementById('careerConfidence').textContent = `${p.confidence}% Match`;
    document.getElementById('careerDescription').textContent = p.description;
    document.getElementById('careerSalary').textContent = `₹${p.average_salary} LPA`;
    document.getElementById('careerCompanies').textContent = p.top_companies;
    document.getElementById('careerPath').textContent = p.learning_path;

    // Key skills
    const keySkillsEl = document.getElementById('careerKeySkills');
    if (p.key_skills) {
      const skillArr = p.key_skills.split(',').map(s => s.trim()).filter(Boolean);
      keySkillsEl.innerHTML = skillArr.map(s => `<span class="result-skill-tag">${s}</span>`).join('');
    }

    // Detected skills
    if (data.skills_detected && data.skills_detected.length > 0) {
      document.getElementById('detectedSkillsWrap').style.display = 'block';
      document.getElementById('detectedSkills').innerHTML =
        data.skills_detected.slice(0, 15).map(s => `<span class="detected-tag">${s}</span>`).join('');
    }

    // Top 3
    const top3El = document.getElementById('top3Careers');
    top3El.innerHTML = p.top_3.map((c, i) => `
      <div class="top-career-item ${i === 0 ? 'best' : ''}">
        <span class="rank">#${i + 1}</span>
        <span class="top-career-name">${c.career}</span>
        <span class="top-career-conf">${c.confidence}%</span>
        <div class="conf-bar">
          <div class="conf-fill" style="width: ${c.confidence}%"></div>
        </div>
      </div>
    `).join('');

    // Show result with animation
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Animate confidence bar
    setTimeout(() => {
      document.querySelectorAll('.conf-fill').forEach(el => {
        el.style.transition = 'width 1s ease';
      });
    }, 100);
  }

  function showNotification(msg, type = 'info') {
    const n = document.getElementById('notification');
    n.textContent = msg;
    n.className = `notification ${type} show`;
    setTimeout(() => n.classList.remove('show'), 4000);
  }
});
