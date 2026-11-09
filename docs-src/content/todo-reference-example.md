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
4. 실행한 터미널에서 `Ctrl+C`를 눌러 서버를 종료하고, 실제 환경에서 접속·종료가 설명대로 됐는지 확인합니다.

실제 Ouroboros 작업에서는 이 코드나 주소를 생성 결과라고 가정하지 마세요. 반환된 실제 작업 경로의 README에서 의존성 출처와 설치, 실행·종료, URL·포트, 테스트와 범위를 읽고, 그 프로젝트의 실제 파일과 결과로 Seed의 각 기준을 확인합니다. 결과가 없거나 실패했다면 성공으로 기록하지 말고 기존 실행 상태와 오류를 먼저 확인하세요.

## 세 앱 기준을 자동으로 검사하기

<details>
<summary>선택형 자동 브라우저 테스트와 검증 환경·한계 보기</summary>

<p>이 선택형 브라우저 테스트는 앞의 세 앱 AC(추가, 빈 제목 거부, 완료 상태를 새로고침 뒤 복원)를 대상으로 합니다. 실제 제품이 생성한 결과가 아니라 이 페이지의 합성 <code>index.html</code>을 확인합니다. README의 설치·실행·접속·종료 안내와 테스트 범위에 관한 나머지 두 AC는 검사하지 않습니다.</p>

<p>Linux 테스트용 프로젝트 루트에 앞 절의 <code>index.html</code>을 저장하고 아래 의존성을 설치하세요. Python 3, <code>uv</code>, 그리고 Linux의 <code>/usr/bin/chromium</code>이 필요합니다. 이 안내의 테스트는 Python 3.14.8과 시스템 Chromium 155.0.8059.84에서 확인했습니다. 의존성 버전은 pytest 9.2.0, pytest-playwright 0.10.0, Playwright 1.64.1입니다. Playwright 브라우저 자동 다운로드는 끄고 시스템 Chromium을 사용합니다.</p>

<pre><code class="language-sh">uv venv --no-config --python /usr/bin/python3 .venv
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 uv pip install --no-config --index-url https://pypi.org/simple --python .venv/bin/python &quot;pytest==9.2.0&quot; &quot;pytest-playwright==0.10.0&quot; &quot;playwright==1.64.1&quot;</code></pre>

<p>프로젝트 루트에서 아래 파일을 <code>tests/test_todo.py</code>로 저장하세요.</p>

<pre><code class="language-python">from pathlib import Path
from urllib.parse import urlsplit

import pytest
from playwright.sync_api import Page

ROOT = Path(__file__).resolve().parents[1]
TODO_URL = &quot;http://todo.test/&quot;

@pytest.fixture(scope=&quot;session&quot;)
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        &quot;executable_path&quot;: &quot;/usr/bin/chromium&quot;,
        &quot;headless&quot;: True,
        &quot;args&quot;: [&quot;--disable-background-networking&quot;, &quot;--disable-extensions&quot;],
    }

@pytest.fixture
def browser_context_args():
    return {&quot;service_workers&quot;: &quot;block&quot;}

@pytest.fixture(scope=&quot;session&quot;, autouse=True)
def delete_output_dir():
    # The plugin&#x27;s default fixture deletes ./test-results. This test writes no artifacts.
    yield


