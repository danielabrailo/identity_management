async function loadPolicies() {
  //Get data
  const data = await request("/api/policies/");

  //build HTML
  let html = "";
  //if no data
  if (data.length === 0) {
    html = `
      <div class="empty-state">
        <i class="bi bi-shield-check"></i>
        <h4>No Policies Yet</h4>
        <p>
          Create a policy to control which information can be shared.
        </p>
      </div>
    `;
  } else {
    //Parse through data
    data.forEach((p) => {
      const permissions = [];
      if (p.can_view_display_name) permissions.push("Display Name");
      if (p.can_view_email) permissions.push("Email");
      if (p.can_view_phone) permissions.push("Phone");
      if (p.can_view_job_title) permissions.push("Job Title");
      if (p.can_view_linkedin) permissions.push("LinkedIn");
      if (p.can_view_social_media) permissions.push("Social Media");
      if (p.can_view_nickname) permissions.push("Nickname");
      if (p.can_view_organization) permissions.push("Organization");
      if (p.can_view_pronouns) permissions.push("Pronouns");
      if (p.can_view_location) permissions.push("Location");
      if (p.can_view_university) permissions.push("University");
      if (p.can_view_website) permissions.push("Website");
      if (p.can_view_bio) permissions.push("Bio");
      if (p.can_view_preferred_contact_way)
        permissions.push("Preferred Contact Way");
      //Build HTML with each permission in a card style
      html += `
        <div class="policy-card">
          <div class="policy-card-header">
            <div>
              <span class="policy-context">
                <i class="bi bi-shield-check"></i>
                ${p.context_name}
              </span>
              <h4>
              <span class="subtitle">Requester type: </span>
                ${p.requester_type_name}
              </h4>
            </div>
          </div>
          <div class="policy-divider"></div>
          <div class="policy-permissions">
            <span class="permissions-label">
              Information shared
            </span>
            <div class="permission-tags">
              ${
                permissions.length > 0
                  ? permissions
                      .map(
                        (permission) => `
                          <span class="permission-tag">
                            <i class="bi bi-check-circle-fill"></i>
                            ${permission}
                          </span>
                        `
                      )
                      .join("")
                  : `
                      <span class="permission-tag denied">
                        <i class="bi bi-eye-slash"></i>
                        No information shared
                      </span>
                    `
              }
            </div>
          </div>
          <div class="policy-actions">
            <button
              class="btn btn-primary btn-sm"
              onclick="editPolicy(${p.id})">
              <i class="bi bi-pencil"></i>
              Edit
            </button>
            <button
              class="btn btn-outline-danger btn-sm"
              onclick="deletePolicy(${p.id})">
              <i class="bi bi-trash"></i>
              Delete
            </button>
          </div>
        </div>
      `;
    });
  }

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
    can_view_nickname: document.getElementById("nickname").checked,
    can_view_organization: document.getElementById("organization").checked,
    can_view_pronouns: document.getElementById("pronouns").checked,
    can_view_location: document.getElementById("location").checked,
    can_view_university: document.getElementById("university").checked,
    can_view_website: document.getElementById("website").checked,
    can_view_bio: document.getElementById("bio").checked,
    can_view_preferred_contact_way: document.getElementById(
      "preferred_contact_way"
    ).checked,
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
  resetPolicyForm();
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
  document.getElementById("nickname").checked = p.can_view_nickname;
  document.getElementById("organization").checked = p.can_view_organization;
  document.getElementById("pronouns").checked = p.can_view_pronouns;
  document.getElementById("location").checked = p.can_view_location;
  document.getElementById("university").checked = p.can_view_university;
  document.getElementById("website").checked = p.can_view_website;
  document.getElementById("bio").checked = p.can_view_bio;
  document.getElementById("preferred_contact_way").checked =
    p.can_view_preferred_contact_way;

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
  //change form title according to if it's editing or a new one
  document.getElementById("policy-form-title").textContent =
    document.getElementById("policy-id").value
      ? "Edit Policy"
      : "Create Policy";
}

function hideForm() {
  resetPolicyForm();
  document.getElementById("form").style.display = "none";
}
function resetPolicyForm() {
  const contextSelect = document.getElementById("context");
  contextSelect.selectedIndex = 0;
  const requesterSelect = document.getElementById("requester_type");
  requesterSelect.selectedIndex = 0;

  document.getElementById("policy-id").value = "";
  document.getElementById("context").value = "";
  document.getElementById("requester_type").value = "";

  document.getElementById("display_name").checked = false;
  document.getElementById("email").checked = false;
  document.getElementById("phone").checked = false;
  document.getElementById("job_title").checked = false;
  document.getElementById("linkedin").checked = false;
  document.getElementById("social_media").checked = false;
  document.getElementById("nickname").checked = false;
  document.getElementById("organization").checked = false;
  document.getElementById("pronouns").checked = false;
  document.getElementById("location").checked = false;
  document.getElementById("university").checked = false;
  document.getElementById("website").checked = false;
  document.getElementById("bio").checked = false;
  document.getElementById("preferred_contact_way").checked = "";
}

loadPolicies();
loadDropdowns();
