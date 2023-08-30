// 이 부분은 테스트용입니다. runserver시 주석처리해주세요.
const WriteUtils = require("./write/writeUtils");
module.exports = {
  addPathNode,
  addStepNode,
};
// 여기까지

function addPathNode(prevPathId, id) {
  const NewBtn = document.querySelector(".add_new-btn");
  if (NewBtn) {
    NewBtn.parentNode.removeChild(NewBtn);
  }
  // 가로모드인지 세로모드인지.
  const main = document.querySelector(".main-container");
  let isColumnMode = main.classList.contains("col-mode");

  const li = document.createElement("li");
  li.classList.add("path", `path_${id}`);

  const span = document.createElement("span");
  span.classList.add("path_intro");

  const input = document.createElement("input");
  input.maxLength = 10;
  input.placeholder = "패스 제목 입력...";
  input.type = "text";
  input.classList.add("writePage-input", "path_title");
  input.addEventListener("change", (event) =>
    WriteUtils.handleChangePathTitle(event, id)
  );

  const addButton = document.createElement("button");
  addButton.type = "button";
  addButton.classList.add("secondary-btn", "path-add-btn");
  addButton.textContent = "패스+";
  addButton.addEventListener("click", () =>
    WriteUtils.createPathAndDisplay(id)
  );

  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.classList.add("step-btn");
  deleteButton.addEventListener("click", () => WriteUtils.handleDeletePath(id));

  const deleteIcon = document.createElement("i");
  deleteIcon.classList.add("fa-solid", "fa-trash");
  deleteButton.appendChild(deleteIcon);

  span.appendChild(input);
  span.appendChild(addButton);
  span.appendChild(deleteButton);

  li.appendChild(span);

  // 여기까지 path_intro 추가.

  const stepContainerWithBtn = document.createElement("div");
  stepContainerWithBtn.classList.add("step_container_w_btn");

  const stepContainer = document.createElement("div");
  stepContainer.classList.add("step_container");

  if (!isColumnMode) {
    stepContainer.classList.add("container_row-mode");
  }
  stepContainerWithBtn.appendChild(stepContainer);

  const stepAddButton = document.createElement("button");
  stepAddButton.type = "button";
  stepAddButton.classList.add("step-add-btn", "item_add-btn");
  stepAddButton.textContent = "+";
  stepAddButton.addEventListener("click", () => handleAddStep(id));

  stepContainerWithBtn.appendChild(stepAddButton);

  li.appendChild(stepContainerWithBtn);

  if (prevPathId) {
    const prevPath = document.querySelector(`.path_${prevPathId}`);
    if (prevPath.nextSibling) {
      main.insertBefore(li, prevPath.nextSibling);
    } else {
      main.append(li);
    }
  } else {
    main.append(li);
  }
}

function addStepNode(targetPathId, id) {
  const stepContainer = document.querySelector(
    `.path_${targetPathId} .step_container`
  );

  const section = document.createElement("section");
  section.classList.add("step", `step_${id}`);

  const stepContent = document.createElement("div");
  stepContent.classList.add("step-content");

  const titleInput = document.createElement("input");
  titleInput.maxLength = 20;
  titleInput.onchange = () => handleChangeStepTitle(id);
  titleInput.type = "text";
  titleInput.classList.add("writePage-input", "title");
  titleInput.placeholder = "스텝 제목 입력...";

  const descTextarea = document.createElement("textarea");
  descTextarea.maxLength = 500;
  descTextarea.onchange = () => handleChangeStepDesc(id);
  descTextarea.classList.add("writePage-input", "desc");
  descTextarea.id = "step-desc";
  descTextarea.placeholder = "스텝 내용 입력...";

  const imageInput = document.createElement("input");
  imageInput.type = "file";
  imageInput.classList.add("imageInput");
  imageInput.onchange = () => handleChangeStepImage(id);

  stepContent.appendChild(titleInput);
  stepContent.appendChild(descTextarea);
  stepContent.appendChild(imageInput);

  const stepBtnContainer = document.createElement("div");
  stepBtnContainer.classList.add("step-btn-container");

  const moveUpButton = createStepButton("moveItemUp", id, "fa-angles-up");
  const moveDownButton = createStepButton("moveItemDown", id, "fa-angles-down");
  const deleteButton = createStepButton("handleDeleteItem", id, "fa-trash");

  stepBtnContainer.appendChild(moveUpButton);
  stepBtnContainer.appendChild(moveDownButton);
  stepBtnContainer.appendChild(deleteButton);

  const modalOverlay = document.createElement("div");
  modalOverlay.classList.add("modal__overlay", "hidden");

  const editModal = document.createElement("div");
  editModal.classList.add(`step__edit-modal`, `modal_${id}`, "hidden");

  const modalTitleInput = document.createElement("input");
  modalTitleInput.type = "text";
  modalTitleInput.classList.add("title");

  const modalDescTextarea = document.createElement("textarea");
  modalDescTextarea.classList.add("desc");

  const modalImageInput = document.createElement("input");
  modalImageInput.type = "file";
  modalImageInput.classList.add("imageInput");

  const modalButtonContainer = document.createElement("div");

  const cancelButton = document.createElement("button");
  cancelButton.type = "button";
  cancelButton.classList.add("btn");
  cancelButton.onclick = () => handleToggleModal(id);
  cancelButton.textContent = "취소";

  const saveButton = document.createElement("button");
  saveButton.type = "button";
  saveButton.classList.add("btn");
  saveButton.onclick = () => handleSaveValue(id);
  saveButton.textContent = "등록";

  modalButtonContainer.appendChild(cancelButton);
  modalButtonContainer.appendChild(saveButton);

  editModal.appendChild(modalTitleInput);
  editModal.appendChild(modalDescTextarea);
  editModal.appendChild(modalImageInput);
  editModal.appendChild(modalButtonContainer);

  modalOverlay.appendChild(editModal);

  section.appendChild(stepContent);
  section.appendChild(stepBtnContainer);
  section.appendChild(modalOverlay);

  stepContainer.appendChild(section);
}

