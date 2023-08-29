const { fireEvent, screen } = require("@testing-library/dom");
const { createPathAndDisplay, paths, steps } = require("./writeUtils");

/*
  path의 구조는 다음과 같습니다.
  {
    id: uuid,
    order: 1,
    title: "패스 제목",
  }
*/

describe("path 추가와 삭제", () => {
  let mainContainer;
  beforeEach(() => {
    mainContainer = document.createElement("ul");
    mainContainer.innerHTML = `
    <ul class="main-container writePage__main col-mode">
    <button
      type="button"
      class="initial-path-add-btn add_new-btn writePage__btn"
    >
      패스 추가하기
    </button>
  </ul>
    `;
    document.body.appendChild(mainContainer);
  });

  afterEach(() => {
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });
  it("처음에 path 추가버튼 눌렀을시 path 객체가 잘 생성이 되는지", () => {
    const button = document.querySelector(".add_new-btn");
    button.onclick = () => {
      createPathAndDisplay();
    };

    fireEvent(button, new MouseEvent("click", { bubbles: true }));

    expect(paths[0]).toEqual({
      id: expect.any(String),
      order: 1,
      title: "",
    });

    // 추가 버튼이 화면에 없어야함
    expect(screen.queryByText("패스 추가하기")).toBeNull();

    //
  });

  it("기존 path가 있을때 거기에 path 추가버튼 누를시 path 추가가 잘 되는지", () => {
    const currentPath = document.querySelector(".path");
    const button = document.querySelector(".add_new-btn");
  });

  it("기존 path를 삭제할시 order 업데이트가 잘 되는지", () => {});
});

describe("반응형", () => {});

describe("모드 관련", () => {});

describe("스탭 관련", () => {});

describe("스텝 제목, 내용, 이미지 변경시 잘 되는지", () => {});
