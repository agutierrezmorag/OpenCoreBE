const newsItems = document.querySelectorAll(".news-item");
let currentIndex = 0;
const itemsPerPage = 3;

function showItems(startIndex) {
  for (let i = 0; i < newsItems.length; i++) {
    if (i >= startIndex && i < startIndex + itemsPerPage) {
      newsItems[i].style.display = "inline-block";
    } else {
      newsItems[i].style.display = "none";
    }
  }
}

function showNextItems() {
  const newIndex = Math.min(
    currentIndex + itemsPerPage,
    newsItems.length - itemsPerPage
  );
  currentIndex = newIndex;
  showItems(currentIndex);
}

function showPreviousItems() {
  const newIndex = Math.max(currentIndex - itemsPerPage, 0);
  currentIndex = newIndex;
  showItems(currentIndex);
}

document.addEventListener("DOMContentLoaded", () => {
  showItems(currentIndex);

  // Event listeners para los botones de flecha
  document.querySelector(".adelante").addEventListener("click", showNextItems);
  document.querySelector(".atras").addEventListener("click", showPreviousItems);
});
