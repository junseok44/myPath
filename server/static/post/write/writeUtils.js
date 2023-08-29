// 이 부분은 테스트 용입니다. runserver시 주석 처리해주세요
const uuid = require("uuid");
const { addPathNode } = require("../addNode");
const updateSelectOptions = jest.fn();
const changeDisplay = jest.fn();
// 여기까지

let paths = [];
let steps = [];

// 이 부분은 테스트 용입니다. runsever시 주석 처리해주세요.
module.exports = {
  createPathAndDisplay: createPathAndDisplay,
  addPathData: addPathData,
  paths: paths,
  steps: steps,
};
// 여기까지.

function createPathAndDisplay(prevPathId) {
  let id = uuid.v4();
  addPathNode(prevPathId, id);
  addPathData(prevPathId, id);

  updateSelectOptions();
  changeDisplay(id);
}

function addPathData(prevPathId, id) {
  const prevPathItem = paths.find((path) => path.id == prevPathId);
  if (prevPathItem) {
    paths = paths.map((path) =>
      // 추가하려는 패스보다 오른쪽에 있나
      path.order >= prevPathItem.order + 1
        ? {
            ...path,
            order: path.order + 1,
          }
        : path
    );
    paths.push({
      id: id,
      order: prevPathItem.order + 1,
      title: ``,
    });
  } else {
    paths.push({ id: id, order: 1, title: `` });
  }
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
      <button type="button" onclick="createPathAndDisplay()" class="btn add_new-btn writePage__btn">
        내 패스 만들기
      </button>
      `;
    }

    updateSelectOptions();
    if (targetOption) changeDisplay(targetOption.value);
  }, 300);

  paths = paths.filter((path) => path.id !== targetPathId);
  steps = steps.filter((step) => step.pathId !== targetPathId);
}

function moveItemUp(stepId) {
  const targetStep = steps.find((step) => step.id == stepId);
  const pathId = targetStep.pathId;
  const target = document.querySelector(`.step_${stepId}`);
  const container = document.querySelector(`.path_${pathId} .step_container`);
  const previousNode = target.previousSibling;
  if (!target.previousSibling) return;

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
      };
    else if (step.id === targetStep.id)
      return {
        ...step,
        order: step.order - 1,
      };
    else return step;
  });
}

function moveItemDown(stepId) {
  const targetStep = steps.find((step) => step.id == stepId);
  const pathId = targetStep.pathId;
  const target = document.querySelector(`.step_${stepId}`);
  const container = document.querySelector(`.path_${pathId} .step_container`);
  const nextNode = target.nextSibling;
  if (!nextNode) return;
  const next_nextNode = nextNode.nextSibling;

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
      };
    else if (step.id === targetStep.id)
      return {
        ...step,
        order: step.order + 1,
      };
    else return step;
  });
}

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

function handleChangePathTitle(e, pathId) {
  paths = paths.map((path) =>
    path.id == pathId
      ? { ...path, title: e.target.value, isEdited: true }
      : path
  );

  updateSelectOptions();
  changeDisplay(pathId);
}

/*
  path의 구조는 다음과 같습니다.
  {
    id: uuid,
    order: 1,
    title: "패스 제목",
  }

*/
/*
  step의 구조는 다음과 같습니다.
  {
    id: uuid,
    pathId: uuid,
    order: 1,
    isNew: true,
    isEdited: false,
    title: "스텝 제목",
    desc: "스텝 설명",
    image: "이미지 데이터",
  }

*/
