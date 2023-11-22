function selectTab(tabName) {
  // Get all elements with the class 'badge2' and remove the class
  var badge2Elements = document.querySelectorAll(".badge2");
  for (var i = 0; i < badge2Elements.length; i++) {
    badge2Elements[i].classList.remove("badge2");
    badge2Elements[i].classList.add("badge3"); // Reset other tabs to badge3 class
  }

  // Get all elements with the class 'card-title2' and remove the class
  var cardTitle2Elements = document.querySelectorAll(".card-title2");
  for (var i = 0; i < cardTitle2Elements.length; i++) {
    cardTitle2Elements[i].classList.remove("card-title2");
    cardTitle2Elements[i].classList.add("card-title3"); // Reset other titles to card-title3 class
  }

  // Get the element corresponding to the selected tab and update its class
  var selectedTab = document.querySelector(
    ".badge3[onclick=\"selectTab('" + tabName + "')\"]"
  );
  selectedTab.classList.remove("badge3");
  selectedTab.classList.add("badge2");

  // Get the element corresponding to the selected tab title and update its class
  var selectedTitle = selectedTab.querySelector(".card-title3");
  selectedTitle.classList.remove("card-title3");
  selectedTitle.classList.add("card-title2");

  // Update the selected_tab variable
  var selected_tab = document.getElementById("cards-row");
  selected_tab.innerHTML = tabName;

  // Add your logic to handle the selected tab, for example, updating content
  // You can add more logic here based on the selected tab
  // For now, let's just log the selected tab name
  console.log("Selected tab:", tabName);
}

window.onload = function () {
  selectTab('recent');
};