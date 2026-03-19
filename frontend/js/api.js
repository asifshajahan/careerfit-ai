const API_BASE = "https://careerfit-ai-backend.onrender.com";

const api = {

  // Signup
  async signup(name, email, password) {
    const res = await fetch(`${API_BASE}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: name,
        email: email,
        password: password
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Signup failed");
    }

    return data;
  },

  // Login
  async login(email, password) {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Login failed");
    }

    return data;
  },

  // Predict career from skills
  async predictFromSkills(skills, email = null) {
    const res = await fetch(`${API_BASE}/predict-skills`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        skills: skills,
        email: email
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Prediction failed");
    }

    return data;
  },

  // Predict career from resume file
  async predictFromResume(file, email = null) {
    const formData = new FormData();

    formData.append("file", file);

    if (email) {
      formData.append("email", email);
    }

    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Resume prediction failed");
    }

    return data;
  },

  // Get career information
  async getCareerInfo() {
    const res = await fetch(`${API_BASE}/career-info`);

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Failed to fetch career info");
    }

    return data;
  }

};

// Make API available globally
window.CareerFitAPI = api;