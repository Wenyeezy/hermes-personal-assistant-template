const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
let enabledModules = {nutrition: true, health: true, finance: false, career: false};

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {"Content-Type": "application/json", ...(options.headers || {})},
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `Request failed (${response.status})`);
  return payload;
}

function todayInputs() {
  const now = new Date();
  const pad = (value) => String(value).padStart(2, "0");
  const localDay = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  $$('input[type="date"]').forEach((input) => { if (!input.value) input.value = localDay; });
}

function localDate(offsetDays = 0) {
  const value = new Date();
  value.setDate(value.getDate() + offsetDays);
  const pad = (part) => String(part).padStart(2, "0");
  return `${value.getFullYear()}-${pad(value.getMonth() + 1)}-${pad(value.getDate())}`;
}

function displayNumber(value, digits = 0) {
  return Number(value || 0).toLocaleString(undefined, {maximumFractionDigits: digits});
}

function optionalNumber(value, digits = 0) {
  return value == null ? "—" : displayNumber(value, digits);
}

async function refreshStatus() {
  const data = await api("/api/status");
  if (data.demo_mode) {
    $("#workspace-mode").textContent = "A fictional day. A real local workspace.";
    $("#workspace-guidance").textContent = "All samples are fictional. Confirm a sample meal or log a workout; this separate demo uses no model or account. Finance stays off unless you enable it.";
  }
  enabledModules = data.module_settings;
  $$('[data-optional]').forEach((element) => { element.hidden = !enabledModules[element.dataset.optional]; });
  $$('[data-module]').forEach((element) => { element.checked = enabledModules[element.dataset.module]; });
  const active = $(".tab.active");
  if (active?.hidden) activateModule("nutrition");
  const {nutrition, health, workout} = data.modules;
  $("#nutrition-metric").textContent = `${displayNumber(nutrition.calories)} kcal`;
  $("#nutrition-detail").textContent = `${nutrition.entries} confirmed meal${nutrition.entries === 1 ? "" : "s"}`;
  $("#health-metric").textContent = health ? `${displayNumber(health.steps)} steps` : "No data";
  $("#health-detail").textContent = health ? `${health.occurred_on} · ${health.source}` : "Manual bridge ready";
  $("#protein-metric").textContent = `${displayNumber(nutrition.protein_g, 1)} g`;
  $("#workout-metric").textContent = `${displayNumber(workout.minutes, 1)} min`;
  $("#workout-detail").textContent = `${workout.entries} workout${workout.entries === 1 ? "" : "s"} saved today`;

  const select = $("#provider-select");
  const selected = select.value;
  select.innerHTML = "";
  Object.entries(data.providers).forEach(([name, status]) => {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = `${name} · ${status.reason}`;
    option.disabled = !status.ready;
    select.append(option);
  });
  if ([...select.options].some((option) => option.value === selected && !option.disabled)) select.value = selected;

  const [nutritionRange, healthRange] = await Promise.all([
    api(`/api/nutrition/summary?start=${localDate(-6)}&end=${localDate()}`),
    api("/api/health/summary?days=7"),
  ]);
  const totals = nutritionRange.totals;
  const goal = nutritionRange.goals;
  $("#nutrition-summary").textContent = `Last 7 days, confirmed records · ${displayNumber(totals.calories)} kcal · ${displayNumber(totals.protein_g, 1)} g protein${goal?.calories ? ` · daily goal ${displayNumber(goal.calories)} kcal` : " · goals are optional"}`;
  const days = healthRange.days;
  const avgSteps = days.length ? days.reduce((sum, item) => sum + Number(item.steps || 0), 0) / days.length : 0;
  $("#health-summary").textContent = `Recent ${days.length} recorded day${days.length === 1 ? "" : "s"} · ${displayNumber(avgSteps)} avg steps · ${healthRange.workouts.length} workout${healthRange.workouts.length === 1 ? "" : "s"}`;
}

function compactItem(module, item) {
  if (module === "nutrition") return `${item.occurred_on} · ${item.description} · ${displayNumber(item.calories)} kcal · ${item.status} · ${item.source}`;
  if (module === "health") return `${item.occurred_on} · ${optionalNumber(item.steps)} steps · ${optionalNumber(item.exercise_minutes, 1)} min · ${optionalNumber(item.distance_km, 2)} km`;
  if (module === "health/workouts") return `${item.occurred_on} · ${item.activity} · ${displayNumber(item.duration_minutes, 1)} min · ${optionalNumber(item.active_calories)} active kcal`;
  if (module === "finance") return `${item.occurred_on} · ${item.description} · ${displayNumber(item.amount, 2)} · ${item.status}`;
  return `${item.company} · ${item.role} · ${item.status}${item.next_step ? ` · ${item.next_step}` : ""}`;
}

