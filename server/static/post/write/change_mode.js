//테스트용입니다. runserver시 주석처리해주세요.

module.exports = {
  toggleMode,
  checkmode,
};

// 여기까지.

let main = document.querySelector(".main-container");
const modeBtn = document.querySelector(".mode-btn");

checkmode();

function checkmode() {
  main = document.querySelector(".main-container");
  if (main.classList.contains("col-mode")) {
    modeBtn.innerText = "가로모드로 바꾸기";
    return "col";
  } else {
    modeBtn.innerText = "세로모드로 바꾸기";
    return "row";
  }
}

function toggleMode() {
  main = document.querySelector(".main-container");
  const allContainer = document.querySelectorAll(".step_container");
  for (let item of allContainer) {
    item.classList.toggle("container_row-mode");
  }
  main.classList.toggle("col-mode");
  checkmode();
}
