async function loadPolicies() {
  const data = await request("/api/policies/");

  let html = "<table class='table'>";
  html += "<tr><th>Context</th><th>Requester</th><th>Actions</th></tr>";

  data.forEach((p) => {
    html += `
            <tr>
                <td>${p.context_name}</td>
                <td>${p.requester_type_name}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editPolicy(${p.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deletePolicy(${p.id})">Delete</button>
                </td>
            </tr>
        `;
  });

  html += "</table>";

  document.getElementById("policy-list").innerHTML = html;
}

async function loadDropdowns() {
  const contexts = await request("/api/contexts/");
  const requesters = await request("/api/requester-types/");

  const ctx = document.getElementById("context");
  const req = document.getElementById("requester_type");

  ctx.innerHTML = "";
  req.innerHTML = "";

  contexts.forEach((c) => {
    ctx.innerHTML += `<option value="${c.id}">${c.name}</option>`;
  });

  requesters.forEach((r) => {
    req.innerHTML += `<option value="${r.id}">${r.name}</option>`;
  });
}

async function savePolicy() {
  const id = document.getElementById("policy-id").value;

  const payload = {
    context: document.getElementById("context").value,
    requester_type: document.getElementById("requester_type").value,

    can_view_display_name: document.getElementById("display_name").checked,
    can_view_email: document.getElementById("email").checked,
    can_view_phone: document.getElementById("phone").checked,
    can_view_job_title: document.getElementById("job_title").checked,
    can_view_linkedin: document.getElementById("linkedin").checked,
    can_view_social_media: document.getElementById("social_media").checked,
  };

  if (id) {
    await request(`/api/policies/${id}/`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  } else {
    await request("/api/policies/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  hideForm();
  loadPolicies();
}

async function editPolicy(id) {
  const p = await request(`/api/policies/${id}/`);

  document.getElementById("policy-id").value = p.id;
  document.getElementById("context").value = p.context;
  document.getElementById("requester_type").value = p.requester_type;

  document.getElementById("display_name").checked = p.can_view_display_name;
  document.getElementById("email").checked = p.can_view_email;
  document.getElementById("phone").checked = p.can_view_phone;
  document.getElementById("job_title").checked = p.can_view_job_title;
  document.getElementById("linkedin").checked = p.can_view_linkedin;
  document.getElementById("social_media").checked = p.can_view_social_media;

  showForm();
}

async function deletePolicy(id) {
  await request(`/api/policies/${id}/`, {
    method: "DELETE",
  });

  loadPolicies();
}

function showForm() {
  document.getElementById("form").style.display = "block";
}

function hideForm() {
  document.getElementById("form").style.display = "none";
}

loadPolicies();
loadDropdowns();