async function refreshList(module) {
  const container = $(`[data-list="${module}"]`);
  const {items} = await api(`/api/${module}?limit=8`);
  container.innerHTML = "<h3>Recent</h3>";
  if (!items.length) {
    container.insertAdjacentHTML("beforeend", '<p class="empty">Nothing saved yet.</p>');
    return;
  }
  const list = document.createElement("ul");
  items.forEach((item) => {
    const row = document.createElement("li");
    row.textContent = compactItem(module, item);
    if (module === "nutrition" && item.status === "needs_review") {
      const confirm = document.createElement("button");
      confirm.type = "button";
      confirm.textContent = "Confirm this meal";
      confirm.addEventListener("click", async () => {
        confirm.disabled = true;
        try {
          await api("/api/nutrition/confirm", {method: "POST", body: JSON.stringify({id: item.id, confirmed: true})});
          await Promise.all([refreshStatus(), refreshList("nutrition")]);
        } catch (error) { confirm.disabled = false; $("#nutrition-summary").textContent = error.message; }
      });
      row.append(confirm);
    }
    list.append(row);
  });
  container.append(list);
}

function formPayload(form) {
  const payload = {};
  new FormData(form).forEach((value, key) => { payload[key] = value; });
  return payload;
}

function readAsDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error("Could not read image"));
    reader.readAsDataURL(file);
  });
}

$("#analyze-nutrition-photo").addEventListener("click", async () => {
  const file = $("#nutrition-photo").files[0];
  const status = $("#nutrition-photo-status");
  const form = $('[data-api="nutrition"]');
  if (!file) {
    status.textContent = "Choose a JPEG, PNG, or WebP first.";
    return;
  }
  if (file.size > 5_000_000) {
    status.textContent = "Choose an image smaller than 5 MB.";
    return;
  }
  status.textContent = "Sending this image to your configured OpenAI account…";
  try {
    const image_data_url = await readAsDataURL(file);
    const {estimate} = await api("/api/nutrition/analyze-photo", {
      method: "POST",
      body: JSON.stringify({image_data_url}),
    });
    Object.entries(estimate).forEach(([key, value]) => {
      if (form.elements[key]) form.elements[key].value = value;
    });
    status.textContent = `Estimate loaded (${Math.round(Number(estimate.confidence || 0) * 100)}% confidence). Review every field, then explicitly save.`;
  } catch (error) {
    status.textContent = error.message;
  }
});

$$('.entry-form[data-api]').forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const module = form.dataset.api;
    const status = $$(".status-line", form).at(-1);
    const submit = $('button[type="submit"]', form);
    submit.disabled = true;
    status.textContent = "Saving locally…";
    try {
      await api(`/api/${module}`, {method: "POST", body: JSON.stringify(formPayload(form))});
      status.textContent = "Saved locally.";
      await Promise.all([refreshStatus(), refreshList(module)]);
    } catch (error) {
      status.textContent = error.message;
    } finally {
      submit.disabled = false;
    }
  });
});

$("#nutrition-goals-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const status = $(".status-line", form);
  status.textContent = "Saving goals locally…";
  try {
    await api("/api/nutrition/goals", {method: "POST", body: JSON.stringify(formPayload(form))});
    status.textContent = "Goals saved locally.";
    await refreshStatus();
  } catch (error) {
    status.textContent = error.message;
  }
});

$("#chat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const message = form.elements.message.value.trim();
  const provider = $("#provider-select").value;
  const log = $("#chat-log");
  const status = $("#chat-status");
  if (!message) return;
  const user = document.createElement("div");
  user.className = "message user";
  user.textContent = message;
  log.append(user);
  form.elements.message.value = "";
  status.textContent = `Waiting for ${provider}…`;
  try {
    const result = await api("/api/chat", {method: "POST", body: JSON.stringify({message, provider, session_id: "dashboard"})});
    const assistant = document.createElement("div");
    assistant.className = "message assistant";
    assistant.textContent = result.text;
    log.append(assistant);
    status.textContent = `Answered by ${result.provider}.`;
  } catch (error) {
    status.textContent = error.message;
  }
  log.scrollTop = log.scrollHeight;
});

function activateModule(target) {
  const tab = $(`[data-target="${target}"]`);
  if (!tab || tab.hidden || !enabledModules[target]) return;
  $$('.tab, .module').forEach((item) => item.classList.remove("active"));
  $(`[data-target="${target}"]`).classList.add("active");
  $(`#${target}`).classList.add("active");
}
$$('.tab').forEach((tab) => tab.addEventListener("click", () => activateModule(tab.dataset.target)));
$$('[data-jump]').forEach((button) => button.addEventListener("click", () => {
  activateModule(button.dataset.jump);
  $(`#${button.dataset.jump}`).scrollIntoView({behavior: "smooth", block: "start"});
  $("input", $(`#${button.dataset.jump}`)).focus({preventScroll: true});
}));

async function start() {
  todayInputs();
  await refreshStatus();
  await Promise.all(["nutrition", "health", "health/workouts", ...["finance", "career"].filter((name) => enabledModules[name])].map(refreshList));
}

$$('[data-module]').forEach((control) => control.addEventListener("change", async () => {
  const module = control.dataset.module;
  const enabled = control.checked;
  const status = $("#module-status");
  control.disabled = true;
  try {
    await api("/api/modules", {method: "POST", body: JSON.stringify({module, enabled})});
    await refreshStatus();
    if (enabled) await refreshList(module);
    status.textContent = `${module === "finance" ? "Finance" : "Career"} ${enabled ? "enabled by your choice" : "off"}. Existing records kept. No account connected.`;
  } catch (error) { control.checked = !enabled; status.textContent = error.message; }
  finally { control.disabled = false; }
}));

start().catch((error) => { $("#chat-status").textContent = error.message; });
