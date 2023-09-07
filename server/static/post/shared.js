function handleAddStep(targetPathId) {
  let id = uuid.v4();
  addStepNode(targetPathId, id);

  steps.push({
    id,
    pathId: targetPathId,
    order: steps.filter((step) => step.pathId == targetPathId).length + 1,
    isNew: true,
    isEdited: false,
    title: "",
    desc: "",
  });
}

function handleChangePathTitle(e, pathId) {
  // const { updateSelectOptions, changeDisplay } = require("../responsivePath");

  paths = paths.map((path) =>
    path.id == pathId
      ? { ...path, title: e.target.value, isEdited: true }
      : path
  );

  updateSelectOptions();
  changeDisplay(pathId);
}

function handleDeletePath(targetPathId) {
  const main = document.querySelector(".main-container");
  const target = main.querySelector(`.path_${targetPathId}`);
  // const { updateSelectOptions, changeDisplay } = require("../responsivePath");
  // 이 부분 로직 분리하기
  // 내가 볼때 지우고 나서 다음 option을 뭐로 설정할지에 관한 로직임.
  const selectElement = document.querySelector("#pathSelect");
  var specificOptionIndex = Array.from(selectElement.options).findIndex(
    function (option) {
      return option.value === targetPathId;
    }
  );
  if (specificOptionIndex == 0) {
    specificOptionIndex = 2;
  }
  var targetOption = selectElement.options[specificOptionIndex - 1];

  target.classList.add("fadeout");
  setTimeout(() => {
    main.removeChild(target);
    if (main.childElementCount == 0) {
      main.innerHTML = `
        <button type="button" onclick="createPathAndDisplay()" class="btn add_new-btn writePage__btn">
          내 패스 만들기
        </button>
        `;
    }

    updateSelectOptions();
    if (targetOption) changeDisplay(targetOption.value);
  }, 300);

  targetOrder = paths.find((path) => path.id == targetPathId).order;

  paths = paths.map((path) => {
    if (path.order > targetOrder) {
      path.order -= 1;
    }
    return path;
  });

  paths = paths.filter((path) => path.id !== targetPathId);
  steps = steps.filter((step) => step.pathId !== targetPathId);
}

function handleDeleteItem(targetStepId) {
  const targetNode = document.querySelector(`.step_${targetStepId}`);

  targetNode.classList.add("fadeout");
  setTimeout(() => {
    targetNode.parentNode.removeChild(targetNode);
  }, 300);
  // targetNode.parentNode.removeChild(targetNode);

  const targetStep = steps.find((step) => step.id == targetStepId);

  steps = steps.map((step) => {
    if (step.colId == targetStep.colId && step.order > targetStep.order) {
      step.order -= 1;
      step.isEdited = true;
    }

    return step;
  });
  steps.splice(
    steps.findIndex((step) => step.id == targetStepId),
    1
  );
}
