// 이 부분은 테스트용입니다. runserver시 주석 처리해주세요.
// module.exports = {
//   updateSelectOptions,
//   changeDisplay,
// };
//

let responsiveWidth = 900;
const listElement = document.querySelector(".main-container");
const selectElement = document.getElementById("pathSelect");

// 현재 존재하는 path들의 데이터를 바탕으로 option을 생성함.
function updateSelectOptions() {
  selectElement.innerHTML = "";
  const listItems = listElement.querySelectorAll(".path");
  let index = 1;
  for (const listItem of listItems) {
    let title = listItem.querySelector(".path_title").value;
    const pathTitle = title !== "" ? title : `이름없는 패스${index}`;
    const option = document.createElement("option");
    const classNames = listItem.className.split(" ");
    // 패스의 id를 option의 value로 설정함.
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

// 해당 option으로 change가 발생할시 다른거 다 숨기고 그 해당 path만 보여줌
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

// 옵션들 중에서 value가 id인 옵션을 선택하고, change 이벤트를 발생시킴.
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

if (window.innerWidth <= responsiveWidth) {
  listItems.forEach((item) => (item.style.display = "none"));
  if (listItems.length > 0) listItems[0].style.display = "block";

  updateSelectOptions();
}

// 개발용 이벤트 리스너.
window.addEventListener("resize", () => {
  const listItems = listElement.querySelectorAll(".path");
  if (window.innerWidth <= responsiveWidth) {
    listItems.forEach((item) => (item.style.display = "none"));
    if (listItems.length > 0) listItems[0].style.display = "block";
    updateSelectOptions();
  } else {
    // listItems.forEach((item) => (item.style.display = "block"));
  }
});
