let requesterTypes = [];

async function loadPage() {
  await loadRequesterTypes();
  await loadRequests();
}
async function loadRequesterTypes() {
  requesterTypes = await request("/api/requester-types/");
}
async function loadRequests() {
  //Call requests
  const requests = await request("/api/identity-requests/");
  renderRequests(requests);
}
function renderRequests(requests) {
  const container = document.getElementById("requests-container");
  //Empty state
  if (requests.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="bi bi-inbox"></i>
        <h4>No incoming requests</h4>
        <p>
          You don't have any identity requests waiting for your review.
        </p>
      </div>
    `;
    return;
  }
  //Build HTML
  let html = `
    <div class="requests-list">
  `;
  //Parse through requests data
  requests.forEach((r) => {
    const statusClass =
      r.status === "approved"
        ? "status-approved"
        : r.status === "denied"
        ? "status-denied"
        : "status-pending";
    const statusIcon =
      r.status === "approved"
        ? "bi-check-circle-fill"
        : r.status === "denied"
        ? "bi-x-circle-fill"
        : "bi-clock-fill";
    html += `
      <div class="request-card">
      <!-- Action message for this specific request -->
      <div id="request-message-${r.id}"></div>
        <!-- Header -->
        <div class="request-card-header">
          <div class="requester-info">
            <div class="requester-avatar">
              <i class="bi bi-person"></i>
            </div>
            <div>
              <span class="request-label">
                Identity request from
              </span>
              <h4>
                ${r.requester_username}
              </h4>
            </div>
          </div>
          <span class="request-status ${statusClass}">
            <i class="bi ${statusIcon}"></i>
            ${capitalizeStatus(r.status)}
          </span>
        </div>
        <!--Request details -->
        <div class="request-details">
          <div class="request-detail">
            <span class="detail-label">
              <i class="bi bi-shield"></i>
              Context
            </span>
            <span class="detail-value">
              ${r.context_name}
            </span>
          </div>
          <div class="request-detail">
            <span class="detail-label">
              <i class="bi bi-chat-left-text"></i>
              Reason
            </span>
            <span class="detail-value">
              ${r.reason || "No reason provided"}
            </span>
          </div>
        </div>
        <!-- Requester type -->
        <div class="request-permission">
          <div>
            <span class="detail-label">
              <i class="bi bi-person-badge"></i>
              Requester Type
            </span>
            ${
              r.status === "approved"
                ? `
                  <span class="requester-type-display">
                    ${r.requester_type_name}
                  </span>
                `
                : `
                  <select
                    id="requester-type-${r.id}"
                    class="form-select requester-type-select">
                    ${renderRequesterTypes()}
                  </select>
                `
            }
          </div>
        </div>
        <!-- Actions -->
        <div class="request-actions">
          <button
            class="btn btn-primary"
            onclick="approveRequest(${r.id})"
            ${r.status === "approved" ? "disabled" : ""}>
            <i class="bi bi-check-lg"></i>
            Approve
          </button>
          <button
            class="btn btn-outline-danger"
            onclick="denyRequest(${r.id})"
            ${r.status === "denied" ? "disabled" : ""}>
            <i class="bi bi-x-lg"></i>
            Deny
          </button>
        </div>
      </div>
    `;
  });
  html += `
    </div>
  `;
  container.innerHTML = html;
}
function renderRequesterTypes() {
  let options = "";
  //Fill in the possible requester types
  requesterTypes.forEach((type) => {
    options += `
      <option value="${type.id}">
        ${type.name}
      </option>
    `;
  });
  return options;
}
async function approveRequest(id) {
  //get requester type
  const requesterType = document.getElementById(`requester-type-${id}`).value;
  // call endpoint
  await request(`/api/identity-requests/${id}/approve/`, {
    method: "PATCH",
    body: JSON.stringify({
      requester_type: requesterType,
    }),
  });
  await loadRequests();
  //Show success message
  showRequestMessage(
    id,
    "Request approved",
    "The requester can now access the identity information allowed by your policy.",
    "success"
  );
}
async function denyRequest(id) {
  //call endpoint
  await request(`/api/identity-requests/${id}/deny/`, {
    method: "PATCH",
  });
  await loadRequests();
  //Show request denied msg
  showRequestMessage(
    id,
    "Request denied",
    "The identity request has been denied.",
    "denied"
  );
}
function showRequestMessage(id, title, message, type) {
  //Get container specific to the request card
  const container = document.getElementById(`request-message-${id}`);
  if (!container) {
    return;
  }
  //Type of message to define icon, class ad heading
  const isSuccess = type === "success";
  const icon = isSuccess ? "bi-check-lg" : "bi-x-lg";
  const className = isSuccess ? "request-success" : "request-denied";
  //Build HTML
  container.innerHTML = `
    <div class="${className} request-message">
      <div class="message-icon">
        <i class="bi ${icon}"></i>
      </div>
      <div>
        <h4>${title}</h4>
        <p>${message}</p>
      </div>
    </div>
  `;
  //utomatically remove the message after 3 seconds
  setTimeout(() => {
    container.innerHTML = "";
  }, 3000);
}
function capitalizeStatus(status) {
  return status.charAt(0).toUpperCase() + status.slice(1);
}
loadPage();
