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
