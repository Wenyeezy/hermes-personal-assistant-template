"use strict";
(() => {
  const media = new URLSearchParams(window.location.search).get("media");
  if (["wide", "square", "career", "nutrition", "install"].includes(media)) {
    document.body.classList.add("social", `social-${media}`);
    if (["career", "nutrition"].includes(media)) document.body.classList.add("social-scene");
  }
  const fresh = () => JSON.parse(JSON.stringify(window.HERMES_FIXTURES));
  let sample = fresh();
  let receipts = [];
  const byId = (id) => document.getElementById(id);
  const tabs = [...document.querySelectorAll("[data-tab]")];
  function activate(name, focus = false) {
    tabs.forEach((tab) => {
      const active = tab.dataset.tab === name;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      byId(`panel-${tab.dataset.tab}`).hidden = !active;
      if (active && focus) tab.focus();
    });
  }
  function render() {
    byId("career-status").textContent = sample.career.status === "saved" ? "Saved (simulated)" : "Draft";
    byId("save-career").disabled = sample.career.status === "saved";
    const confirmed = sample.nutrition.filter((item) => item.status === "confirmed");
    byId("calorie-total").textContent = confirmed.reduce((total, item) => total + item.calories, 0).toLocaleString("en-US");
    byId("nutrition-summary").textContent = `${confirmed.reduce((total, item) => total + item.protein_g, 0)} g protein · ${confirmed.length} confirmed sample${confirmed.length === 1 ? "" : "s"}`;
    const lunchConfirmed = sample.nutrition[1].status === "confirmed";
    byId("lunch-status").textContent = lunchConfirmed ? "Confirmed (simulated)" : "Needs review";
    byId("lunch-status").classList.toggle("pending", !lunchConfirmed);
    byId("confirm-lunch").disabled = lunchConfirmed;
    const reviewed = sample.finance.status === "reviewed";
    byId("finance-status").textContent = reviewed ? "Reviewed (simulated)" : "Needs review";
    byId("finance-status").classList.toggle("pending", !reviewed);
    byId("review-expense").disabled = reviewed;
    byId("receipt-text").textContent = receipts.length ? receipts[receipts.length - 1].text : "Try an action above. Its simulated receipt will appear here.";
  }
  function receipt(action, description) {
    const id = `DEMO-${String(receipts.length + 1).padStart(3, "0")}`;
    receipts.push({ id, action, simulated: true, text: `${id} · ${description} · simulated, this tab only.` });
    render();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(tab.dataset.tab));
    tab.addEventListener("keydown", (event) => {
      let next;
      if (["ArrowDown", "ArrowRight"].includes(event.key)) next = (index + 1) % tabs.length;
      if (["ArrowUp", "ArrowLeft"].includes(event.key)) next = (index + tabs.length - 1) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); activate(tabs[next].dataset.tab, true); }
    });
  });
  byId("save-career").addEventListener("click", () => {
    if (sample.career.status === "saved") return;
    sample.career.status = "saved"; receipt("career.save", "Fictional opportunity saved. No application sent");
  });
  byId("confirm-lunch").addEventListener("click", () => {
    if (sample.nutrition[1].status === "confirmed") return;
    sample.nutrition[1].status = "confirmed"; receipt("nutrition.confirm", "Fictional lunch confirmed. Confirmed total: 1,030 kcal");
  });
  byId("review-expense").addEventListener("click", () => {
    if (sample.finance.status === "reviewed") return;
    sample.finance.status = "reviewed"; receipt("finance.review", "Fictional $12 expense reviewed. No money moved");
  });
  byId("reset-demo").addEventListener("click", () => { sample = fresh(); receipts = []; render(); activate("career"); });
  byId("export-demo").addEventListener("click", () => {
    const payload = { schema: "hermes.fictional-export.v1", fictional: true, simulated: true, sample, receipts };
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" }));
    const link = document.createElement("a"); link.href = url; link.download = "hermes-fictional-sample.json";
    document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  byId("copy-command").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(byId("install-command").textContent); byId("copy-status").textContent = "Copied. Run it in your downloaded source folder."; }
    catch (_) { byId("copy-status").textContent = "Clipboard unavailable. Select and copy the command above."; }
  });
  render();
  if (media === "nutrition") activate("nutrition");
})();
