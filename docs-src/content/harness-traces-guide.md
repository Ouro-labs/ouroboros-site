# Auto 인터뷰 trace를 찾고 비교하기

이 안내서는 `ooo auto`의 Auto session 한 건을 실제 ID로 찾아 로컬 trace를 확인하는 절차를 설명합니다. trace는 인터뷰·Seed 결정 과정을 살펴보는 투영 자료입니다. job 실행 상태, 실제 코드 변경, 작업 성공이나 요구 충족의 증거를 대신하지 않습니다.

기준은 Ouroboros 고정 소스 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 [`harness` CLI](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/harness.py), [trace exporter](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/auto/trace_export.py), [Auto pipeline](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/auto/pipeline.py)와 [CLI reference](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md)입니다. 아래 예시의 ID는 설명용 자리표시자입니다. 사용자 실행이나 설치 데이터는 조사하거나 읽지 않았습니다.

## 언제 trace가 생기는가

`ooo auto`가 terminal 상태에 도달하면 pipeline이 best-effort로 trace를 내보냅니다. 이 내보내기는 저장된 Auto 상태·Seed 결정 ledger와 EventStore 이벤트를 파일로 투영합니다. 모델을 다시 호출하거나 Auto 실행을 재개하지 않습니다. 다시 내보낼 때는 projection 파일을 덮어쓸 수 있고, 빈 stream은 같은 이름의 기존 JSONL 파일을 삭제할 수 있습니다. 제한 시간 뒤에도 background daemon thread가 trace 쓰기/삭제를 계속할 수 있습니다. 내보내기가 실패하거나 시간 제한을 넘기면 Auto 결과를 실패시키지는 않지만 trace가 없거나 불완전할 수 있습니다. 따라서 실행 응답이 있어도 trace가 반드시 존재하는 것은 아닙니다.

일반적인 trace 위치는 Auto 실행의 작업 디렉터리 아래 `.ouroboros/traces/<auto-session-id>/`입니다. 한 trace 디렉터리에는 `summary.md`, `outcome.json`과 데이터가 있는 경우 `questions.jsonl`, `ambiguity.jsonl`, `lateral.jsonl`, `decisions.jsonl`, `flags.jsonl`이 있습니다. 비어 있는 stream 파일은 생략될 수 있습니다.

## 올바른 ID와 로컬 저장소 찾기

Auto 시작 응답의 **`auto_session_id`**를 사용하세요. 소스에서 ID 형태는 `auto_` 뒤에 12자리 16진수이며, trace 디렉터리 이름도 이 ID입니다. 아래 ID는 서로 다른 레코드이므로 혼동하지 마세요.

| 시작/실행 레코드 | 의미 | trace 명령에 사용 |
| --- | --- | --- |
| `auto_session_id` (`auto_…`) | Auto 인터뷰·Seed·handoff 계보 | 예 |
| `job_id` | 백그라운드 job 상태/결과 | 아니요 |
| `execution_id` | 실행 이벤트·상태 레코드 | 아니요 |
| `session_id` | 실행 세션 | 아니요 |

시작 응답이 없으면 `ouroboros harness list`가 기본 Auto 상태 저장소와 trace 디렉터리에서 발견한 ID를 보여 줄 수 있습니다. 다만 목록은 현재 CLI가 바라보는 저장소만 읽습니다. 기본 경로는 다음과 같습니다.

- trace: 명령을 실행한 현재 디렉터리의 `.ouroboros/traces/`
- Auto 상태 JSON: `~/.ouroboros/data/`
- EventStore: 현재 설정에서 결정되는 DB 경로

Auto trace는 실행 당시 프로젝트 디렉터리를 기준으로 쓰일 수 있지만 CLI 기본 trace 경로는 **명령 실행 시 현재 디렉터리**를 기준으로 합니다. 다른 디렉터리에서 조회한다면 실행 당시 trace 위치를 `--traces-root`로 지정하세요. 필요한 경우 상태 저장소와 DB 경로도 따로 맞춥니다. `list`는 `--traces-root`, `--data-root`를 받으며 DB를 사용하지 않습니다. `show`, `trace`, `diff`는 세 경로 옵션을 모두 받습니다. `frontier`는 `--traces-root`만 받습니다.

