let responsiveWidth = 600;
const listElement = document.querySelector(".main-container");
const selectElement = document.getElementById("pathSelect");

function updateSelectOptions() {
  selectElement.innerHTML = "";
  const listItems = listElement.querySelectorAll(".path");
  let index = 1;
  for (const listItem of listItems) {
    let title = listItem.querySelector(".path_title").value;
    const pathTitle = title !== "" ? title : `이름없는 패스${index}`;
    const option = document.createElement("option");
    const classNames = listItem.className.split(" ");
    for (const className of classNames) {
      if (className.startsWith("path_")) {
        option.value = className.slice(5);
        break;
      }
    }
    option.textContent = pathTitle;

    // detail 페이지일때는 이렇게.
    if (typeof pathTitle == "undefined") {
      if (listItem.querySelector(".path_title").innerHTML == "") {
        option.textContent = `이름없는 패스${index}`;
      } else {
        option.textContent = listItem.querySelector(".path_title").innerHTML;
      }
    }
    selectElement.appendChild(option);
    index++;
  }
}

selectElement.addEventListener("change", () => {
  const selectedOption = selectElement.options[selectElement.selectedIndex];
  const selectedValue = selectedOption.value;
  const listItems = listElement.querySelectorAll(".path");
  // Hide all list items
  listItems.forEach((item) => (item.style.display = "none"));

  // Show the selected list item
  const selectedItem = Array.from(listItems).find((item) =>
    item.classList.contains(`path_${selectedValue}`)
  );
  if (selectedItem) {
    selectedItem.style.display = "block";
  }
});

function changeDisplay(id) {
  if (window.innerWidth <= responsiveWidth) {
    var optionElements = selectElement.getElementsByTagName("option");
    for (var i = 0; i < optionElements.length; i++) {
      if (optionElements[i].value === `${id}`) {
        optionElements[i].selected = true;
        var changeEvent = new Event("change", { bubbles: true });
        selectElement.dispatchEvent(changeEvent);
        break;
      }
    }
  }
}

const listItems = listElement.querySelectorAll(".path");
// console.log(listItems);

if (window.innerWidth <= responsiveWidth) {
  listItems.forEach((item) => (item.style.display = "none"));
  listItems[0].style.display = "block";
  updateSelectOptions();
} else {
  // listItems.forEach((item) => (item.style.display = "block"));
}

// 개발용 이벤트 리스너.
window.addEventListener("resize", () => {
  const listItems = listElement.querySelectorAll(".path");
  if (window.innerWidth <= responsiveWidth) {
    listItems.forEach((item) => (item.style.display = "none"));
    listItems[0].style.display = "block";
    updateSelectOptions();
  } else {
    // listItems.forEach((item) => (item.style.display = "block"));
  }
});
