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
    buildRegisterCount.textContent = `${visible} / ${buildRegisterItems.length}`;
    buildRegisterEmpty.hidden = visible !== 0;
  };
  buildRegisterSearch.addEventListener("input", filterBuildRegister);
  buildRegisterMode.addEventListener("change", filterBuildRegister);
  filterBuildRegister();
}
