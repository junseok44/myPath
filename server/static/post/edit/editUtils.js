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

function handleAddPath(prevPathId) {
  let id = uuid.v4();
  addPathNode(prevPathId, id);

  const prevPathItem = paths.find((path) => path.id == prevPathId);
  if (prevPathItem) {
    paths = paths.map((path) =>
      path.order >= prevPathItem.order + 1
        ? {
            ...path,
            order: path.order + 1,
            isEdited: true,
          }
        : path
    );

    paths.push({
      id: id,
      order: prevPathItem.order + 1,
      title: ``,
      isNew: true,
      isEdited: false,
    });
  } else {
    paths.push({ id: id, order: 1, title: ``, isNew: true, isEdited: false });
  }

  updateSelectOptions();
  changeDisplay(id);
}

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

function handleDeleteItem(stepId) {
  const step = document.querySelector(`.step_${stepId}`);

  step.classList.add("fadeout");
  setTimeout(() => {
    step.parentNode.removeChild(step);
  }, 300);

  steps = steps.filter((step) => step.id !== stepId);
  deletedIds.push(stepId);
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

function handleDeletePath(targetPathId) {
  const main = document.querySelector(".main-container");
  const target = main.querySelector(`.path_${targetPathId}`);

  var optionElements = selectElement.getElementsByTagName("option");
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
      <button type="button" onclick="handleAddPath()" class="add_new-btn btn">
      옆에 새로운 패스 추가하기
      </button>
      `;
    }
    updateSelectOptions();
    if (targetOption) changeDisplay(targetOption.value);
  }, 300);

  deletedPaths.push(targetPathId);
  // 누구야 이거 느낌표 빼놓은거...
  paths = paths.filter((path) => path.id !== targetPathId);
  steps = steps.filter((step) => step.pathId !== targetPathId);
}
