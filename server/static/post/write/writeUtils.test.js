const { fireEvent, screen, waitFor } = require("@testing-library/dom");
const WriteUtils = require("./writeUtils");

const createFirstPath = () => {
  const button = document.querySelector(".add_new-btn");
  button.onclick = () => {
    WriteUtils.createPathAndDisplay();
  };

  fireEvent(button, new MouseEvent("click", { bubbles: true }));
};

// 가로모드와 세로모드인지.

describe("path 추가와 삭제", () => {
  let mainContainer;
  let paths;
  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = `
    <div class="pathSelect">
    <span>패스 선택</span>
    <select id="pathSelect" class="writePage-input select"></select>
    </div>
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
    WriteUtils.resetPathsAndSteps();
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });
  it("처음에 path 추가버튼 눌렀을시 path 객체가 잘 생성이 되는지", () => {
    createFirstPath();
    const path = document.querySelector(".path");

    expect(
      Array.from(path.classList).some((className) =>
        /^path_\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$/.test(className)
      )
    ).toBeTruthy();

    expect(screen.queryByPlaceholderText("패스 제목 입력...")).toBeTruthy();
    expect(screen.queryByText("패스+")).toBeTruthy();
    expect(screen.queryByText("패스 추가하기")).toBeFalsy();

    // 패스 데이터가 잘 추가되었는지.
    expect(paths[0]).toEqual({
      id: expect.any(String),
      order: 1,
      title: "",
    });
  });

  it("생성한 path의 삭제버튼을 누르면 path가 삭제되어야 함", async () => {
    const createPathandDisplay_spy = jest.spyOn(
      WriteUtils,
      "createPathAndDisplay"
    );
    const handleDeletePath_spy = jest.spyOn(WriteUtils, "handleDeletePath");
    createFirstPath();
    expect(createPathandDisplay_spy).toBeCalledTimes(1);

    // handleDeletePath 실행.
    const deleteIcon = document.querySelector(".fa-trash");
    fireEvent(deleteIcon, new MouseEvent("click", { bubbles: true }));

    expect(handleDeletePath_spy).toBeCalledTimes(1);
    expect(handleDeletePath_spy).toBeCalledWith(paths[0].id);

    await waitFor(() => {
      const path = document.querySelector(".path");
      expect(path).toBeFalsy();
    });

    expect(screen.queryByText("패스 +")).toBeFalsy();
    expect(screen.queryByText("패스 제목 입력")).toBeFalsy();

    // 첫번째 패스가 삭제되면 내 패스 만들기가 보여야 함.
    expect(screen.queryByText("내 패스 만들기")).toBeTruthy();

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(0);
  });

  it("생성한 path의 path 추가버튼 누를시 path 추가가 잘 되는지", () => {
    const createPathAndDisplay_spy = jest.spyOn(
      WriteUtils,
      "createPathAndDisplay"
    );
    // FIXME 이거 스파이가 안됨.
    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    paths = WriteUtils.getPathsAndSteps().paths;

    expect(createPathAndDisplay_spy).toBeCalledTimes(2);
    // prevPathId로 잘 호출되었는지.
    expect(createPathAndDisplay_spy).toBeCalledWith(paths[0].id);

    // FIXME 현재 createpathanddisplay는 paths를 잘 업데이트해서 불러오는데
    // 왜 delete같은경웨는 반영이 잘 안된거지?

    // 지금 화면에는 path가 두개가 추가가 되어있어야함.
    const newPath = document.querySelector(`.path_${paths[1].id}`);
    expect(newPath).toBeTruthy();

    //data상에 두개의 path가 보이나?
    expect(paths.length).toBe(2);
    expect(paths[1]).toEqual({
      id: expect.any(String),
      order: 2,
      title: "",
    });
  });

  it("기존 path를 삭제할시 order 업데이트가 잘 되는지", () => {});

  it("기존 path를 삭제할시 안에 있던 step들이 잘 삭제가 되는지", () => {});
});

describe("스탭 관련", () => {
  it("패스를 추가하고 거기에 스텝을 추가할시 추가가 잘 되는지", () => {});
});

describe("패스 select 관련", () => {});

describe("반응형", () => {});

describe("모드 관련", () => {});

describe("스텝 제목, 내용, 이미지 변경시 잘 되는지", () => {});
