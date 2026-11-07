# 첫 작업의 결과를 확인하는 참고 예제

이 페이지는 첫 작업의 할 일 웹앱과 같은 목표를 이해하기 위해 **문서용으로 별도 작성한 합성 참고 예제**입니다. Ouroboros가 생성한 코드나 실행 결과가 아니며, 제품의 Interview·Seed·실행·평가가 성공했다는 증거가 아닙니다. 실제 작업에서 생성된 프로젝트의 README와 코드를 우선 확인하세요.

이 단일 HTML 예제는 Seed의 다섯 수용 기준 중 앞의 세 가지 앱 동작만 보여 줍니다. README에 설치·실행·접속·종료 방법을 기록하는 기준과 테스트 명령·범위를 기록하는 기준은 실제 생성된 프로젝트에서 각각 별도로 확인해야 합니다. 이 페이지 자체가 그 프로젝트 README를 대신하지 않습니다.

## 기대하는 동작

브라우저에서 제목을 입력해 추가하면 목록에 나타납니다. 빈 제목은 추가되지 않습니다. 완료를 체크한 뒤 같은 브라우저에서 새로고침해도 완료 상태가 남습니다. 계정, 서버 저장, 다른 기기와의 동기화는 포함하지 않습니다. 데이터는 이 예제를 연 브라우저의 해당 주소에 `localStorage`로 저장됩니다. 같은 주소에서 이전에 저장한 예제 데이터가 있다면 다시 표시되므로, 기존 데이터를 건드리고 싶지 않으면 별도의 브라우저 프로필을 사용하세요. 브라우저 저장이 차단되거나 지워지면 새로고침 후 데이터가 남지 않을 수 있습니다.

## 별도 폴더에서 실행하기

신뢰할 수 있는 별도 빈 폴더에서 아래 내용을 `index.html`로 저장하세요. 기존 프로젝트의 파일을 덮어쓰지 마세요. 이 예제에는 별도 패키지 설치가 필요 없고, 아래 서버 명령에는 Python 3가 필요합니다.

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>할 일 참고 예제</title>
</head>
<body>
  <main>
    <h1>할 일</h1>
    <form id="task-form">
      <label for="task-title">할 일 제목</label>
      <input id="task-title" autocomplete="off">
      <button type="submit">추가</button>
    </form>
    <p id="message" role="status"></p>
    <ul id="tasks"></ul>
  </main>
  <script>
    const key = 'ouroboros-docs-todo-reference-v1';
    const form = document.getElementById('task-form');
    const input = document.getElementById('task-title');
    const list = document.getElementById('tasks');
    const message = document.getElementById('message');
    let tasks = [];
    let storageAvailable = true;

    try {
      const saved = localStorage.getItem(key);
      if (saved !== null) {
        const parsed = JSON.parse(saved);
        if (!Array.isArray(parsed) || !parsed.every(item =>
          item && typeof item.title === 'string' && typeof item.completed === 'boolean')) {
          throw new Error('Invalid saved data');
        }
        tasks = parsed;
      }
    } catch (error) {
      storageAvailable = false;
      message.textContent = '저장된 데이터를 읽을 수 없습니다. 기존 데이터는 변경하지 않습니다.';
    }

    function save() {
      if (!storageAvailable) return;
      try {
        localStorage.setItem(key, JSON.stringify(tasks));
      } catch (error) {
        storageAvailable = false;
        message.textContent = '브라우저에 저장하지 못했습니다. 새로고침하면 변경이 사라질 수 있습니다.';
      }
    }

    function render() {
      list.replaceChildren();
      for (const task of tasks) {
        const item = document.createElement('li');
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = task.completed;
        checkbox.addEventListener('change', () => {
          task.completed = checkbox.checked;
          save();
        });
        label.append(checkbox, document.createTextNode(' ' + task.title));
        item.append(label);
        list.append(item);
      }
    }

    form.addEventListener('submit', event => {
      event.preventDefault();
      const title = input.value.trim();
      if (!title) {
        if (storageAvailable) message.textContent = '제목을 입력하세요.';
        return;
      }
      if (storageAvailable) message.textContent = '';
      tasks.push({title, completed: false});
      save();
      render();
      input.value = '';
    });
    render();
  </script>
</body>
</html>
```

저장한 폴더에서 다음을 실행하세요.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

서버가 시작되면 같은 기기의 브라우저에서 `http://127.0.0.1:8000/`을 엽니다. 8000번 포트가 이미 사용 중이면 서버는 시작되지 않습니다. 다른 사용 가능한 포트로 명령의 `8000`을 바꾸고 브라우저 주소에도 같은 포트를 사용하세요. 서버를 종료하려면 실행한 터미널에서 `Ctrl+C`를 누릅니다. 이 서버는 지정 폴더의 파일을 로컬에 제공하므로 별도 빈 폴더에서 실행하세요.

## 수용 기준을 직접 확인하기

1. 제목에 `문서 읽기`를 입력하고 **추가**를 누릅니다. 목록에 같은 제목이 보여야 합니다.
2. 빈 제목이나 공백만 입력하고 **추가**를 누릅니다. 항목 수가 늘지 않아야 합니다.
3. 추가한 항목의 체크 상자를 선택하고 페이지를 새로고침합니다. 같은 제목과 완료 표시가 남아 있어야 합니다. 브라우저 저장을 허용하지 않았다면 이 조건을 확인할 수 없습니다.
4. 서버를 종료하고, 이 페이지가 설명한 저장·실행·주소·종료 방법과 실제 환경의 결과를 비교합니다. 자동 테스트는 이 참고 예제에 제공하지 않습니다. 위 확인은 사람이 브라우저에서 하는 수동 검사입니다.

실제 Ouroboros 작업에서는 이 코드나 주소를 생성 결과라고 가정하지 마세요. 반환된 실제 작업 경로의 README에서 의존성 출처와 설치, 실행·종료, URL·포트, 테스트와 범위를 읽고, 그 프로젝트의 실제 파일과 결과로 Seed의 각 기준을 확인합니다. 결과가 없거나 실패했다면 성공으로 기록하지 말고 기존 실행 상태와 오류를 먼저 확인하세요.