## 기본 조회 순서

아래 `<AUTO_SESSION_ID>`를 시작 응답에서 받은 실제 `auto_session_id`로 바꾸세요. 꺾쇠 괄호를 입력값에 포함하지 않습니다.

```sh
# 저장된 상태와 이미 내보낸 trace를 함께 확인
ouroboros harness list

# 요약과 주요 outcome 필드 확인
ouroboros harness show <AUTO_SESSION_ID>

# 질문 stream에서 검색어가 있는 JSONL 행 찾기
ouroboros harness trace <AUTO_SESSION_ID> --grep "검색할 내용" --stream questions

# 두 실제 Auto trace 비교 (B - A delta)
ouroboros harness diff <AUTO_SESSION_ID_A> <AUTO_SESSION_ID_B>

# 이미 내보낸 trace 중 한 지표로 정렬
ouroboros harness frontier --metric final_ambiguity
```

`ouroboros harness`는 Auto trace를 보는 독립 CLI 명령 그룹입니다. Megacode의 외부 `harness` 실행 파일과 다르며, runtime harness 설정을 관리하지 않습니다. 설치판의 옵션은 먼저 `ouroboros harness --help` 및 각 하위 명령 `--help`로 확인하세요.

### 출력은 이렇게 읽습니다

- `list`는 `run_id`, 저장 시각, `exported`/`not exported`, phase, grade, ambiguity, provenance 요약을 표시합니다. `not exported`는 Auto 상태 파일은 있지만 trace가 아직 없다는 뜻입니다. `list`는 trace를 생성하지 않습니다.
- `show`는 `summary.md`와 `outcome.json`의 상태, phase, grade, Seed/QA 요약, 카운트, blocker, provenance 정보를 출력합니다. 이는 trace에 기록된 시점의 요약이지 현재 worker가 살아 있는지 또는 작업이 통과했는지 확인하는 조회가 아닙니다.
- `trace`는 다섯 JSONL stream 중 하나 또는 전체에서 `--grep` 패턴이 맞는 행을 파일명과 줄 번호와 함께 출력합니다. `--stream` 허용값은 `questions`, `ambiguity`, `lateral`, `decisions`, `flags`입니다. 정규식이 잘못된 경우 literal 부분 문자열 검색으로 처리됩니다. 검색 일치가 없어도 명령은 `No matches...`를 출력할 수 있습니다.
- `diff A B`는 grade, final ambiguity, 질문/결정 카운트, 상태 분류 카운트와 각 stream의 행 개수를 나란히 보여 줍니다. 수치 delta는 **B−A**입니다. 건수나 점수 변화만으로 원인이나 품질 개선을 입증할 수 없습니다.
- `frontier --metric`은 디스크에 이미 내보낸 trace만 한 지표로 순위화합니다. Auto 상태를 전부 trace로 변환하지 않습니다. 소스의 지표는 `final_ambiguity`, `rounds`, `decisions`, `promoted`, `rejected`, `gated`, `ambiguity_points`, `lateral`, `flags`, `unverified_provenance`입니다. 낮은 값 우선인 지표와 높은 값 우선인 지표가 섞여 있으며 결측은 끝으로 갑니다. `rounds`는 별도 대화 턴 수가 아니라 outcome의 question count를 사용합니다. 이는 정렬 기능이지 합격 판정이 아닙니다.

`No traces found.`가 나오면 현재 경로의 trace root와 Auto data root, 실제 ID, 실행 프로젝트를 먼저 대조하세요. `Run not found`는 해당 ID의 trace와 투영 가능한 Auto 상태가 발견되지 않았다는 뜻입니다. 잘못된 형식의 ID도 같은 오류일 수 있으니 ID 종류를 확인하고 파일을 임의 삭제하거나 생성하지 마세요. 알 수 없는 stream은 malformed input 오류이고, 알 수 없는 metric은 지원 목록을 함께 출력합니다. 유효한 지표에 대한 빈 frontier는 `No traced runs found.`가 될 수 있습니다. 빈 출력이나 종료 코드 0을 실행 성공 또는 레코드 부재의 증거로 간주하지 마세요.

## 조회와 export의 파일/DB 효과

