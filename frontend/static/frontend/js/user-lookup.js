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
                        onclick="submitRequest(${u.id})">
                        Submit Request
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
  const contextSelect = document.getElementById("context");
  // Load contexts
  contexts.forEach((c) => {
    contextSelect.innerHTML += `
              <option value="${c.id}">
                  ${c.name}
              </option>
          `;
  });
}
async function submitRequest(userId) {
  //Payload to send
  const payload = {
    target_user: userId,
    context: document.getElementById("context").value,
    reason: document.getElementById("reason").value,
  };
  //send request
  await request("/api/identity-requests/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  //Confirmation
  document.getElementById("results").innerHTML = `
    <div class="alert alert-success mt-3">
        <strong>Request submitted!</strong><br>
        The target user has been notified and can now approve or deny your request.
    </div>
  `;
}
loadDropdowns();
