# 자동 세션 정리: 삭제 전에 확인하기

기준: 2026-11-04, Ouroboros source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 안내는 [cleanup CLI](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/cleanup.py)와 [worktree 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/worktree.py)을 기준으로 한다. 설치 버전의 `ouroboros cleanup --help`도 확인한다.

**판본과 확인 범위:** cleanup CLI와 worktree 구현 경로를 공개 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), `v0.59.9`, 위 722판 사이에서 정적으로 대조했을 때 이 선택 경로에는 소스 차이가 보이지 않았다. 선택 파일 비교일 뿐 주변 상태 저장·잠금·Git 버전과의 전체 동등성을 뜻하지 않는다. 내용 중 임시 cleanup 시험은 합성 상태의 과거 관찰이며 다른 설치판·운영 worktree·실제 사용자 데이터는 시험하지 않았다. 정리 명령의 현재 도움말과 실제 후보를 확인하고, 상세한 세션 복구는 [진행 상태](/docs/progress-detail/) 및 [복구](/docs/recovery-detail/)를 따른다.

!!! danger "기본 명령은 실제로 제거합니다"
    독립 CLI의 `ouroboros cleanup`은 기본이 미리보기가 아니다. 조건에 맞는 worktree·안전 삭제 가능한 브랜치·오래된 lock·세션 상태 파일을 실제로 제거한다. 삭제 전 진행 중 작업·다른 작업자·미전송 commit·무시된 파일과 백업을 확인한다. 이 문서나 명령 예시는 삭제 승인이 아니다. 자동 복구나 삭제 취소는 보장되지 않는다.

## 먼저 후보와 실제 작업 확인

1. 실행 중인 작업의 상태·소유자와 실제 작업 위치를 [진행 상태](/docs/progress-detail/), [복구](/docs/recovery-detail/)에서 확인한다. 접속이 끊긴 것만으로 작업이 끝났다고 판단하지 않는다.
2. 설정의 `orchestrator.worktree_root`(기본 `~/.ouroboros/worktrees`)와 `~/.ouroboros/data/auto_*.json`을 확인한다. 현재 프로젝트 한 곳만 대상으로 한다고 가정하지 않는다. 대상 경로의 권한과 기존 백업도 확인한다.
3. 독립 CLI에서 `ouroboros cleanup --dry-run`으로 후보를 보고 출력된 경로·branch·상태와 실제 Git 상태를 각각 대조한다. `--force`나 `--state-all`을 쓸 계획이면 그 옵션과 함께 dry-run하여 범위를 따로 본다. 이 판본의 dry-run은 제거하지 않지만 다른 초기화·로그 부작용과 다른 버전의 동작까지 보장하지 않는다.
4. worktree를 제거해도 필요한 결과가 안전한 위치에 있는지, branch나 commit의 병합·원격 보관 여부를 확인한다. `git status --porcelain`의 깨끗함은 **ignored 파일의 보존이나 원격 백업을 증명하지 않는다**. 캐시·환경 파일·사용자 데이터가 있을 수 있으므로 제거 대상 디렉터리를 직접 확인한다. 다른 프로세스가 동시에 작업을 시작할 수도 있다.
5. 실제 제거는 대상과 영향을 확인하고 명시적으로 결정한 경우에만 실행한다. 실행 후 출력과 Git worktree 목록, 남은 branch·상태 파일을 재확인한다. 후보가 비어 있다는 출력은 모든 작업이 안전하게 보관됐다는 뜻이 아니다.

## 각 옵션과 대상

