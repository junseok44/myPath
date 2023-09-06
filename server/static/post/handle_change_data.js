// 이 부분은 테스트 용입니다. runserver시 주석 처리해주세요
// 중간에 require 숨어있습니다. ctrl+f로 찾아서 주석처리해주세요.
// module.exports = {
//   handleChangeStepDesc,
//   handleChangeStepImage,
//   handleChangeStepTitle,
// };

//

function handleChangeStepTitle(stepId) {
  // let steps = require("./write/writeUtils").getPathsAndSteps().steps;
  const stepNode = document.querySelector(`.step_${stepId}`);
  const titleInput = stepNode.querySelector(".title");
  const step = steps.find((step) => step.id == stepId);
  step.title = titleInput.value;
  step.isEdited = true;
}

function handleChangeStepDesc(stepId) {
  // let steps = require("./write/writeUtils").getPathsAndSteps().steps;
  const stepNode = document.querySelector(`.step_${stepId}`);
  const descInput = stepNode.querySelector(".desc");

  const step = steps.find((step) => step.id == stepId);
  step.desc = descInput.value;
  step.isEdited = true;
}

function handleChangeStepImage(stepId) {
  // let steps = require("./write/writeUtils").getPathsAndSteps().steps;

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

function moveItemUp(stepId) {
  const targetStep = steps.find((step) => step.id == stepId);
  const pathId = targetStep.pathId;
  const target = document.querySelector(`.step_${stepId}`);
  const container = document.querySelector(`.path_${pathId} .step_container`);
  const previousNode = target.previousElementSibling;
  if (!previousNode) return;

  container.removeChild(target);
  container.insertBefore(target, previousNode);

  const movedStep = steps.find(
    (step) => step.pathId == pathId && step.order == targetStep.order - 1
  );
  // targetStep은 order를 -1 . movedStep은 order를 1.
  steps = steps.map((step) => {
    if (step.id == movedStep.id)
      return {
        ...step,
        order: step.order + 1,
        isEdited: true,
      };
    else if (step.id === targetStep.id)
      return {
        ...step,
        order: step.order - 1,
        isEdited: true,
      };
    else return step;
  });
}

function moveItemDown(stepId) {
  const targetStep = steps.find((step) => step.id == stepId);
  const pathId = targetStep.pathId;
  const target = document.querySelector(`.step_${stepId}`);
  const container = document.querySelector(`.path_${pathId} .step_container`);
  const nextNode = target.nextElementSibling;

  if (!nextNode) return;
  const next_nextNode = nextNode.nextElementSibling;
  container.removeChild(target);

  if (next_nextNode) {
    container.insertBefore(target, next_nextNode);
  } else {
    container.appendChild(target);
  }

  const movedStep = steps.find(
    (step) => step.pathId == pathId && step.order == targetStep.order + 1
  );

  steps = steps.map((step) => {
    if (step.id == movedStep.id)
      return {
        ...step,
        order: step.order - 1,
        isEdited: true,
      };
    else if (step.id === targetStep.id)
      return {
        ...step,
        order: step.order + 1,
        isEdited: true,
      };
    else return step;
  });
}