function createStepButton(clickHandler, id, icon) {
  const button = document.createElement("button");
  button.type = "button";
  button.classList.add("step-btn");
  button.onclick = () => window[clickHandler](id);
  const iconElement = document.createElement("i");
  iconElement.classList.add("fa-solid", `fa-${icon}`);
  button.appendChild(iconElement);
  return button;
}

/*
현재 step의 구조는 다음과 같습니다.
                <div class="step-content">
                  <input maxlength="20" onchange="handleChangeStepTitle('${id}')" type="text" class="writePage-input title" placeholder="스텝 제목 입력..." / >
                  <textarea maxlength="500" onchange="handleChangeStepDesc('${id}')" class="writePage-input desc" id="step-desc" placeholder="스텝 내용 입력..." ></textarea>
                  <input type="file" class="imageInput" onchange="handleChangeStepImage('${id}')" />
                </div>
                <div class="step-btn-container">
                  <button type="button" class="step-btn" onclick="moveItemUp('${id}')"><i class="fa-solid fa-angles-up"></i></button>
                  <button type="button" class="step-btn" onclick="moveItemDown('${id}')"><i class="fa-solid fa-angles-down"></i></button>
                  <button type="button" class="step-btn" onclick="handleDeleteItem('${id}')"><i class="fa-solid fa-trash"></i></button>
                </div>
                <div class="modal__overlay hidden">
                  <div class="step__edit-modal modal_${id} hidden">
                    <input type="text" class="title" />
                    <textarea class="desc"></textarea>
                    <input type="file" class='imageInput' />
                    <div>
                      <button type="button" class="btn" onClick="handleToggleModal('${id}')">취소</button>
                      <button type="button" class="btn" onclick="handleSaveValue('${id}')">등록</button>
                    </div>
                  </div>
                </div>
        
*/

/*

현재 패스의 구조는 다음과 같습니다.

if (isColumnMode) {
    li.innerHTML += `
    <span class="path_intro">
    <input maxlength="10" placeholder="패스 제목 입력..." type="text" class="writePage-input path_title" onchange="handleChangePathTitle(event,'${id}')">
    <button type="button" class="secondary-btn path-add-btn" onclick="createPathAndDisplay('${id}')">패스+</button>
    <button type="button" class="step-btn" onclick="handleDeletePath('${id}')"><i class="fa-solid fa-trash"></i></button>
    </span>
    <div class="step_container_w_btn">
    <div class="step_container ${isColumnMode ? "" : " container_row-mode"}">
    </div>
    <button type="button" class="step-add-btn" onclick="handleAddStep('${id}')" class="item_add-btn">+</button>
    </div>
    `;
  } else {
    li.innerHTML += `
    <span class="path_intro">
    <input maxlength="10" placeholder="패스 제목 입력..." type="text" class="path_title writePage-input" onchange="handleChangePathTitle(event,'${id}')">
    <button type="button" class="secondary-btn path-add-btn" onclick="handleAddPath('${id}')">패스+</button>
    <button type="button" class="step-btn" onclick="handleDeletePath('${id}')"><i class="fa-solid fa-trash"></i></button>
    </span>
    <div class="step_container_w_btn">
    <div class="step_container ${
      isColumnMode ? "" : " container_row-mode"
    }"></div>
    <button type="button" class="step-add-btn" onclick="handleAddStep('${id}')" class="item_add-btn">+</button>
    </div>
    `;
  }


*/
