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
