const { fireEvent, screen, waitFor } = require("@testing-library/dom");
const userEvent = require("@testing-library/user-event");
const WriteUtils = require("./writeUtils");

const mainContainer_html = `
<div class="pathSelect">
<span>패스 선택</span>
<select id="pathSelect" class="writePage-input select"></select>
</div>
<button
type="button"
class="mode-btn writePage__btn"
>
세로모드로
</button>
<ul class="main-container writePage__main col-mode">
<button
  type="button"
  class="initial-path-add-btn add_new-btn writePage__btn"
>
  패스 추가하기
</button>
</ul>`;

const createFirstPath = () => {
  const button = document.querySelector(".add_new-btn");
  button.onclick = () => {
    WriteUtils.createPathAndDisplay();
  };
  fireEvent(button, new MouseEvent("click", { bubbles: true }));
};

describe("path 추가와 삭제", () => {
  let mainContainer;
  let paths;
  let steps;
  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = mainContainer_html;
    document.body.appendChild(mainContainer);
  });

  afterEach(() => {
    WriteUtils.resetPathsAndSteps();
    // const main_container_ul = document.querySelector(".main-container");
    // if (main_container_ul) {
    //   main_container_ul.innerHTML = "";
    // }
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });
  it("처음에 path 추가버튼 눌렀을시 path 객체가 잘 생성이 되는지", () => {
    createFirstPath();
    const path = document.querySelector(".path");

    // path의 className 중에 path_uuid 인 className이 있는지.
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

  it("생성한 path의 삭제버튼을 누를시  path 삭제가 잘 되는지", async () => {
    // const createPathandDisplay_spy = jest.spyOn(
    //   WriteUtils,
    //   "createPathAndDisplay"
    // );
    // const handleDeletePath_spy = jest.spyOn(WriteUtils, "handleDeletePath");
    createFirstPath();
    // expect(createPathandDisplay_spy).toBeCalledTimes(1);

    // handleDeletePath 실행.
    const deleteIcon = document.querySelector(".fa-trash");
    fireEvent(deleteIcon, new MouseEvent("click", { bubbles: true }));

    // expect(handleDeletePath_spy).toBeCalledTimes(1);
    // expect(handleDeletePath_spy).toBeCalledWith(paths[0].id);

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

  it("생성한 path의 패스+ 버튼을 누를시 path 추가가 잘 되는지", () => {
    // const createPathAndDisplay_spy = jest.spyOn(
    //   WriteUtils,
    //   "createPathAndDisplay"
    // );
    createFirstPath();

    // 새롭게 path 추가 버튼 누를때.
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    paths = WriteUtils.getPathsAndSteps().paths;

    // expect(createPathAndDisplay_spy).toBeCalledTimes(2);
    // 새로 생성된 path가 prevPathId로 잘 호출되었는지.
    // expect(createPathAndDisplay_spy).toBeCalledWith(paths[0].id);

    // FIXME 현재 createpathanddisplay는 paths를 잘 업데이트해서 불러오는데
    // 왜 delete같은경웨는 반영이 잘 안된거지?

    // 지금 화면에는 path가 두개가 추가가 되어있어야함.
    const newPath = document.querySelector(`.path_${paths[1].id}`);
    expect(newPath).toBeTruthy();

    expect(screen.queryAllByPlaceholderText("패스 제목 입력...").length).toBe(
      2
    );
    expect(screen.queryAllByText("패스+").length).toBe(2);
    const deleteIcons = document.querySelectorAll(".fa-trash");
    expect(deleteIcons.length).toBe(2);
    const stepContainer = document.querySelectorAll(".step_container");
    expect(stepContainer.length).toBe(2);

    //data상에 두개의 path가 추가되었나?
    expect(paths.length).toBe(2);
    expect(paths[1]).toEqual({
      id: expect.any(String),
      order: 2,
      title: "",
    });
  });

  it("생성한 path의 step 추가버튼을 누를시 step이 잘 추가가 되는지,", () => {
    createFirstPath();
    const stepAddButton = document.querySelector(".step-add-btn");
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));

    expect(screen.queryByPlaceholderText("스텝 제목 입력...")).toBeTruthy();
    expect(screen.queryByPlaceholderText("스텝 내용 입력...")).toBeTruthy();

    // 스탭 데이터가 잘 들어가 있나요?
    steps = WriteUtils.getPathsAndSteps().steps;
    expect(steps.length).toBe(1);
    expect(steps[0]).toEqual({
      id: expect.any(String),
      pathId: paths[0].id,
      order: 1,
      isNew: true,
      isEdited: false,
      title: "",
      desc: "",
    });

    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));

    expect(screen.queryAllByPlaceholderText("스텝 제목 입력...").length).toBe(
      2
    );
    expect(screen.queryAllByPlaceholderText("스텝 내용 입력...").length).toBe(
      2
    );

    expect(steps.length).toBe(2);
    expect(steps[1]).toEqual({
      id: expect.any(String),
      pathId: paths[0].id,
      order: 2,
      isNew: true,
      isEdited: false,
      title: "",
      desc: "",
    });
  });

  it("생성한 path의 이름을 변경할시 path 이름이 잘 변경되는지", () => {
    createFirstPath();
    const pathTitleInput = screen.queryByPlaceholderText("패스 제목 입력...");
    expect(pathTitleInput).toBeTruthy();

    fireEvent.change(pathTitleInput, { target: { value: "이걸로 가자" } });
    expect(pathTitleInput.value).toBe("이걸로 가자");

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths[0]).toEqual({
      id: expect.any(String),
      order: 1,
      title: "이걸로 가자",
      isEdited: true,
    });
  });

  it("path 생성 -> step 생성후 삭제시 안에 있던 step들이 잘 삭제가 되는지", () => {
    createFirstPath();

    const stepAddButton = document.querySelector(".step-add-btn");
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));

    steps = WriteUtils.getPathsAndSteps().steps;
    expect(steps.length).toBe(2);

    const pathDeleteBtn = document.querySelector(".fa-trash");
    fireEvent(pathDeleteBtn, new MouseEvent("click", { bubbles: true }));

    steps = WriteUtils.getPathsAndSteps().steps;
    expect(steps.length).toBe(0);
  });
});
// 현재 이 부분의 맹점은. path[0]이 정확히 dom상의 첫번째 path를 가리키는지를 모른다는것.
// 상관없을것같기도 하다.
// 그리고 이 부분에서 중복이 없는지. 체크하는것도 논리적인 실력이 될듯.
describe("path order 관련 테스트", () => {
  let mainContainer;
  let paths;
  let steps;

  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = mainContainer_html;
    document.body.appendChild(mainContainer);
  });

  afterEach(() => {
    WriteUtils.resetPathsAndSteps();
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });

  it("패스1, 2 추가, 패스2 삭제시 order는 1", () => {
    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(2);
    expect(paths[0].order).toBe(1);
    expect(paths[1].order).toBe(2);

    const pathDeleteBtn = document.querySelectorAll(".fa-trash");
    fireEvent(pathDeleteBtn[1], new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(1);
    expect(paths[0].order).toBe(1);
  });

  it("패스1, 2추가, 패스1 삭제시 order는 1", () => {
    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    const pathDeleteBtn = document.querySelectorAll(".fa-trash");
    fireEvent(pathDeleteBtn[1], new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(1);
    expect(paths[0].order).toBe(1);
  });

  it("패스1,2 추가, 패스1 옆에 패스3 추가시 order는 1,3,2", () => {
    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(3);
    expect(paths[0].order).toBe(1);
    expect(paths[1].order).toBe(3);
    expect(paths[2].order).toBe(2);
  });

  it("패스1,2,3 추가, 패스 1 삭제시 패스2, 3의 order는 1,2", () => {
    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 세번째 패스 추가
    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[1];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(3);

    const pathDeleteBtn = document.querySelectorAll(".fa-trash");
    fireEvent(pathDeleteBtn[0], new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(2);
    expect(paths[0].order).toBe(1);
    expect(paths[1].order).toBe(2);
  });

  it("패스1,2,3 추가, 패스 2 삭제시 패스1, 3의 order는 1,2", () => {
    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 세번째 패스 추가
    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[1];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    const pathDeleteBtn = document.querySelectorAll(".fa-trash");
    fireEvent(pathDeleteBtn[1], new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(2);
    expect(paths[0].order).toBe(1);
    expect(paths[1].order).toBe(2);
  });

  it("패스 1,2,3 추가, 패스 3삭제시 패스 1,2의 order는 1,2", () => {
    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 세번째 패스 추가
    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[1];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    const pathDeleteBtn = document.querySelectorAll(".fa-trash");
    fireEvent(pathDeleteBtn[2], new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(2);
    expect(paths[0].order).toBe(1);
    expect(paths[1].order).toBe(2);
  });

  it("패스 1,2,3 추가, 패스2 삭제후 패스1 옆에 패스4 추가시 order는 1,3,2", () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 세번째 패스 추가
    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[1];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    const pathDeleteBtn = document.querySelectorAll(".fa-trash");
    fireEvent(pathDeleteBtn[2], new MouseEvent("click", { bubbles: true }));

    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(3);
    expect(paths[0].order).toBe(1);
    expect(paths[1].order).toBe(3);
    expect(paths[2].order).toBe(2);
  });

  it("패스 1,2,3 추가, 패스2 삭제후 패스1 옆에 패스4,5 추가시 order는 1,4,3,2", () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 세번째 패스 추가
    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[1];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    const pathDeleteBtn = document.querySelectorAll(".fa-trash");
    fireEvent(pathDeleteBtn[2], new MouseEvent("click", { bubbles: true }));

    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    expect(paths.length).toBe(4);
    expect(paths[0].order).toBe(1);
    expect(paths[1].order).toBe(4);
    expect(paths[2].order).toBe(3);
    expect(paths[3].order).toBe(2);
  });
});
describe("step 데이터 변경 테스트", () => {
  let mainContainer;
  let paths;
  let steps;

  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = mainContainer_html;
    document.body.appendChild(mainContainer);
  });

  afterEach(() => {
    WriteUtils.resetPathsAndSteps();
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });

  it("스텝 제목 변경시 변경 잘 되는지", () => {
    createFirstPath();

    const stepAddButton = document.querySelector(".step-add-btn");
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    const stepTitleInput = screen.queryByPlaceholderText("스텝 제목 입력...");
    expect(stepTitleInput).toBeTruthy();

    fireEvent.change(stepTitleInput, {
      target: { value: "이걸로 변경해봅시다." },
    });

    steps = WriteUtils.getPathsAndSteps().steps;
    expect(steps[0]).toEqual({
      id: expect.any(String),
      pathId: paths[0].id,
      order: 1,
      isNew: true,
      isEdited: true,
      title: "이걸로 변경해봅시다.",
      desc: "",
    });
  });
  it("스텝 내용 변경시 변경 잘 되는지", () => {
    createFirstPath();

    const stepAddButton = document.querySelector(".step-add-btn");
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));

    const stepDescInput = screen.queryByPlaceholderText("스텝 내용 입력...");
    expect(stepDescInput).toBeTruthy();

    fireEvent.change(stepDescInput, {
      target: { value: "내용은 이거다!." },
    });

    steps = WriteUtils.getPathsAndSteps().steps;
    expect(steps[0]).toEqual({
      id: expect.any(String),
      pathId: paths[0].id,
      order: 1,
      isNew: true,
      isEdited: true,
      title: "",
      desc: "내용은 이거다!.",
    });
  });

  it("스텝 이미지 변경시 이미지 데이터가 변경 잘 되는지", async () => {
    createFirstPath();

    const stepAddButton = document.querySelector(".step-add-btn");
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));

    const file1 = new File(["hello"], "hello.png", { type: "image/png" });
    const file2 = new File(["fake file"], "hello2.png", { type: "image/png" });
    steps = WriteUtils.getPathsAndSteps().steps;
    stepImageInput = screen.queryByTestId(`imageInput_${steps[0].id}`);
    expect(stepImageInput).toBeTruthy();

    await waitFor(() => {
      userEvent.default.upload(stepImageInput, file1);
      expect(stepImageInput.files.length).toBe(1);
    });

    expect(stepImageInput.files[0]).toStrictEqual(file1);

    steps = WriteUtils.getPathsAndSteps().steps;

    await waitFor(() => {
      expect(steps[0]).toEqual({
        id: expect.any(String),
        pathId: paths[0].id,
        order: 1,
        isNew: true,
        isEdited: true,
        title: "",
        desc: "",
        image: expect.stringMatching(/^data:image\/png;base64/),
      });
    });

    let storedImage = steps[0].image;
    await waitFor(() => {
      userEvent.default.upload(stepImageInput, file2);
    });

    expect(stepImageInput.files[0]).toStrictEqual(file2);
    steps = WriteUtils.getPathsAndSteps().steps;
    // 이미지가 변경이 되었는지
    await waitFor(() => {
      expect(steps[0].image).not.toBe(storedImage);
    });
  });

  it("용량이 큰 이미지 업로드시 어떻게 되는지 테스트", () => {
    // 이부분 어떻게 테스트할지 생각해봐야함.
    expect(1).toBe(2);
  });

  it("제목, 내용, 이미지 변경 종합 테스트 ( 패스1,2 추가, 패스2에 스탭 1,2 추가) ", async () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    const stepAddButton = document.querySelectorAll(".step-add-btn")[1];
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    steps = WriteUtils.getPathsAndSteps().steps;
    const stepTitleInput =
      screen.queryAllByPlaceholderText("스텝 제목 입력...")[1];
    const stepDescInput =
      screen.queryAllByPlaceholderText("스텝 내용 입력...")[1];
    const stepImageInput = screen.queryByTestId(`imageInput_${steps[1].id}`);

    fireEvent.change(stepTitleInput, { target: { value: "제목제목" } });
    fireEvent.change(stepDescInput, { target: { value: "내용내용" } });
    await waitFor(() => {
      userEvent.default.upload(
        stepImageInput,
        new File(["hello"], "hello.png", { type: "image/png" })
      );
    });

    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    await waitFor(() => {
      expect(steps[1]).toEqual({
        id: expect.any(String),
        pathId: paths[1].id,
        order: 2,
        isNew: true,
        isEdited: true,
        title: "제목제목",
        desc: "내용내용",
        image: expect.stringMatching(/^data:image\/png;base64/),
      });
    });
  });
});
describe("step 추가, 삭제시 order가 제대로 반영이 되는지", () => {
  let mainContainer;
  let paths;
  let steps;
  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = mainContainer_html;
    document.body.appendChild(mainContainer);
  });
  afterEach(() => {
    WriteUtils.resetPathsAndSteps();
    // const main_container_ul = document.querySelector(".main-container");
    // if (main_container_ul) {
    //   main_container_ul.innerHTML = "";
    // }
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });
  it("path1 추가, step1,2,3 추가시 order는 1,2,3", () => {
    createFirstPath();
    const stepAddButton = document.querySelector(".step-add-btn");
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));

    steps = WriteUtils.getPathsAndSteps().steps;
    expect(steps.length).toBe(3);
    expect(steps[0].order).toBe(1);
    expect(steps[1].order).toBe(2);
    expect(steps[2].order).toBe(3);
  });

  it("path1 추가, 스텝 1,2,3 추가후 스텝 2 삭제하면 order는 1,2", async () => {
    createFirstPath();
    const stepAddButton = document.querySelector(".step-add-btn");
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));
    fireEvent(stepAddButton, new MouseEvent("click", { bubbles: true }));

    console.log(document.querySelectorAll(".fa-fa-trash"));
    const stepDeleteBtn = document.querySelectorAll(".fa-trash")[2];
    fireEvent(stepDeleteBtn, new MouseEvent("click", { bubbles: true }));

    steps = WriteUtils.getPathsAndSteps().steps;
    expect(steps.length).toBe(2);
    expect(steps[0].order).toBe(1);
    expect(steps[1].order).toBe(2);
  });
});
// css 상에서, pathSelect는 450px 이하에서만 나타나지만
// 현재 테스트에서는 그냥 pc에서도 화면상에 있다고 생각.
describe("패스 select 관련 테스트 (updateSelectoptions)", () => {
  let mainContainer;
  let paths;
  let steps;
  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = mainContainer_html;
    document.body.appendChild(mainContainer);
  });
  afterEach(() => {
    WriteUtils.resetPathsAndSteps();
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });
  it("패스를 추가할시 pathSelect가 잘 업데이트 되는지", async () => {
    createFirstPath();
    const path_select = document.querySelector("#pathSelect");
    expect(path_select).toBeTruthy();

    let options;
    options = document.querySelectorAll("option");
    expect(options.length).toBe(1);
    expect(options[0].value).toBe(paths[0].id);
    expect(options[0].text).toBe("이름없는 패스1");
  });

  it("생성된 패스의 이름을 변경할시 pathSelect가 잘 업데이트 되는지", async () => {
    createFirstPath();

    const path_select = document.querySelector("#pathSelect");
    expect(path_select).toBeTruthy();

    const pathTitleInput = screen.queryByPlaceholderText("패스 제목 입력...");
    fireEvent.change(pathTitleInput, { target: { value: "이걸로 가자" } });

    let options;
    options = document.querySelectorAll("option");
    expect(options.length).toBe(1);
    expect(options[0].textContent).toBe("이걸로 가자");
  });

  it("패스 삭제시 select가 잘 업데이트 되는지 (패스가 1개일때)", async () => {
    createFirstPath();
    const pathDeleteBtn = document.querySelector(".fa-trash");
    fireEvent(pathDeleteBtn, new MouseEvent("click", { bubbles: true }));

    const path_select = document.querySelector("#pathSelect");
    expect(path_select).toBeTruthy();

    await waitFor(() => {
      const options = document.querySelectorAll(`option`);
      expect(options.length).toBe(0);
    });
  });

  it("패스 삭제시 select가 잘 업데이트 되는지 (패스가 두개이상일때)", async () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    const path_select = document.querySelector("#pathSelect");
    expect(path_select).toBeTruthy();

    paths = WriteUtils.getPathsAndSteps().paths;
    let options;

    options = document.querySelectorAll(`option`);
    expect(options[0].value).toBe(paths[0].id);

    expect(options[0].text).toBe("이름없는 패스1");
    expect(options[1].value).toBe(paths[1].id);
    expect(options[1].text).toBe("이름없는 패스2");

    const pathDeleteBtn = document.querySelector(".fa-trash");
    fireEvent(pathDeleteBtn, new MouseEvent("click", { bubbles: true }));

    await waitFor(() => {
      options = document.querySelectorAll(`option`);
      expect(options.length).toBe(1);
    });
    expect(options[0].value).toBe(paths[1].id);
    expect(options[0].text).toBe("이름없는 패스1");
  });
});
describe("모바일 반응형 테스트 (changeDisplay)", () => {
  let mainContainer;
  let paths;
  let pathSelect;
  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = mainContainer_html;
    document.body.appendChild(mainContainer);
    pathSelect = document.querySelector("#pathSelect");
    if (!pathSelect.onchange) {
      const { onChangeSelectElement } = require("../responsivePath");
      pathSelect.onchange = onChangeSelectElement;
    }
    window.innerWidth = 450;
    window.innerHeight = 700;
  });
  afterEach(() => {
    WriteUtils.resetPathsAndSteps();
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });
  it("처음 패스 추가시 select에 그 함수로 선택되어있고 화면에는 첫번째 패스만 보여야함.", () => {
    createFirstPath();

    expect(pathSelect).toBeTruthy();
    const selected_option = pathSelect.options[pathSelect.selectedIndex];

    expect(selected_option.textContent).toBe("이름없는 패스1");

    const paths = document.querySelectorAll(".path");
    const path1_style = window.getComputedStyle(paths[0]);
    expect(path1_style.display).toBe("block");
  });

  it("마지막 패스 옆으로 패스를 계속 추가할시 화면에는 추가된 path만 보여야 함.", () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    expect(screen.queryByText("이름없는 패스2")).toBeTruthy();
    expect(screen.queryByText("이름없는 패스1")).toBeTruthy();

    let selected_option = pathSelect.options[pathSelect.selectedIndex];
    expect(selected_option.textContent).toBe("이름없는 패스2");

    let allPaths;
    allPaths = document.querySelectorAll(".path");
    const path1_style = window.getComputedStyle(allPaths[0]);
    expect(path1_style.display).toBe("none");
    let path2_style = window.getComputedStyle(allPaths[1]);
    expect(path2_style.display).toBe("block");

    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[1];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    selected_option = pathSelect.options[pathSelect.selectedIndex];
    expect(selected_option.textContent).toBe("이름없는 패스3");

    allPaths = document.querySelectorAll(".path");
    expect(allPaths.length).toBe(3);
    path2_style = window.getComputedStyle(allPaths[1]);
    let path3_style = window.getComputedStyle(allPaths[2]);
    expect(path2_style.display).toBe("none");
    expect(path3_style.display).toBe("block");
  });

  it("패스 추가 이후 기존 패스 사이에 패스 추가할시 그 패스만 보이도록 되었는지.", () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    let selected_option = pathSelect.options[pathSelect.selectedIndex];
    expect(selected_option.textContent).toBe("이름없는 패스2");

    let allPaths;
    allPaths = document.querySelectorAll(".path");
    const path1_style = window.getComputedStyle(allPaths[0]);
    expect(path1_style.display).toBe("none");
    let path2_style = window.getComputedStyle(allPaths[1]);
    expect(path2_style.display).toBe("block");
    let path3_style = window.getComputedStyle(allPaths[2]);
    expect(path3_style.display).toBe("none");
  });

  it("패스 삭제시 해당 path의 이전 path만 화면에 보이고 select는 그 값으로.", async () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    const pathDeleteBtn = document.querySelectorAll(".fa-trash")[1];
    fireEvent(pathDeleteBtn, new MouseEvent("click", { bubbles: true }));

    // 3초뒤에 삭제되고 display 변경되기 때문에 watiFor 사용해주어야 함.
    await waitFor(() => {
      let selected_option = pathSelect.options[pathSelect.selectedIndex];
      expect(selected_option.textContent).toBe("이름없는 패스1");
      expect(selected_option.value).toBe(paths[0].id);
    });

    let allPaths;
    allPaths = document.querySelectorAll(".path");
    expect(allPaths.length).toBe(1);
    const path1_style = window.getComputedStyle(allPaths[0]);
    expect(path1_style.display).toBe("block");
  });

  it("첫번째 패스 삭제시 두번째 패스가 화면에 보이고 select는 그 값만 선택되어야.", async () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    paths = WriteUtils.getPathsAndSteps().paths;
    let new_added_id = paths[1].id;

    const pathDeleteBtn = document.querySelectorAll(".fa-trash")[0];
    fireEvent(pathDeleteBtn, new MouseEvent("click", { bubbles: true }));

    await waitFor(() => {
      let selected_option = pathSelect.options[pathSelect.selectedIndex];
      expect(selected_option.textContent).toBe("이름없는 패스1");
      expect(selected_option.value).toBe(new_added_id);
    });

    let allPaths;
    allPaths = document.querySelectorAll(".path");
    expect(allPaths.length).toBe(1);
    const path1_style = window.getComputedStyle(allPaths[0]);
    expect(path1_style.display).toBe("block");
  });

  it("패스 select시 select한 path만 보이고 다른 path는 보이지 않는지", () => {
    createFirstPath();

    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[1];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    let allPaths;
    allPaths = document.querySelectorAll(".path");
    expect(allPaths.length).toBe(3);
    let path1_style = window.getComputedStyle(allPaths[0]);
    expect(path1_style.display).toBe("none");
    let path2_style = window.getComputedStyle(allPaths[1]);
    expect(path2_style.display).toBe("none");
    let path3_style = window.getComputedStyle(allPaths[2]);
    expect(path3_style.display).toBe("block");

    let selected_option = pathSelect.options[pathSelect.selectedIndex];
    expect(selected_option.textContent).toBe("이름없는 패스3");

    let option_elements = document.querySelectorAll("option");
    option_elements[1].selected = true;
    pathSelect.dispatchEvent(new Event("change"));

    path1_style = window.getComputedStyle(allPaths[0]);
    expect(path1_style.display).toBe("none");
    path2_style = window.getComputedStyle(allPaths[1]);
    expect(path2_style.display).toBe("block");
    path3_style = window.getComputedStyle(allPaths[2]);
    expect(path3_style.display).toBe("none");

    selected_option = pathSelect.options[pathSelect.selectedIndex];
    expect(selected_option.textContent).toBe("이름없는 패스2");

    option_elements[0].selected = true;
    pathSelect.dispatchEvent(new Event("change"));

    path1_style = window.getComputedStyle(allPaths[0]);
    expect(path1_style.display).toBe("block");
    path2_style = window.getComputedStyle(allPaths[1]);
    expect(path2_style.display).toBe("none");
    path3_style = window.getComputedStyle(allPaths[2]);
    expect(path3_style.display).toBe("none");

    selected_option = pathSelect.options[pathSelect.selectedIndex];
    expect(selected_option.textContent).toBe("이름없는 패스1");
  });
});

