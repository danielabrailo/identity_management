// Add labels for a better display in the UI
const labels = {
  display_name: "Display Name",
  email: "Email",
  phone: "Phone",
  job_title: "Job Title",
  linkedin: "LinkedIn",
  social_media: "Social Media",
};
async function searchUsers() {
  const username = document.getElementById("search").value;

  const data = await request(`/api/users/search/?username=${username}`);

  renderUsers(data);
}
function renderUsers(users) {
  let html = "<table class='table'>";

  html += `
        <tr>
            <th>Username</th>
            <th>Actions</th>
        </tr>
    `;

  users.forEach((u) => {
    html += `
            <tr>
                <td>${u.username}</td>
                <td>
                    <button
                        class="btn btn-sm btn-primary"
                        onclick="goToDisclosure(${u.id})">
                        Preview Identity
                    </button>
                </td>
            </tr>
        `;
  });

  html += "</table>";

  document.getElementById("results").innerHTML = html;
}
async function loadDropdowns() {
  const contexts = await request("/api/contexts/");

  const requesterTypes = await request("/api/requester-types/");

  const contextSelect = document.getElementById("context");
  const requesterSelect = document.getElementById("requester_type");

  contexts.forEach((c) => {
    contextSelect.innerHTML += `
              <option value="${c.id}">
                  ${c.name}
              </option>
          `;
  });

  requesterTypes.forEach((r) => {
    requesterSelect.innerHTML += `
              <option value="${r.id}">
                  ${r.name}
              </option>
          `;
  });
}
async function goToDisclosure(userId) {
  const payload = {
    target_user_id: userId,
    context_id: document.getElementById("context").value,
    requester_type_id: document.getElementById("requester_type").value,
  };
  const result = await request("/api/context-profiles/evaluate/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  renderResult(result);
}
function renderResult(data) {
  let html = "<h4>User Information</h4>";
  html += "<table class='table'>";

  Object.entries(data).forEach(([key, value]) => {
    if (!value || value === "") {
      return;
    }
    html += `
                  <tr>
                      <th>${labels[key] || key}</th>
                      <td>${value}</td>
                  </tr>
              `;
  });

  html += "</table>";
  document.getElementById("results").innerHTML = html;
}
loadDropdowns();
