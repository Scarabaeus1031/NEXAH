const filterButtons = [...document.querySelectorAll("[data-filter]")];
const applicationCards = [...document.querySelectorAll("[data-kind]")];

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    filterButtons.forEach((candidate) => candidate.classList.toggle("is-active", candidate === button));
    applicationCards.forEach((card) => {
      const kinds = card.dataset.kind.split(/\s+/);
      card.hidden = filter !== "all" && !kinds.includes(filter);
    });
  });
});

const areaMenus = [...document.querySelectorAll(".area-menu")];

areaMenus.forEach((menu) => {
  menu.addEventListener("toggle", () => {
    if (!menu.open) return;
    areaMenus.forEach((candidate) => {
      if (candidate !== menu) candidate.open = false;
    });
  });
});

document.addEventListener("click", (event) => {
  if (event.target.closest(".area-menu")) return;
  areaMenus.forEach((menu) => { menu.open = false; });
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  areaMenus.forEach((menu) => { menu.open = false; });
});

const archiveSearch = document.getElementById("archive-search");
const archiveItems = [...document.querySelectorAll("[data-archive-item]")];
const archiveGroups = [...document.querySelectorAll("[data-archive-group]")];
const archiveCount = document.getElementById("archive-count");
const archiveEmpty = document.getElementById("archive-empty");

if (archiveSearch) {
  const filterArchive = () => {
    const query = archiveSearch.value.trim().toLocaleLowerCase("de");
    let visible = 0;
    archiveItems.forEach((item) => {
      const match = !query || item.textContent.toLocaleLowerCase("de").includes(query);
      item.hidden = !match;
      if (match) visible += 1;
    });
    archiveGroups.forEach((group) => {
      group.hidden = !group.querySelector("[data-archive-item]:not([hidden])");
    });
    archiveCount.textContent = `${visible} ${visible === 1 ? "Eintrag" : "Einträge"}`;
    archiveEmpty.hidden = visible !== 0;
  };
  archiveSearch.addEventListener("input", filterArchive);
  filterArchive();
}

const buildInventorySearch = document.getElementById("build-inventory-search");
const buildInventoryGroup = document.getElementById("build-inventory-group");
const buildInventoryState = document.getElementById("build-inventory-state");
const buildInventoryItems = [...document.querySelectorAll("[data-build-item]")];
const buildInventoryCount = document.getElementById("build-inventory-count");

if (buildInventorySearch && buildInventoryGroup && buildInventoryState) {
  const primaryGroups = new Set(["FOUNDATION", "PROCESSOR", "APPLICATION", "VISUAL_INSTRUMENT", "MISSING_ASSEMBLY"]);
  const filterBuildInventory = () => {
    const query = buildInventorySearch.value.trim().toLocaleLowerCase("de");
    const group = buildInventoryGroup.value;
    const state = buildInventoryState.value;
    let visible = 0;
    buildInventoryItems.forEach((item) => {
      const groupMatch = group === "all" || item.dataset.group === group || (group === "other" && !primaryGroups.has(item.dataset.group));
      const stateMatch = state === "all" || item.dataset.state === state;
      const queryMatch = !query || item.textContent.toLocaleLowerCase("de").includes(query);
      const match = groupMatch && stateMatch && queryMatch;
      item.hidden = !match;
      if (match) visible += 1;
    });
    buildInventoryCount.textContent = `${visible} / ${buildInventoryItems.length}`;
  };
  [buildInventorySearch, buildInventoryGroup, buildInventoryState].forEach((control) => {
    control.addEventListener(control === buildInventorySearch ? "input" : "change", filterBuildInventory);
  });
  filterBuildInventory();
}

const buildRegisterSearch = document.getElementById("build-register-search");
const buildRegisterMode = document.getElementById("build-register-mode");
const buildRegisterItems = [...document.querySelectorAll("[data-build-log-item]")];
const buildRegisterGroups = [...document.querySelectorAll("[data-build-log-group]")];
const buildRegisterCount = document.getElementById("build-register-count");
const buildRegisterEmpty = document.getElementById("build-register-empty");

if (buildRegisterSearch && buildRegisterMode) {
  const filterBuildRegister = () => {
    const query = buildRegisterSearch.value.trim().toLocaleLowerCase("de");
    const mode = buildRegisterMode.value;
    let visible = 0;
    buildRegisterItems.forEach((item) => {
      const match = (mode === "all" || item.dataset.mode === mode) && (!query || item.textContent.toLocaleLowerCase("de").includes(query));
      item.hidden = !match;
      if (match) visible += 1;
    });
    buildRegisterGroups.forEach((group) => {
      group.hidden = !group.querySelector("[data-build-log-item]:not([hidden])");
    });
    buildRegisterCount.textContent = `${visible} / ${buildRegisterItems.length}`;
    buildRegisterEmpty.hidden = visible !== 0;
  };
  buildRegisterSearch.addEventListener("input", filterBuildRegister);
  buildRegisterMode.addEventListener("change", filterBuildRegister);
  filterBuildRegister();
}

