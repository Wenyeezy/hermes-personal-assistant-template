"use strict";

/* Query-only composition selection. No fetch, storage, runtime, or model calls. */
(() => {
  const params = new URLSearchParams(window.location.search);
  const scenes = ["cover", "meal", "workout", "summary", "install"];
  const requestedScene = params.get("scene");
  const isStoryboard = scenes.includes(requestedScene);
  const scene = isStoryboard ? requestedScene : "cover";
  const format = params.get("format") === "square" ? "square" : "wide";
  const root = document.documentElement;

  root.dataset.format = format;
  root.dataset.mode = isStoryboard ? "storyboard" : "poster";
  root.dataset.scene = scene;
  // Capture dimensions are metadata for the composing agent, not runtime state.
  root.dataset.captureWidth = format === "square" ? "1080" : isStoryboard ? "1280" : "1200";
  root.dataset.captureHeight = format === "square" ? "1080" : isStoryboard ? "720" : "675";

  for (const section of document.querySelectorAll(".scene[data-scene]")) {
    section.hidden = section.dataset.scene !== scene;
  }

  const position = document.getElementById("scene-position");
  position.hidden = !isStoryboard;
  position.textContent = `${String(scenes.indexOf(scene) + 1).padStart(2, "0")} / 05`;
  const names = { cover: "Meals + Fitness", meal: "Meal record", workout: "Walking", summary: "Daily summary", install: "Run locally" };
  document.title = `Hermes Life | ${names[scene]} | ${isStoryboard ? "Illustrative storyboard" : "Launch asset"}`;
})();
