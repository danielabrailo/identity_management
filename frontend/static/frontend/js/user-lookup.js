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
  // Get username
  const username = document.getElementById("search").value.trim();
  // If there's no username provided
  if (!username) {
    document.getElementById("results").innerHTML = `
      <div class="empty-state">
        <i class="bi bi-search"></i>
        <h4>Enter a username</h4>
        <p>
          Enter a username to search for a user.
        </p>
      </div>
    `;
    return;
  }
  // Get user
  const data = await request(
    `/api/users/search/?username=${encodeURIComponent(username)}`
  );
  renderUsers(data);
}
function renderUsers(users) {
  // If no users are found
  if (users.length === 0) {
    document.getElementById("results").innerHTML = `
      <div class="empty-state">
        <i class="bi bi-person-x"></i>
        <h4>No users found</h4>
        <p>
          Try searching for a different username.
        </p>
      </div>
    `;
    return;
  }
  // Results
  let html = `
    <div class="search-results-header">
      <div>
        <h3>Search Results</h3>
        <p>Select a user to submit an identity request.</p>
      </div>
    </div>
    <div class="user-results">
  `;
  // Parse through users founds
  users.forEach((u) => {
    html += `
      <div class="user-result-card">
        <div class="user-result-info">
          <div class="user-avatar">
            <i class="bi bi-person"></i>
          </div>
          <div>
            <span class="user-result-label">
              Username
            </span>
            <h5>
              ${u.username}
            </h5>
          </div>
        </div>
        <button
          class="btn btn-primary btn-sm"
          onclick="submitRequest(${u.id})">
          <i class="bi bi-send"></i>
          Request Identity
        </button>
      </div>
    `;
  });
  html += `
    </div>
  `;
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
  <div class="request-success">
    <div class="success-icon">
      <i class="bi bi-check-lg"></i>
    </div>
    <div>
      <h4>Request submitted</h4>
      <p>
        The user has been notified and can now approve or deny your request.
      </p>
    </div>
  </div>
`;
}
loadDropdowns();
