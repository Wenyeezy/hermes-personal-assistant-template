"use strict";
window.HERMES_FIXTURES = {
  schema: "hermes.fictional-preview.v1",
  fictional: true,
  profile: { name: "Alex", label: "A fictional day" },
  career: { company: "Harbor Works", role: "Product Operations", nextStep: "Review the role and write one question.", status: "draft" },
  nutrition: [
    { description: "Oat bowl", calories: 420, protein_g: 18, status: "confirmed" },
    { description: "Lunch estimate", calories: 610, protein_g: 28, status: "needs_review" }
  ],
  finance: { description: "Notebook", amount: 12, category: "Supplies", status: "needs_review" }
};
