"use strict";
window.HERMES_FIXTURES = {
  schema: "hermes.fictional-preview.v1",
  fictional: true,
  profile: { name: "Alex", label: "A fictional day" },
  fitness: { steps: 6800, activity: "Walking", duration_minutes: 30, logged: false },
  financeEnabled: false,
  nutrition: [
    { description: "Oat bowl", calories: 420, protein_g: 18, status: "confirmed" },
    { description: "Lunch estimate", calories: 610, protein_g: 28, status: "needs_review" }
  ],
  finance: { description: "Notebook", amount: 12, category: "Supplies", status: "needs_review" }
};
