function showAllSteps() {
  console.log(steps);
}

function showModal(id) {
  hideAllModal();
  const modal = document.querySelector(`.modal_${id}`);
  modal.parentElement.classList.remove("hidden");
}

function hideModal(id) {
  const modal = document.querySelector(`.modal_${id}`);
  modal.parentElement.classList.add("hidden");
}

function hideAllModal() {
  const modals = document.querySelectorAll(".step__edit-modal");
  modals.forEach((modal) => {
    if (!modal.parentElement) return;
    modal.parentElement.classList.add("hidden");
  });
}

function handleSaveValue() {
  hideAllModal();
}
