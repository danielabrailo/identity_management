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
  const data = await ContextProfileAPI.list();

  let html = "<table class='table'>";
  html += "<tr><th>Context</th><th>Display Name</th><th>Actions</th></tr>";

  data.forEach((p) => {
    html += `
            <tr>
                <td>${p.context_name}</td>
                <td>${p.display_name}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editProfile(${p.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteProfile(${p.id})">Delete</button>
                </td>
            </tr>
        `;
  });

  html += "</table>";

  document.getElementById("context-list").innerHTML = html;
}

function showCreateForm() {
  document.getElementById("form-container").style.display = "block";
  document.getElementById("profile-id").value = "";
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

  document.getElementById("profile-id").value = data.id;
  document.getElementById("context").value = data.context;
  document.getElementById("display_name").value = data.display_name;
  document.getElementById("email").value = data.email;
  document.getElementById("phone").value = data.phone;
  document.getElementById("job_title").value = data.job_title;
  document.getElementById("linkedin").value = data.linkedin;

  document.getElementById("form-container").style.display = "block";
}

async function deleteProfile(id) {
  await ContextProfileAPI.remove(id);

  loadProfiles();
}

loadProfiles();
loadContexts();
