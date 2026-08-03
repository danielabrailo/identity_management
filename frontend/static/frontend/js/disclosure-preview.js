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
      <div class="alert alert-info mt-3">
        You do not have any approved identity requests yet
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
  let html = "<h4>Disclosed Information</h4>";
  html += "<table class='table'>";

  Object.entries(data).forEach(([key, value]) => {
    if (!value) {
      value = "Not visible";
    }
    html += `
                <tr>
                    <th>${labels[key] || key}</th>
                    <td>${value}</td>
                </tr>
            `;
  });

  html += "</table>";
  document.getElementById("preview-result").innerHTML = html;
}
loadRequests();
