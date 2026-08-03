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
  //get container
  const container = document.getElementById("requests-container");
  //empty state
  if (requests.length === 0) {
    container.innerHTML = `
            <div class="alert alert-info">
                You have no incoming identity requests.
            </div>
        `;

    return;
  }
  //create table with requests
  let html = `
  <table class="table">
  <tr>
      <th>Requester</th>
      <th>Context</th>
      <th>Reason</th>
      <th>Status</th>
      <th>Requester Type</th>
      <th>Actions</th>
  </tr>
  `;
  requests.forEach((r) => {
    html += `
      <tr>
          <td>
              ${r.requester_username}
          </td>
          <td>
              ${r.context_name}
          </td>
          <td>
              ${r.reason}
          </td>
          <td>
              ${r.status}
          </td>
          <td>
          ${
            r.status === "approved"
              ? r.requester_type_name
              : `
              <select 
                  id="requester-type-${r.id}"
                  class="form-select">
                  ${renderRequesterTypes()}
              </select>
              `
          }
          </td>
          <td>
            <button
                class="btn btn-success btn-sm"
                onclick="approveRequest(${r.id})"
                ${r.status === "approved" ? "disabled" : ""}>
                Approve
            </button>
        
            <button
                class="btn btn-danger btn-sm"
                onclick="denyRequest(${r.id})"
                ${r.status === "denied" ? "disabled" : ""}>
                Deny
            </button>      
        </td>
      </tr>
      `;
  });
  html += "</table>";
  container.innerHTML = html;
}
function renderRequesterTypes() {
  let options = "";
  //Fill in the requester types options
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
  const response = await request(`/api/identity-requests/${id}/approve/`, {
    method: "PATCH",
    body: JSON.stringify({
      requester_type: requesterType,
    }),
  });
  alert("Request approved!");
  loadRequests();
}
async function denyRequest(id) {
  //call endpoint
  await request(`/api/identity-requests/${id}/deny/`, {
    method: "PATCH",
  });
  alert("Request denied!");
  loadRequests();
}
loadPage();
