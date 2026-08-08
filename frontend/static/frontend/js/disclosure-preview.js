// Add labels for a better display in the UI
const labels = {
  display_name: "Display Name",
  email: "Email",
  phone: "Phone",
  job_title: "Job Title",
  linkedin: "LinkedIn",
  social_media: "Social Media",
};

async function loadRequests() {
  //requests
  const requests = await request("/api/identity-requests/approved/");
  // fill in the select
  const select = document.getElementById("identity_request");
  //If there isn't any approved request yet
  if (requests.length === 0) {
    document.getElementById("preview-result").innerHTML = `
      <div class="empty-state">
        <i class="bi bi-inbox"></i>
        <h4>No Approved Requests</h4>
        <p>
          You don't have any approved identity requests to preview yet.
        </p>
      </div>
    `;
    select.disabled = true;
    return;
  }
  // if there are requests
  requests.forEach((r) => {
    select.innerHTML += `
      <option value="${r.id}">
        ${r.target_username} - ${r.context_name}
      </option>
    `;
  });
}
async function previewDisclosure() {
  const requestId = document.getElementById("identity_request").value;
  if (!requestId) {
    return;
  }
  //payload
  const payload = {
    request_id: requestId,
  };
  // call endpoint
  const result = await request("/api/context-profiles/evaluate/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  //show results
  renderResult(result);
}
function renderResult(data) {
  //build hMTL
  let html = `
    <div class="disclosure-result">
      <div class="result-header">
        <div>
          <h3>Disclosed Information</h3>
          <p>
            This is the information available through this approved request.
          </p>
        </div>
        <div class="result-status">
          <i class="bi bi-shield-check"></i>
          Approved
        </div>
      </div>
      <div class="disclosure-grid">
  `;
  //Parse through data
  Object.entries(data).forEach(([key, value]) => {
    //only display fields that contain actual data
    if (value === null || value === undefined || value === "") {
      return;
    }
    html += `
      <div class="disclosure-item visible">
        <div class="disclosure-icon">
          <i class="bi ${getDisclosureIcon(key)}"></i>
        </div>
        <div class="disclosure-content">
          <span class="disclosure-label">
            ${labels[key] || key}
          </span>
          <span class="disclosure-value">
            ${value}
          </span>
        </div>
        <div class="disclosure-status">
          <i class="bi bi-check-circle-fill"></i>
        </div>
      </div>
    `;
  });
  html += `
      </div>

    </div>
  `;
  document.getElementById("preview-result").innerHTML = html;
}
function getDisclosureIcon(key) {
  //Get the corresponding icons
  const icons = {
    display_name: "bi-person",
    email: "bi-envelope",
    phone: "bi-telephone",
    job_title: "bi-briefcase",
    linkedin: "bi-linkedin",
    social_media: "bi-share",
    nickname: "bi-person-heart",
    organization: "bi-building",
  };
  return icons[key] || "bi-info-circle";
}
loadRequests();