def test_todo_three_app_acceptance_criteria(page: Page):
    html = (ROOT / &quot;index.html&quot;).read_text(encoding=&quot;utf-8&quot;)

    fulfilled = []
    external_requests = []

    def fulfill_only_fixture(route):
        url = urlsplit(route.request.url)
        if url.scheme == &quot;http&quot; and url.netloc == &quot;todo.test&quot; and url.path == &quot;/&quot;:
            fulfilled.append(route.request.url)
            route.fulfill(status=200, content_type=&quot;text/html; charset=utf-8&quot;, body=html)
        else:
            if url.netloc != &quot;todo.test&quot;:
                external_requests.append(route.request.url)
            route.abort()

    page.context.route(&quot;**/*&quot;, fulfill_only_fixture)
    page.goto(TODO_URL, wait_until=&quot;domcontentloaded&quot;)

    title = page.locator(&quot;#task-title&quot;)
    add = page.get_by_role(&quot;button&quot;, name=&quot;추가&quot;)
    tasks = page.locator(&quot;#tasks li&quot;)

    title.fill(&quot;Buy oats&quot;)
    add.click()
    assert tasks.count() == 1
    assert &quot;Buy oats&quot; in tasks.first.inner_text()

    title.fill(&quot;   &quot;)
    add.click()
    assert tasks.count() == 1
    assert page.locator(&quot;#message&quot;).inner_text().strip()

    checkbox = tasks.first.locator(&quot;input[type=checkbox]&quot;)
    checkbox.check()
    page.reload(wait_until=&quot;domcontentloaded&quot;)
    assert tasks.count() == 1
    assert &quot;Buy oats&quot; in tasks.first.inner_text()
    assert tasks.first.locator(&quot;input[type=checkbox]&quot;).is_checked()
    assert len(fulfilled) &gt;= 2
    assert external_requests == []</code></pre>

<p>테스트는 pytest-playwright의 <code>page</code>/context fixture로 격리된 브라우저 context를 사용합니다. <code>route.fulfill</code>은 <code>http://todo.test/</code>에 합성 HTML을 제공합니다. 다른 host 요청은 abort하며 service worker를 막고 Chromium background networking을 끕니다. 이는 테스트 page의 요청 제한이며 OS 차원의 네트워크 격리는 아닙니다. plugin의 자동 <code>test-results</code> 삭제 fixture는 테스트 로컬에서 비활성화하고, 별도 산출물도 저장하지 않습니다. Playwright fixture teardown은 context와 browser를 닫지만, 프로세스가 비정상 종료되거나 도구가 자체 세션 밖으로 분리한 자손까지 정리한다고 보장하지는 않습니다.</p>

<p>정식 평가 Stage 1에서 이 명령을 읽으려면 프로젝트 루트의 <code>.ouroboros/mechanical.toml</code>에 항목을 둡니다. 이미 파일이 있으면 덮어쓰지 말고 필요한 값만 검토해 합치세요.</p>

<pre><code class="language-toml">test = &quot;python3 -m pytest -q tests/test_todo.py&quot;
timeout = 120</code></pre>

<p>직접 실행할 때는 프로젝트 루트에서 <code>.venv</code>를 활성화하고 다음을 실행하세요.</p>

<pre><code class="language-sh">. .venv/bin/activate
python3 -m pytest -q tests/test_todo.py</code></pre>

<p>정상 결과는 <code>1 passed</code>입니다. 이 문서의 표본에서 실제 제품 main <code>592c667</code> <code>MechanicalVerifier</code>는 Stage 1 <code>test</code>를 <code>executed=true</code>, <code>passed=true</code>, 종료 코드 0으로 기록했습니다. 같은 verifier에서 앱 <code>&lt;script&gt;</code>를 제거한 negative control과 <code>localStorage</code> 접근을 막은 control은 각각 종료 코드 1로 실패했습니다. 두 실패는 테스트가 기능 부재와 새로고침 후 데이터 손실을 잡았음을 확인한 격리 대조이며, 제품 생성물이나 전체 평가 결과가 아닙니다. <code>.ouroboros/mechanical.toml</code>의 검사가 실행되어도 그것만으로 최종 <code>approved</code>가 되지는 않습니다. 이 검증 환경은 Linux/Python 3.14.8/Chromium 155.0.8059.84입니다. 다른 OS, 브라우저, 설치 조합은 확인하지 않았습니다.</p>

<p>main <code>592c667</code>과 release <code>0.59.9</code>의 기계 명령 검증기는 프로젝트 <code>.venv</code>에서 <code>pytest</code> 모듈을 찾을 때 <code>python3 -m pytest</code> 경로를 허용합니다. <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/languages.py#L1018-L1062">main Stage 1 TOML 로더</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/detector.py#L1851-L1880">main Python module 검증 및 `.venv` 의존성 탐지</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/mechanical.py#L242-L326">main Stage 1 실행기</a>, release <code>0.59.9</code>의 <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/evaluation/languages.py#L1018-L1062">TOML 로더</a>, <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/evaluation/detector.py#L1851-L1880">Python module 검증 및 `.venv` 의존성 탐지</a>, <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/evaluation/mechanical.py#L242-L326">Stage 1 실행기</a>을 확인했습니다. 실제 공식 평가는 설정된 프로젝트 검사를 넘어서 recorded check와 전체 acceptance 조건을 함께 판정합니다. 자세한 경계는 <a href="/docs/seed-guide/#seed-execution-and-evaluation-evidence">Seed 평가 안내</a>를 보세요.</p>

</details>