describe("가로, 세로모드 관련 테스트", () => {
  let mainContainer;
  let paths;
  let pathSelect;
  let modeBtn;

  beforeEach(() => {
    paths = WriteUtils.getPathsAndSteps().paths;
    steps = WriteUtils.getPathsAndSteps().steps;
    mainContainer = document.createElement("div");
    mainContainer.innerHTML = mainContainer_html;
    document.body.appendChild(mainContainer);
    pathSelect = document.querySelector("#pathSelect");
    modeBtn = document.querySelector(".mode-btn");
    if (!pathSelect.onchange) {
      const { onChangeSelectElement } = require("../responsivePath");
      pathSelect.onchange = onChangeSelectElement;
    }
    if (!modeBtn.onclick) {
      const { toggleMode } = require("./change_mode");
      modeBtn.onclick = toggleMode;
    }
    window.innerWidth = 450;
    window.innerHeight = 700;
  });
  afterEach(() => {
    WriteUtils.resetPathsAndSteps();
    if (mainContainer && mainContainer.parentNode) {
      mainContainer.parentNode.removeChild(mainContainer);
    }
  });
  it("처음에 패스추가할시 가로모드로 생성이 되는지", () => {
    let main_container = document.querySelector(".main-container");
    expect(main_container.classList.contains("col-mode")).toBeTruthy();
    const { checkmode } = require("./change_mode");

    expect(checkmode()).toBe("col");
    createFirstPath();

    const stepContainer = document.querySelector(".step_container");
    expect(stepContainer.classList.contains("container_row-mode")).toBeFalsy();
  });

  it("모드 변경시 기존 패스들의 모드 변경이 잘 되는지.", async () => {
    let main_container = document.querySelector(".main-container");
    expect(main_container.classList.contains("col-mode")).toBeTruthy();

    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 모드 변경
    fireEvent(modeBtn, new MouseEvent("click", { bubbles: true }));

    expect(main_container.classList.contains("col-mode")).toBeFalsy();
    const { checkmode } = require("./change_mode");
    expect(checkmode()).toBe("row");

    const stepContainer_list = document.querySelectorAll(".step_container");

    for (cont of stepContainer_list) {
      expect(cont.classList.contains("container_row-mode")).toBeTruthy();
    }
  });

  it("모드 변경후 새롭게 추가할시 추가된 패스들의 모드가 유지가 되는지", () => {
    const { checkmode } = require("./change_mode");

    let main_container = document.querySelector(".main-container");
    expect(main_container.classList.contains("col-mode")).toBeTruthy();

    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 모드 변경
    fireEvent(modeBtn, new MouseEvent("click", { bubbles: true }));
    expect(main_container.classList.contains("col-mode")).toBeFalsy();
    expect(checkmode()).toBe("row");

    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[2];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    const stepContainer_list = document.querySelectorAll(".step_container");
    for (cont of stepContainer_list) {
      expect(cont.classList.contains("container_row-mode")).toBeTruthy();
    }
  });

  it("가로모드로 추가하고, 모드변경해서 추가하고, 다시 가로모드변경시 추가, 변경 잘 되는지", () => {
    const { checkmode } = require("./change_mode");
    let main_container = document.querySelector(".main-container");
    expect(main_container.classList.contains("col-mode")).toBeTruthy();
    expect(checkmode()).toBe("col");

    createFirstPath();
    const path_add_btn = document.querySelector(".path-add-btn");
    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));

    // 세로모드로
    fireEvent(modeBtn, new MouseEvent("click", { bubbles: true }));
    expect(main_container.classList.contains("col-mode")).toBeFalsy();
    expect(checkmode()).toBe("row");

    fireEvent(path_add_btn, new MouseEvent("click", { bubbles: true }));
    const path_add_btn2 = document.querySelectorAll(".path-add-btn")[2];
    fireEvent(path_add_btn2, new MouseEvent("click", { bubbles: true }));

    let stepContainer_list = document.querySelectorAll(".step_container");
    for (cont of stepContainer_list) {
      expect(cont.classList.contains("container_row-mode")).toBeTruthy();
    }
    // 다시 가로모드로
    fireEvent(modeBtn, new MouseEvent("click", { bubbles: true }));
    expect(main_container.classList.contains("col-mode")).toBeTruthy();
    expect(checkmode()).toBe("col");

    stepContainer_list = document.querySelectorAll(".step_container");
    for (cont of stepContainer_list) {
      expect(cont.classList.contains("container_row-mode")).toBeFalsy();
    }
  });
});

describe("종합테스트", () => {});
