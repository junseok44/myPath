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
  const main = document.querySelector(".main-container");
  const NewBtn = document.querySelector(".add_new-btn");
  if (NewBtn) {
    NewBtn.parentNode.removeChild(NewBtn);
  }
  let isColumnMode = main.classList.contains("col-mode");

  li = document.createElement("li");
  li.classList.add(`path`);
  li.classList.add(`path_${id}`);
  if (isColumnMode) {
    li.innerHTML += `
    <span class="path_intro">
    <input placeholder="패스 이름 입력..." type="text" class="path_title" onchange="handleChangePathTitle(event,'${id}')">
    <button type="button" class="btn path-add-btn" onclick="handleAddPath('${id}')">패스+</button>
    <button type="button" class="btn" onclick="handleDeletePath('${id}')"><i class="fa-solid fa-trash"></i></button>
    </span>
    <div class="step_container ${isColumnMode ? "" : " container_row-mode"}">
            </div>
    <button type="button" class="btn step-add-btn" onclick="handleAddStep('${id}')" class="item_add-btn">
          스텝+
        </button>
    `;
  } else {
    li.innerHTML += `
    <span class="path_intro">
    <input placeholder="패스 이름 입력..." type="text" class="path_title" onchange="handleChangePathTitle(event,'${id}')">
    <button type="button" class="btn step-add-btn" onclick="handleAddPath('${id}')">패스+</button>
    <button type="button" class="btn" onclick="handleDeletePath('${id}')"><i class="fa-solid fa-trash"></i></button>
    </span>
    <div class="step_container ${
      isColumnMode ? "" : " container_row-mode"
    }"></div>
    <button type="button" class="btn path-add-btn" onclick="handleAddStep('${id}')" class="item_add-btn">스텝+</button>

    `;
  }

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
                <div class="step-content">
                  <p class="title"></p>
                  <p class="desc"></p>
                  <div class="step-btn-container">
                  <button
                    class="btn edit-btn"
                    type="button"
                    onclick="handleToggleModal('${id}')"
                  ><i class="fa-solid fa-pen-to-square"></i></button>
                  <button type="button" class="btn" onclick="moveItemUp('${id}')"><i class="fa-solid fa-angles-up"></i></button>
                  <button type="button" class="btn" onclick="moveItemDown('${id}')"><i class="fa-solid fa-angles-down"></i></button>
                  <button type="button" class="btn" onclick="handleDeleteItem('${id}')"><i class="fa-solid fa-trash"></i></button>
                  </div>
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
          `;
  stepContainer.appendChild(section);
}
