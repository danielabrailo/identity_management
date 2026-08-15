const API_BASE = "/api";
const API = "/api/context-profiles/";

function getToken() {
  // session auth already handles cookies automatically
  return null;
}

const ContextProfileAPI = {
  list: () => request(`${API_BASE}/context-profiles/`),
  get: (id) => request(`${API_BASE}/context-profiles/${id}/`),
  create: (data) =>
    request(`${API_BASE}/context-profiles/`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id, data) =>
    request(`${API_BASE}/context-profiles/${id}/`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  remove: (id) =>
    request(`${API_BASE}/context-profiles/${id}/`, {
      method: "DELETE",
    }),
};

async function loadContexts() {
  const data = await request("/api/contexts/");
  const select = document.getElementById("context");
  select.innerHTML = "";

  data.forEach((c) => {
    const option = document.createElement("option");
    option.value = c.id;
    option.textContent = c.name;
    select.appendChild(option);
  });
}

//load the profiles and attach to HTML
async function loadProfiles() {
  //Get the data
  const data = await ContextProfileAPI.list();
  //build the HTML
  let html = "";
  //If empty
  if (data.length === 0) {
    html = `
      <div class="empty-state">
        <i class="bi bi-person-vcard"></i>
        <h4>No Context Profiles Yet</h4>
        <p>Create your first profile to start managing your digital identities.</p>
      </div>
    `;
  } else {
    data.forEach((p) => {
      //Build a card HTML with the data of each profile
      html += `
        <div class="profile-card">          
          <div class="profile-card-header">
            <span class="context-badge">
              ${getContextIcon(p.context_name)} ${p.context_name}
            </span>
          </div>
          <h4>${p.display_name || "Unnamed Profile"}</h4>
          ${
            p.job_title
              ? `
              <p>
                <i class="bi bi-briefcase"></i>
                ${p.job_title}
              </p>
            `
              : ""
          }
          ${
            p.organization
              ? `
              <p>
                <i class="bi bi-building"></i>
                ${p.organization}
              </p>
            `
              : ""
          }
          ${
            p.email
              ? `
              <p>
                <i class="bi bi-envelope"></i>
                ${p.email}
              </p>
            `
              : ""
          }
          ${
            p.phone
              ? `
              <p>
                <i class="bi bi-telephone"></i>
                ${p.phone}
              </p>
            `
              : ""
          }
          ${
            p.nickname
              ? `
                <p>
                  <i class="bi bi-person"></i>
                  ${p.nickname}
                </p>
              `
              : ""
          }
          
          ${
            p.linkedin
              ? `
                <p>
                  <i class="bi bi-linkedin"></i>
                  <a href="${p.linkedin}" target="_blank">LinkedIn</a>
                </p>
              `
              : ""
          }
          <div class="profile-actions">
            <button
              class="btn btn-primary btn-sm"
              onclick="editProfile(${p.id})">
              <i class="bi bi-pencil"></i>
              Edit
            </button>
            <button
              class="btn btn-outline-danger btn-sm"
              onclick="deleteProfile(${p.id})">
              <i class="bi bi-trash"></i>
              Delete
            </button>
          </div>
        </div>
      `;
    });
  }
  document.getElementById("context-list").innerHTML = html;
}

function getContextIcon(context) {
  //get icons for each context for easy identification
  switch (context.toLowerCase()) {
    case "professional":
      return "💼";
    case "public":
      return "🌎";
    case "academic":
      return "🎓";
    case "social":
      return "🎉";
    case "governmental/legal":
      return "⚖️";
    case "online":
      return "🌐";
    case "personal":
      return "🏠";
    default:
      return "🪪";
  }
}

function showCreateForm() {
  resetContextProfileForm();
  document.getElementById("form-title").textContent = "Create Profile";
  document.getElementById("form-container").style.display = "block";
}

function hideForm() {
  document.getElementById("form-container").style.display = "none";
}

async function saveProfile() {
  const id = document.getElementById("profile-id").value;
  const payload = {
    context: document.getElementById("context").value,
    display_name: document.getElementById("display_name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
    job_title: document.getElementById("job_title").value,
    linkedin: document.getElementById("linkedin").value,
    nickname: document.getElementById("nickname").value,
    organization: document.getElementById("organization").value,
  };

  if (id) {
    await ContextProfileAPI.update(id, payload);
  } else {
    await ContextProfileAPI.create(payload);
  }

  hideForm();
  loadProfiles();
}

async function editProfile(id) {
  const data = await request(`/api/context-profiles/${id}/`);
  resetContextProfileForm();

  document.getElementById("form-title").textContent = "Edit Profile";
  document.getElementById("profile-id").value = data.id;
  document.getElementById("context").value = data.context;
  document.getElementById("display_name").value = data.display_name;
  document.getElementById("email").value = data.email;
  document.getElementById("phone").value = data.phone;
  document.getElementById("job_title").value = data.job_title;
  document.getElementById("linkedin").value = data.linkedin;
  document.getElementById("nickname").value = data.nickname;
  document.getElementById("organization").value = data.organization;

  document.getElementById("form-container").style.display = "block";
}

async function deleteProfile(id) {
  await ContextProfileAPI.remove(id);

  loadProfiles();
}
//Reset form
function resetContextProfileForm() {
  document.getElementById("profile-id").value = "";

  document.getElementById("context").value = "";
  document.getElementById("display_name").value = "";
  document.getElementById("email").value = "";
  document.getElementById("phone").value = "";
  document.getElementById("job_title").value = "";
  document.getElementById("linkedin").value = "";
  document.getElementById("nickname").value = "";
  document.getElementById("organization").value = "";

  const contextSelect = document.getElementById("context");
  contextSelect.value = "";
  contextSelect.selectedIndex = 0;
}

loadProfiles();
loadContexts();