| 명령 | 고정 구현의 범위 |
| --- | --- |
| `ouroboros cleanup --dry-run` | 제거 가능 후보를 `Would remove`로 표시하고 제거하지 않는다. |
| `ouroboros cleanup` | 관리 root에서 찾은 `auto_` worktree 중 lock이 활성으로 판단되지 않고 checkout이 깨끗하며 이름에서 유도한 `ooo/<auto_ID>` branch가 원본 저장소의 현재 HEAD에 병합됐다고 판정되면 제거한다. **그 예상 branch가 존재하지 않아도 구현은 병합된 것으로 취급하며, 발견 시 실제 checkout branch와 일치하는지 확인하지 않는다.** 따라서 실제 checkout의 HEAD·branch와 예상 branch 존재를 별도로 확인해야 한다. 존재하고 병합된 예상 branch는 안전한 `git branch -d`로 삭제한다. worktree가 없는 오래된 `auto_` lock과 `complete` 상태 파일도 조건에 따라 제거한다. |
| `ouroboros cleanup --force` 또는 `-f` | 위 대상에 깨끗하지만 미병합인 worktree를 추가한다. 미병합 branch는 강제 삭제하지 않지만 작업 디렉터리는 제거된다. dirty checkout을 강제로 지우는 옵션은 아니다. |
| `ouroboros cleanup --state-all` | worktree가 없는 `blocked`, `failed`의 `auto_*.json` 상태 파일도 제거 대상으로 넓힌다. 이 파일을 지우면 해당 세션의 진단·재개에 필요한 정보가 사라질 수 있다. |

옵션을 조합할 수 있지만, 미리보기의 후보는 그 순간 상태에 대한 관찰이다. 실제 명령은 worktree를 먼저 제거한 뒤 상태 파일을 검사하므로, dry-run에서 아직 존재한 worktree 때문에 표시되지 않은 상태 파일이 실제 실행 중 후보가 될 수 있다. 계획 결과가 정확한 최종 삭제 목록이라고 가정하지 않는다. 빈 임시 HOME의 합성 Git 저장소에서 깨끗한 관리 worktree와 같은 ID의 `complete` 상태 파일을 준비한 시험에서는 dry-run이 worktree만 표시하고 둘 다 보존했지만, 이어진 실제 cleanup은 임시 worktree와 상태 파일을 모두 제거했다. 이 관찰은 해당 조건에 한정되며 운영 데이터와 경합은 시험하지 않았다.

구현은 발견한 `auto_` worktree의 live lock과 dirty checkout을 건너뛰고, lock 파일은 worktree 디렉터리가 없고 stale로 판단된 경우에 제거한다. 읽을 수 없거나 손상된 lock도 stale로 판단될 수 있으므로 lock 이름만 보고 소유자가 없다고 확정하지 않는다. 상태 파일 정리는 이 worktree lock 검사와 별도다. 고정 구현은 상태 파일의 phase와 같은 세션 ID의 worktree 디렉터리 존재만 검사하며, 해당 상태 파일에 대해 live lock·세션 소유 프로세스나 백그라운드 job을 조회하지 않는다. 따라서 worktree가 없는 `complete` 또는 `--state-all`의 `blocked`·`failed` 파일이 여전히 필요한 진단 자료이거나 관련 프로세스가 남아 있을 수 있으므로, 상태 파일 후보와 관련 job·보존 요구를 삭제 전에 따로 대조한다. 이 설명은 소스 대조이며 실제 동시 정리를 시험한 것은 아니다. 빈 임시 HOME에서 살아 있는 합성 부모 PID와 호스트가 적힌 lock 및 같은 ID의 `complete` 상태 파일을 준비하고 worktree 없이 실제 `cleanup --dry-run`을 실행한 별도 시험에서 종료 0이었고, live lock은 후보가 아니지만 상태 파일은 후보로 표시됐다. 두 파일은 그대로 보존됐으며 실제 삭제·운영 중 동시성·OS 네트워크 격리는 시험하지 않았다. worktree 탐색은 지정 root의 디렉터리 구조와 Git 연결을 사용한다. 경로 이름만으로 다른 작업자의 파일이 안전하다고 추정하지 말고 반드시 후보를 확인한다. 병합 여부는 해당 원본 저장소의 현재 HEAD 기준이며 원격 push나 외부 백업 여부가 아니다.

