function handleToggleModal(id) {
  const modal = document.querySelector(`.modal_${id}`);
  modal.classList.toggle("hidden");
  modal.parentElement.classList.toggle("hidden");
  // 토글시 다른 아이템들은 다 숨겨지도록 해야함.

  titleVal = descVal = document.querySelector(`.step_${id} .title`).innerText;
  descVal = descVal = document.querySelector(`.step_${id} .desc`).innerText;

  const titleForm = modal.querySelector(".title");
  const descForm = modal.querySelector(".desc");

  titleForm.value = titleVal;
  descForm.value = descVal;
}

function handleSaveValue(id) {
  const modal = document.querySelector(`.modal_${id}`);
  const titleForm = modal.querySelector(".title");
  const descForm = modal.querySelector(".desc");

  const titleNode = document.querySelector(`.step_${id} .title`);
  const descNode = document.querySelector(`.step_${id} .desc`);

  titleNode.innerText = titleForm.value;
  descNode.innerText = descForm.value;
  modal.classList.toggle("hidden");
  modal.parentElement.classList.toggle("hidden");

  step = steps.find((step) => step.id == id);
  step.title = titleForm.value;
  step.desc = descForm.value;
  step.isEdited = true;
}