const achievementSnapshot = globalThis.NEXAH_ECOSYSTEM_ACHIEVEMENTS;

if (achievementSnapshot) {
  const number = new Intl.NumberFormat("de-DE");
  const bytes = (value) => {
    const units = ["B", "KB", "MB", "GB", "TB"];
    let amount = value;
    let unit = 0;
    while (amount >= 1000 && unit < units.length - 1) {
      amount /= 1000;
      unit += 1;
    }
    return `${new Intl.NumberFormat("de-DE", { maximumFractionDigits: unit > 2 ? 2 : 1 }).format(amount)} ${units[unit]}`;
  };
  const values = {
    asOf: achievementSnapshot.asOf,
    scope: achievementSnapshot.scope,
    caution: achievementSnapshot.caution,
    repositories: number.format(achievementSnapshot.git.repositoryCount),
    uniqueCommits: number.format(achievementSnapshot.git.uniqueCommits),
    commitSum: number.format(achievementSnapshot.git.commitSum),
    files: number.format(achievementSnapshot.filesystem.totals.files),
    bytes: bytes(achievementSnapshot.filesystem.totals.bytes),
    ...Object.fromEntries(Object.entries(achievementSnapshot.registers).map(([key, value]) => [key, number.format(value)])),
  };
  document.querySelectorAll("[data-achievement]").forEach((node) => {
    node.textContent = values[node.dataset.achievement] ?? "—";
  });

  const formatGrid = document.getElementById("format-grid");
  if (formatGrid) {
    const labels = { code: "Code + Web", documents: "Documents", data: "Data + Manifests", images: "Images", models3d: "3D Models", media: "Audio + Video", other: "Other" };
    const maximum = Math.max(...Object.values(achievementSnapshot.filesystem.groups).map((group) => group.bytes));
    formatGrid.innerHTML = Object.entries(achievementSnapshot.filesystem.groups).map(([key, group]) => `
      <article><header><strong>${labels[key]}</strong><span>${number.format(group.files)} files</span></header><div><i style="width:${Math.max(2, group.bytes / maximum * 100)}%"></i></div><p>${bytes(group.bytes)}</p></article>
    `).join("");
  }

  const repositoryRows = document.getElementById("repository-rows");
  if (repositoryRows) {
    repositoryRows.innerHTML = achievementSnapshot.git.repositories
      .sort((a, b) => b.commits - a.commits)
      .map((repository) => `<div class="repository-row" role="row"><span role="cell"><strong>${repository.name}</strong><small>${repository.path}</small></span><span role="cell">${number.format(repository.commits)}</span><span role="cell">${number.format(repository.trackedFiles)}</span><span role="cell" class="${repository.dirtyEntries ? "is-dirty" : "is-clean"}">${repository.dirtyEntries ? `${number.format(repository.dirtyEntries)} changes` : "clean"}</span></div>`)
      .join("");
  }
}

const achievementTabs = [...document.querySelectorAll("[data-achievement-tab]")];
const achievementPanels = [...document.querySelectorAll("[data-achievement-panel]")];

if (achievementTabs.length && achievementPanels.length) {
  const validIds = new Set(achievementPanels.map((panel) => panel.dataset.achievementPanel));
  const activateAchievementPanel = (id, { updateHash = false, focus = false } = {}) => {
    const nextId = validIds.has(id) ? id : achievementPanels[0].dataset.achievementPanel;
    achievementPanels.forEach((panel) => { panel.hidden = panel.dataset.achievementPanel !== nextId; });
    achievementTabs.forEach((tab) => {
      const selected = tab.dataset.achievementTab === nextId;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus({ preventScroll: true });
    });
    document.body.classList.add("is-tabbed");
    if (updateHash && window.location.hash !== `#${nextId}`) history.pushState(null, "", `#${nextId}`);
  };

  achievementTabs.forEach((tab, index) => {
    tab.addEventListener("click", (event) => {
      event.preventDefault();
      activateAchievementPanel(tab.dataset.achievementTab, { updateHash: true, focus: true });
    });
    tab.addEventListener("keydown", (event) => {
      const keyTargets = { ArrowLeft: index - 1, ArrowRight: index + 1, Home: 0, End: achievementTabs.length - 1 };
      if (!(event.key in keyTargets)) return;
      event.preventDefault();
      const nextIndex = (keyTargets[event.key] + achievementTabs.length) % achievementTabs.length;
      achievementTabs[nextIndex].click();
    });
  });

  window.addEventListener("hashchange", () => activateAchievementPanel(window.location.hash.slice(1)));
  activateAchievementPanel(window.location.hash.slice(1));
}