상태 파일이 UTF-8로 해독되지 않는 경우도 유의한다. 고정 소스의 상태 판독은 파일 오류와 JSON 구문 오류는 건너뛰지만 UTF-8 해독 오류는 잡지 않는다. 빈 임시 환경의 실제 Typer cleanup 앱에 합성 `auto_*.json`의 잘못된 바이트를 주입한 `--dry-run`은 종료 1·`UnicodeDecodeError`였고 파일은 보존됐다. 실제 제거 명령은 상태 파일 검사 **전에** worktree·stale lock을 처리하므로 이 오류가 나도 앞선 처리가 없었다고 가정할 수 없다(이는 소스 순서의 해석이며 실제 삭제는 미시험). 실행 결과와 실제 경로를 확인하고 손상된 상태 파일은 원본 보존·백업 후 원인을 조사한다. 다른 버전이나 모든 손상 유형에 대한 결과는 아니다. 이는 공개 재현 자료가 제공되지 않는 합성 상태 파일의 로컬 관찰이다.

출력의 `Could not clean`은 일부 worktree 정리 실패를 나타낸다. 이 판본은 해당 `WorktreeError`를 경고로 모으고 그 자체로 실패 종료 코드를 올리지 않는다. 제거된 항목이 하나도 없으면 경고 뒤에 `Nothing to clean up.`도 표시할 수 있으므로 성공 문구나 종료 코드 0만으로 모든 후보가 안전하게 처리됐다고 판단하지 않는다. 다른 항목이 이미 제거됐을 수도 있으므로 실패만 보고 전체가 원상태라고 가정하지 않는다. 고정 소스와 대조하고 격리 HOME에서 Typer CliRunner의 합성 workspace에 `WorktreeError`를 주입한 대역 시험에서도 `--dry-run`은 경고와 `Nothing to clean up.`을 함께 출력하며 종료 0이었다. 실제 worktree 실패·삭제와 OS 네트워크 격리는 시험하지 않았다. 결과 메시지와 파일·Git 상태를 확인하고, 손상·미확인 파일을 reset·clean하거나 강제 삭제하지 않는다. [Git 작업공간과 복구](/docs/existing-project-detail/), [생명주기](/docs/lifecycle-detail/)를 함께 본다.

**검증 범위:** 고정 커밋과 cleanup·worktree 구현 및 해당 테스트에 차이가 없는 로컬 checkout에서, 임시 HOME·임시 Git 저장소를 사용하는 기존 `tests/unit/cli/test_cleanup.py` 11개가 통과했다. 실제 사용자 worktree·lock·상태 파일은 정리하지 않았다. OS 네트워크 격리, 병행 프로세스 경합과 운영 백업·복구 전체는 검증하지 않았다.


추가 독립 격리 시험에서는 임시 Git 저장소의 연결 worktree가 실제로는 `different` 브랜치의 미병합 커밋을 가리키고, 재구성된 `ooo/auto_example123` 브랜치는 없는 상태를 만들었다. `cleanup --dry-run`은 이 worktree를 `Would remove` 후보로 표시했고 종료 코드는 0이었다. 미리보기 뒤 worktree와 파일은 그대로 남았다. 처음에는 시험용 worktree root 주입을 빠뜨려 후보가 없다고 나왔으나, 이를 수정한 격리 실행에서 위 결과를 관찰했다. 이는 특정 조건의 미리보기 관찰이며 실제 삭제·모든 경합 상황의 검증이 아니다. 사용자 저장소는 건드리지 않았다.

별도 빈 임시 HOME·TMPDIR에 합성 상태 파일 `complete`, `failed`, `blocked`, `running` 네 개를 만들고 실제 CLI로 확인했다. `cleanup --dry-run`은 `complete`만, `cleanup --dry-run --state-all`은 `complete`·`failed`·`blocked`를 후보로 표시했다. 두 명령 모두 종료 0이었고 네 파일은 그대로 남았다. 이는 상태 파일에 대한 미리보기의 한 사례이며 실제 삭제, 동시 작업 경합과 OS 수준 네트워크 격리는 시험하지 않았다. 사용자 상태 파일과 모델은 사용하지 않았다.
