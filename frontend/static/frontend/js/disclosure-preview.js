// Add labels for a better display in the UI
const labels = {
  display_name: "Display Name",
  email: "Email",
  phone: "Phone",
  job_title: "Job Title",
  linkedin: "LinkedIn",
  social_media: "Social Media",
};

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
async function previewDisclosure() {
  const payload = {
    target_user_id: window.LOGGED_IN_USER_ID,
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
  let html = "<h4>Visible Information</h4>";
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
loadDropdowns();
