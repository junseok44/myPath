// addPathData 부분에서 isNew isEdited를 추가해주는것 빼고는 동일.
function createPathAndDisplay(prevPathId) {
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

// 동일함.
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

// writeUtils와 다른점은 deletedIds에 추가하는것. 그런데 에러있다.
function handleDeleteItem(stepId) {
  const targetNode = document.querySelector(`.step_${stepId}`);

  targetNode.classList.add("fadeout");
  setTimeout(() => {
    targetNode.parentNode.removeChild(targetNode);
  }, 300);

  steps = steps.filter((step) => step.id !== stepId);
  deletedIds.push(stepId);
}

// deletedPath에 추가하는 거 빼고는 동일. 이것도 순서 보정을 안해줬다.
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
        <button type="button" onclick="createPathAndDisplay()" class="add_new-btn btn">
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
