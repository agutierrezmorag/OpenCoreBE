document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('toggle-filters').addEventListener('click', function() {
    var filters = document.getElementById('filters');
    if (filters.style.display === 'none') {
      filters.style.display = 'block';
    } else {
      filters.style.display = 'none';
    }
  });
});

const prevRecent = document.getElementById("prev-btn-recent");
const nextRecent = document.getElementById("next-btn-recent");
const listRecent = document.getElementById("item-list-recent");

const prevNeutral = document.getElementById("prev-btn-neutral");
const nextNeutral = document.getElementById("next-btn-neutral");
const listNeutral = document.getElementById("item-list-neutral");

const itemWidth = 300;
const padding = 20;

prevRecent.addEventListener("click", () => {
  listRecent.scrollLeft -= itemWidth + padding;
});

nextRecent.addEventListener("click", () => {
  listRecent.scrollLeft += itemWidth + padding;
});

prevNeutral.addEventListener("click", () => {
  listNeutral.scrollLeft -= itemWidth + padding;
});

nextNeutral.addEventListener("click", () => {
  listNeutral.scrollLeft += itemWidth + padding;
});
