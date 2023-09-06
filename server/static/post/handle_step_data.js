function handleChangeStepTitle(stepId) {
  const stepNode = document.querySelector(`.step_${stepId}`);
  const titleInput = stepNode.querySelector(".title");

  const step = steps.find((step) => step.id == stepId);
  step.title = titleInput.value;
  step.isEdited = true;
}

function handleChangeStepDesc(stepId) {
  const stepNode = document.querySelector(`.step_${stepId}`);
  const descInput = stepNode.querySelector(".desc");

  const step = steps.find((step) => step.id == stepId);
  step.desc = descInput.value;
  step.isEdited = true;
}

function handleChangeStepImage(stepId) {
  const stepNode = document.querySelector(`.step_${stepId}`);
  const imageInput = stepNode.querySelector(".imageInput");
  const imageFile = imageInput.files[0];
  const step = steps.find((step) => step.id == stepId);

  if (imageFile) {
    const reader = new FileReader();
    reader.onload = async (event) => {
      imageData = event.target.result;
      step.image = imageData;
    };
    reader.readAsDataURL(imageFile);
  }
  step.isEdited = true;
}