이 CLI에는 별도 `export` 하위 명령이 없습니다. `list`는 이미 있는 trace와 Auto 상태를 읽어 목록만 만듭니다. `show`, `trace`, `diff`는 요청한 ID의 `outcome.json`이 없으면 저장된 Auto 상태와 선택적 EventStore에서 on-demand projection을 시도할 수 있습니다. 이 경우 로컬 `.ouroboros/traces/<ID>/` 아래에 디렉터리와 summary/JSONL/JSON 파일을 만들거나 기존 projection 파일을 다시 씁니다. 새 stream 데이터가 비어 있으면 같은 이름의 이전 JSONL projection을 삭제하기도 합니다. EventStore가 있으면 SQLite read-only로 엽니다. DB가 없더라도 Auto 상태만으로 projection이 가능한 경우가 있으며, 이 경로가 DB를 새로 만든다고 안내하지 않습니다. 삭제/덮어쓰기는 원본 Auto 상태나 EventStore가 아니라 trace projection 디렉터리 안의 파일에 적용됩니다.

조회 명령은 이미 `outcome.json`이 있으면 해당 trace를 내보낸 것으로 보고 자동 갱신하지 않습니다. 오래되거나 부분적인 trace가 최신 Auto 상태를 반영하지 않을 수 있습니다. 이 동작과 달리 terminal Auto finalize는 trace를 다시 내보내므로 기존 projection 파일을 덮어쓰거나 비어 있는 stream의 JSONL을 삭제할 수 있습니다. best-effort finalize가 시간 제한으로 기다림을 포기한 뒤에도 detached daemon thread가 파일 쓰기/삭제를 완료하거나 중단될 수 있습니다. 보존할 trace가 있으면 조회 중 projection을 일으킬 수 있는 `show`/`trace`/`diff`를 실행하거나 같은 Auto ID가 terminal finalize될 수 있기 전에 trace 디렉터리 바깥에 복사해 두세요. trace export는 저장된 상태/이벤트에 근거한 관찰용 projection이며, 원본 Auto 상태·job·EventStore를 갱신하거나 실행을 재개하지 않습니다.

`questions.jsonl`에는 질문과 답변, `decisions.jsonl`에는 결정과 provenance, `flags.jsonl`에는 오류·차단·fallback 등 상태 단서가 들어갈 수 있습니다. `outcome.json`에는 Seed 식별자/경로, QA, blocker, assumption, open gap 등도 포함될 수 있습니다. 텍스트 길이 제한은 비밀정보 삭제나 익명화가 아닙니다. 터미널 출력, trace 디렉터리, 백업 및 외부 공유를 제한하고 내용을 검토한 뒤 민감한 값은 직접 가리세요. 이 명령은 trace 조회/비교용이며 외부 서비스에 게시하거나 작업을 되돌리는 기능으로 설명되지 않습니다.

## 실제 작업 상태와 분리해 확인하기

trace에 `phase`, `grade`, `qa_verdict`, `blocker`가 있어도 원 실행의 현재 상태나 코드 변경이 보장되는 것은 아닙니다. Auto job의 진행/결과는 같은 실제 `job_id`로 job 상태·결과를 확인하고, 실행 상태는 해당 `session_id` 또는 `execution_id`로 조회하세요. 결과 파일과 작업 경로도 실제로 검토한 뒤, 필요한 경우 명시적인 평가 결과를 별도로 확인합니다. trace 통계, 수치 순위, trace 생성만으로 작업 성공이나 acceptance criteria 통과를 선언하지 마세요. [Auto 상태와 ID](/docs/status-guide/) 및 [Auto 사용 흐름](/docs/auto-detail/)도 참고하세요.

## 버전과 검증 범위

이전 소스 `722172ef`를 대상으로 한 실행·합성 시험은 재현 자료가 공개되지 않았으며, `592c667f` 또는 현재 설치판의 검증을 대신하지 않습니다. 이 안내서는 고정 main의 CLI/exporter/pipeline 정적 코드와 기존 문서를 대조해 작성했으며 실제 사용자 Auto 데이터, EventStore, 파일 권한, 모든 오류 조합, 호스트별 동작은 확인하지 않았습니다. 설치된 Ouroboros 버전의 `--help`와 구성된 실제 경로를 기준으로 사용하세요.
