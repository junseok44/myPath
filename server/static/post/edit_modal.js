function showAllSteps() {
  console.log(steps);
}
// 현재 수정중인것. modal이 step 아래로 가려지게 되는 문제.

function toggleModal(id) {
  const modal = document.querySelector(`.modal_${id}`);
  if (modal.parentElement.classList.contains("hidden")) {
    hideAllModal();
    modal.parentElement.classList.remove("hidden");
    modal.parentElement.parentElement.parentElement.parentElement.parentElement.style.zIndex = 1000;
    modal.parentElement.parentElement.style.zIndex = 500;
  } else {
    modal.parentElement.classList.add("hidden");
    modal.parentElement.parentElement.parentElement.parentElement.parentElement.style.zIndex =
      "auto";
    modal.parentElement.parentElement.style.zIndex = "auto";
  }
}

// 내가 원하는것.
// 클릭시 일단 모든 모달을 숨기고 -> 모달을 보여준다.
// 그 다음 클릭시 다시 모든 모달을 숨긴다.

function hideModal(id) {
  const modal = document.querySelector(`.modal_${id}`);
  modal.parentElement.classList.add("hidden");
}

function hideAllModal() {
  const modals = document.querySelectorAll(".step__edit-modal");

  const steps = document.querySelectorAll(".step");
  steps.forEach((step) => {
    step.style.zIndex = "auto";
  });
  modals.forEach((modal) => {
    if (!modal.parentElement) return;
    modal.parentElement.classList.add("hidden");
    modal.parentElement.parentElement.parentElement.parentElement.parentElement.style.zIndex =
      "auto";
  });
}

function handleSaveValue() {
  hideAllModal();
}
