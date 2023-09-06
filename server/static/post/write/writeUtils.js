// 이 부분은 테스트 용입니다. runserver시 주석 처리해주세요
// 파일 중간중간에 require가 섞여있는데 주석처리해주세요. ctrl+f로 다 찾아서.
// const uuid = require("uuid");

// function getPathsAndSteps() {
//   return { paths, steps };
// }

// function resetPathsAndSteps() {
//   paths = [];
//   steps = [];
// }

// module.exports = {
//   getPathsAndSteps: getPathsAndSteps,
//   resetPathsAndSteps: resetPathsAndSteps,
//   createPathAndDisplay: createPathAndDisplay,
//   addPathData: addPathData,
//   handleDeletePath: handleDeletePath,
//   handleAddStep: handleAddStep,
//   handleChangePathTitle: handleChangePathTitle,
//   handleDeleteItem: handleDeleteItem,
//   moveItemUp: moveItemUp,
//   moveItemDown: moveItemDown,
// };

// 여기까지

let paths = [];
let steps = [];

function createPathAndDisplay(prevPathId) {
  let id = uuid.v4();
  addPathNode(prevPathId, id);
  addPathData(prevPathId, id);

  // const { updateSelectOptions, changeDisplay } = require("../responsivePath");

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

// 이 부분은 테스트 용입니다. runsever시 주석 처리해주세요.
// const { addStepNode, addPathNode } = require("../addNode_by_javascript");
// 여기까지.
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
