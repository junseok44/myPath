function handleChangePathTitle(e, pathId) {
  paths = paths.map((path) =>
    path.id == pathId
      ? { ...path, title: e.target.value, isEdited: true }
      : path
  );

  updateSelectOptions();
  changeDisplay(pathId);
}

function addPathNode(prevPathId, id) {
  const main = document.querySelector(".main");
  const NewBtn = document.querySelector(".add_new-btn");
  if (NewBtn) {
    NewBtn.parentNode.removeChild(NewBtn);
  }
  let isColumnMode = main.classList.contains("column-mode");

  li = document.createElement("li");
  li.classList.add(`path`);
  li.classList.add(`path_${id}`);
  li.innerHTML += `
        <input placeholder="패스 이름 입력..." type="text" class="path_title" onchange="handleChangePathTitle(event,'${id}')">
        <button type="button" onclick="handleAddPath('${id}')">패스 추가하기</button>
        <button type="button" onclick="handleDeletePath('${id}')">패스 삭제하기</button>

        <div class="step_container ${
          isColumnMode ? "" : " container_row-mode"
        }">
                </div>
        <button type="button" onclick="handleAddStep('${id}')" class="item_add-btn">
              스텝 추가하기
            </button>
        `;
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
  section.classList.add(`step`);
  section.classList.add(`step_${id}`);
  section.innerHTML = `
                <div>
                  <p class="title"></p>
                  <p class="desc"></p>
                  <button type="button" onclick="moveItemUp('${id}')">위로 올리기</button>
                  <button type="button" onclick="moveItemDown('${id}')">밑으로 내리기</button>
                  <button type="button" onclick="handleDeleteItem('${id}')">삭제하기</button>
                  <button
                    class="edit-btn"
                    type="button"
                    onclick="handleToggleModal('${id}')"
                  >
                    편집하기
                  </button>
                </div>
                <div class="modal__overlay hidden">

                <div class="step__edit-modal modal_${id} hidden">
                  <input type="text" class="title" />
                  <textarea class="desc"></textarea>
                  <div>
                    <button type="button" onClick="handleToggleModal('${id}')">취소</button>
                    <button type="button" onclick="handleSaveValue('${id}')">변경</button>
                  </div>
                  </div>
                  </div>
          `;
  stepContainer.appendChild(section);
}
