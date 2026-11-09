---
description: "기존 Git 프로젝트에 Ouroboros를 적용할 때의 작업 경로와 변경 보호를 안내합니다. 상세 내용은 제품 소스 722 기준이며 설치 버전과 대조하세요."
---

# 기존 프로젝트에서 시작하기

!!! warning "판본과 검증 범위"
    이 안내의 상세 동작은 별도 표시가 없으면 2026-11-04 조사한 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 설치된 플러그인과 호스트 MCP 서버는 별도 판본입니다. 아래 합성·대역 시험은 표시된 조건에 한정되며 실제 모델·인증·모든 호스트의 동작을 증명하지 않습니다. 설치한 버전의 도움말과 [제품 시작 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)를 대조하세요. 구판 동작이 현재 설치에도 같다고 가정하지 않습니다.


## 현재 상황

이미 코드와 변경 이력이 있는 Git 저장소에 기능을 추가하거나 오류를 고치려는 단계입니다. 기존 파일, 브랜치, 검증 명령을 확인하고 현재 변경을 보존할 작업 branch 또는 별도 checkout을 준비하세요.

## 입력

대상 저장소의 절대경로, 변경 목표와 바꾸면 안 되는 동작, 실제 lint·build·test 명령을 준비합니다. 예를 들어 “이 저장소의 로그인 오류를 고치고 기존 테스트를 유지하며 회귀 테스트를 추가한다”는 목표에 저장소의 정확한 검증 명령을 붙입니다. CLI의 `/path/to/project`와 `/path/to/scan-root`는 실제 경로로 바꿉니다.

### 실행 전 저장소 기준을 기록하세요 {#worktree-preflight}

Git 저장소라면 `ooo run` 또는 독립 CLI 실행 전에 프로젝트 터미널에서 현재 branch, 기준 commit, 변경 상태를 읽기 전용으로 확인해 기록합니다.

```bash
git branch --show-current
git rev-parse --verify HEAD
git status --short
```

`rev-parse`가 실패하면 아직 `HEAD`가 없는 저장소일 수 있습니다. 초기 commit을 자동으로 만들지 말고 기존 파일과 실행 설정을 검토하세요. 제품 main `592c667f`와 release `0.59.9`의 공통 worktree 구현은 새 task branch를 만들 때 `HEAD`를 기준으로 삼습니다. 이 경우 원본 저장소의 미커밋 변경과 `detect`가 만든 미추적·무시된 `.ouroboros/mechanical.toml`은 새 worktree에 자동으로 포함되지 않을 수 있으므로, 실행 전에 실제 작업 경로와 검증 설정을 확인하세요([작업 worktree 입력 점검](#worktree-inputs)). 이미 해당 task branch가 있거나 내부 호출이 다른 기준점을 지정하면 결과가 다를 수 있습니다. 이 설명은 worktree를 사용하는 CLI 기본 orchestrator 경로와 MCP in-process 실행 경로에 한정됩니다. 이 경로들의 worktree 활성 여부는 공통 `orchestrator.use_worktrees` 설정(기본값 `true`)에 따릅니다. 표준 MCP 도구에는 `use_worktree` 토글이 공개 입력으로 제공되지 않습니다. 실행 후에는 응답의 실제 작업 위치를 확인하세요. 반환된 task branch/worktree와 그 기준 commit을 시작 전에 기록한 값과 대조하고, 아래 [별도 작업 결과 확인 절차](#review-worktree-result)를 따릅니다. 기존 변경을 전달하기 위해 임의로 stash·reset·commit하지 마세요. [main worktree 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/worktree.py#L339-L388) · [0.59.9 worktree 구현](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/core/worktree.py#L339-L388) · [main worktree 기본 설정](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/models.py#L775-L777) · [0.59.9 worktree 기본 설정](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/config/models.py#L765-L768) · [main CLI worktree 호출](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py#L858-L867) · [main MCP 입력 계약](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/execution_handlers.py#L1057-L1062) · [0.59.9 MCP 입력 계약](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/execution_handlers.py#L1057-L1062)

**실행 전 확인 순서:** 보존할 파일과 진행 중인 작업을 판단하고 → 위 명령으로 기준 HEAD와 변경 상태를 기록하고 → 실제 관리 root·저장소별 경로와 등록 상태를 확인하세요. 어느 단계든 확인할 수 없으면 실행을 보류하세요. 아래 경고의 조건과 남는 위험도 확인하세요.

!!! warning "작업 worktree 준비 경로의 기존 파일을 먼저 확인하세요"
    고정 구현의 `prepare_task_workspace`는 관리 경로 `<worktree_root>/<저장소 이름>/<durable_id>`를 준비할 때, 그 경로가 이미 존재하지만 대상 저장소의 `git worktree list --porcelain`에 등록되어 있지 않으면 복구 대상으로 간주해 해당 경로에 재귀 삭제를 시도합니다. 일반 파일·심볼릭 링크 등 모든 경로가 삭제에 성공한다는 뜻은 아니며, 이 준비 경로는 worktree 활성화 등 조건을 만족하는 실행에 한정됩니다. `worktree_root`의 기본값은 `~/.ouroboros/worktrees`입니다. 이 삭제는 작업 lock을 획득하기 전에 일어나며, 해당 디렉터리의 파일이 다른 작업자나 사용자에게 필요한지 확인하지 않습니다. 유효한 다른 저장소의 디렉터리라도 대상 저장소의 목록에 없다면 안전하다고 가정하지 마세요. 새 CLI 실행과 ID가 별도 제공되지 않은 일반 MCP 실행의 ID는 실행 중 생성되므로 정확한 새 경로를 미리 알 수 없습니다. 시작 전에 실제 관리 root와 저장소별 디렉터리, 대상 저장소의 `git worktree list --porcelain`으로 등록 상태를 확인하고 진행 중 작업 및 보존 자료를 살펴봅니다. 재개라면 실제 세션 ID와 저장된 workspace 경로가 있을 때 그 기록도 대조합니다. 확인할 수 없으면 실행을 보류하고 불확실한 경로를 임의로 삭제하거나 덮어쓰지 마세요. 확인 후에도 동시 변경에 따른 위험은 남습니다. 이 경계는 `cleanup` 명령의 `--dry-run`과 별개인 **작업 공간 준비** 경로입니다. [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/worktree.py). 별도 임시 Git 저장소의 합성 일반 디렉터리 한 사례에서 marker가 삭제되고 새 worktree가 등록됨을 확인했습니다. 운영 데이터·심볼릭 링크·동시 경합은 시험하지 않았습니다. [CLI main](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py#L843-L860) · [CLI release](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/run.py#L843-L860) · [MCP main](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/execution_handlers.py#L1250-L1278)

### 호스트 플러그인에서 시작

Codex 또는 Claude Code에서 대상 프로젝트 폴더를 열고 현재 변경을 보존할 branch 또는 별도 checkout을 준비합니다. 기존 작업과 실행 중인 작업을 덮어쓰지 않습니다. 호스트에 저장소의 문서와 실제 검증 명령을 먼저 읽도록 요청한 뒤 `ooo interview`로 변경 목표와 제약을 정합니다. 이어 `ooo seed`로 YAML을 생성·검토하고 `ooo run`으로 실행합니다. [진행 확인](/docs/progress-detail/#host-status)과 [호스트 복구](/docs/recovery-detail/#host-recovery)를 사용합니다.

### 독립 CLI에서 시작

아래 등록·탐지 명령은 [독립 CLI가 설치된 경우](/docs/first-run-detail/#install-check)에 사용합니다.

1. 대상 Git 저장소 경로를 확인하고 작업 branch를 만듭니다. 원본 작업을 보존해야 한다면 별도 checkout에서 진행합니다.
2. `ouroboros setup scan /path/to/scan-root`로 범위를 좁혀 저장소를 등록하고 `ouroboros setup list`로 확인합니다. 인수를 생략하면 홈 디렉터리를 검색하므로 의도한 경로를 명시하는 편이 분명합니다.
   `setup scan`은 선택한 root 아래 최대 두 단계만 탐색하고 숨김·일부 잡음 디렉터리를 건너뜁니다. 발견된 저장소 내부는 더 내려가지 않으며 다른 위치의 worktree를 자동으로 확장하지 않습니다. 예를 들어 저장소가 `~/work/repos/OWNER/REPO`라면 기본 홈 검색에서 깊이 제한으로 빠질 수 있으므로 `ouroboros setup scan ~/work/repos`처럼 적절한 root를 지정하고 `setup list`에서 실제 경로를 확인합니다. 검색 결과가 없다는 사실은 저장소 부재의 증거가 아닙니다. 이 명령은 이번에 발견한 결과를 레지스트리에 추가·갱신하며 기존 등록은 보존합니다. scan 출력은 이번 검색 결과이고 전체 등록 목록은 `setup list`로 확인합니다. [고정 소스의 검색 규칙](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/brownfield.py), [brownfield 흐름](/docs/workflows-detail/).

   `ouroboros setup default`는 등록된 저장소 목록을 표시하고 **한 번에 번호 하나**를 받아 해당 저장소의 기본 선택 상태를 반전합니다. 이미 기본이면 해제하고 아니면 추가하며 여러 기본 저장소를 둘 수 있습니다. 기본 입력 `skip`이나 잘못된 번호는 변경 없이 끝납니다. 등록 목록이 비어 있으면 먼저 적절한 범위를 scan하라는 안내가 나옵니다. 이 명령은 레지스트리를 변경하므로 선택 전에 `setup list`의 경로를 확인하세요. 기본 지정은 PM 인터뷰용 레지스트리 선택이며 이후 모든 실행의 작업 디렉터리를 확정한다는 뜻이 아닙니다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/setup.py).

3. 저장소에서 `ouroboros detect /path/to/project`를 실행합니다. 프로젝트에 따라 모델 호출이 발생할 수 있습니다. 생성된 `.ouroboros/mechanical.toml`의 lint·build·test·static 명령을 읽고, 프로젝트가 실제 제공하는 명령인지 확인합니다. 기존 파일은 `--force` 없이는 보존됩니다.
4. 변경 목표와 기존 제약을 인터뷰에 넣습니다. 예: `ouroboros init start "이 저장소의 로그인 오류를 고친다. 기존 테스트를 유지하고 새 회귀 테스트를 추가한다"`.
5. `init start`의 `Start workflow now?`는 기본 Yes입니다. Seed를 먼저 확인하려면 `n`을 선택하고, 생성된 Seed의 작업 경로와 완료 조건이 해당 저장소를 가리키는지 검토한 뒤 `ouroboros run /path/to/seed.yaml`을 실행합니다. 이미 Yes를 선택했다면 실행을 시도한 것이므로 시작 전 오류와 기존 작업의 상태를 먼저 확인하고 중복 실행하지 않습니다. [상태 확인](/docs/progress-detail/)과 [실패 복구](/docs/recovery-detail/)를 이어서 사용합니다.

### Seed 경로가 거부되거나 예상과 다를 때

고정 버전의 독립 CLI 경로 해석기는 명시적 `--project-dir`과 원본 metadata 경로를 먼저 처리하고 유효한 brownfield target을 안정 기준 선택에 반영한다. 이후 Seed 모델의 후보 경로를 평가하는 분기에서 후보가 모두 안정 기준 디렉터리 밖으로 벗어나 거부되면, 조용히 다른 위치에서 실행하지 않고 오류와 종료 코드 1을 반환한다. 이 조건을 모든 명시 경로와 모든 거부 상황에 일반화하지 않는다. 반면 MCP 실행·진화 핸들러의 **실행 후 검증 작업 디렉터리 해석 경로**는 해당 거부를 경고로 기록한 뒤 각각 dispatch 또는 stable base로 돌아갈 수 있다. 이것을 MCP의 모든 실행이 경로 오류를 무조건 중단한다거나, fallback 디렉터리가 원래 의도한 프로젝트라는 보장으로 해석하지 않는다. 명시된 작업 디렉터리나 위임된 부모 경로가 있는 경우에는 그 호출 경로의 우선순위가 따로 적용된다. 시작 전 대상 경로를 확인하고 반환된 실제 작업 위치와 검증 결과를 대조한다. 독립 CLI의 `--project-dir`은 명시적 대상 선택지지만 설정 전에 대상과 기존 변경을 확인한다. [CLI 경로 해석](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py), [MCP 실행 검증 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/execution_handlers.py), [진화 검증 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evolution_handlers.py).

고정 소스의 관련 호출자 대역 테스트 14개에서 거부·미지정·포함된 경로와 CLI의 명시 경로·상대 파일 참조·brownfield fallback을 확인했다. 이는 해석기 단위의 합성 시험이며 실제 모델 실행, 모든 MCP 호출 경로, OS 수준 격리나 운영 작업공간을 검증한 것은 아니다.

### 작업 worktree의 기존 변경과 검증 설정 확인 {#worktree-inputs}

!!! warning "검증 파일과 미커밋 변경은 작업 공간마다 확인하세요"
    새 task worktree는 원본 저장소의 `HEAD`를 기준으로 생성됩니다. 원본의 미커밋 코드와 `detect`로 새로 만든 미추적·무시된 `.ouroboros/mechanical.toml`은 자동으로 포함되지 않을 수 있습니다. 기존 task branch를 재사용하는 경우에는 그 branch의 내용이 기준입니다. 실행 결과의 `Task worktree`·`Task branch` 또는 호스트 응답의 `worktree_path`·`worktree_branch`를 확인하고, **실제 작업 경로**에서 필요한 변경과 검증 설정이 존재하는지 확인하세요. 별도 worktree가 없는 경우에는 응답과 실행 경로를 확인합니다. 상태를 맞추기 위해 기존 변경을 자동으로 stash·reset하거나 임의로 커밋하지 마세요. 원하는 변경과 설정을 어떻게 보존·전달할지는 저장소 상태와 허용된 작업 범위에 맞게 결정해야 합니다. [작업 공간 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/worktree.py), [평가 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py).

    빈 임시 Git 저장소에서 원본의 미커밋 파일과 미추적 `mechanical.toml`을 둔 뒤 새 task worktree를 준비한 격리 시험에서는 작업 공간에 커밋된 파일 내용만 있었고 해당 설정 파일은 없었습니다. 이 관찰은 해당 경로 한 사례이며 모든 호스트·설정에서 같은 결과를 보장하지 않습니다.

별도 임시 Git 저장소에서 실제 CLI를 별도 프로세스로 시작하고 런타임 생성·preflight만 대역한 합성 실패 사례에서는 관리 worktree가 Git 목록에 등록되고 검증 명령 표식과 실패 상태가 확인됐다. 별도 상태 CLI의 종료 0은 조회 성공이다. 실제 모델·작업 성공이나 병합·재시작은 검증하지 않았다.

별도의 합성 성공 명령 사례에서도 임시 관리 worktree 등록, CLI 종료 0 및 상태 `complete`를 확인했다. 출력에는 checkpoint를 찾지 못했다는 경고와 충분하지 않은 frugality 근거가 있었고, mock adapter는 의미 있는 작업 결과물을 만들지 않았다. 따라서 이는 실제 작업 완료·정식 평가·병합의 증거가 아니다.

!!! warning "검증 명령을 보지 않고 실행하지 마세요"
    `detect`는 제안된 명령의 형식과 프로젝트 안의 실행 진입점·선언 등을 검사해 파일로 남기지만, 그 검사를 해당 명령을 실행해 **통과했다는 증거**로 해석하지 마세요. 명령을 실제로 실행할 수 있는지, 테스트가 필요한 동작을 다루는지는 작업 경로에서 별도로 확인해야 합니다. 허용 목록이나 경로 검사는 프로젝트의 모든 의도와 테스트 범위를 보장하지 않습니다. `mechanical.toml`이 비거나 생성되지 않았다면 Stage 1 검증이 비어 있을 수 있습니다. [제안 검증 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/detector.py). 이 설명은 고정 소스의 제안 검증 경로를 대조한 것이며, 실제 모델 탐지나 사용자 프로젝트 테스트를 실행한 것은 아닙니다.

기존 저장소 등록·검증 탐지의 상세 동작은 [CLI 원본](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md)에 연결했습니다.

## 예상

호스트에서는 인터뷰 뒤 Seed에 변경 목표와 대상 저장소가 나타나야 합니다. 독립 CLI에서는 `setup list`로 등록된 저장소를 보고, `detect` 뒤 `.ouroboros/mechanical.toml`에서 제안된 검증 명령을 볼 수 있습니다. Seed 생성과 실행 결과는 별도로 확인해야 합니다.

## 확인

Seed의 작업 경로가 의도한 저장소인지, 완료 조건에 유지할 동작과 새 회귀 테스트가 있는지 읽으세요. `mechanical.toml`의 각 명령이 이 프로젝트에서 실제로 실행 가능한지 확인하고, 실행 뒤에는 변경 파일·테스트 결과·기존 변경 보존 여부를 대조하세요. 설정 파일이 비었거나 생성되지 않았다면 검증 범위가 빠졌는지 점검합니다.

## 별도 작업 결과를 원래 프로젝트에 반영하기 {#review-worktree-result}

작업이 성공했다고 표시되어도 변경이 원래 브랜치에 자동으로 들어갔다고 가정하지 마세요. 호스트·설정에 따라 별도 worktree가 없을 수 있습니다. 먼저 실제 응답의 `worktree_path`와 `worktree_branch`, 또는 독립 CLI의 `Task worktree`·`Task branch`가 있는지 확인합니다. 이 필드가 없다면 결과에서 실제 작업 위치를 확인하고 추측한 경로를 사용하지 마세요. 제품 main `592c667f`와 release `v0.59.9`의 worktree 경로는 [공간 준비 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/worktree.py), [CLI 반환 경로](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py)와 [release 공간 준비 구현](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/core/worktree.py)을 참고하세요. 실제 연결된 호스트와 설치 버전은 다를 수 있습니다.

1. **원래 작업을 먼저 보존합니다.** 원래 프로젝트에서 `git status --short`와 `git branch --show-current`를 확인하고, 사용자가 작업 중인 수정·새 파일을 기록합니다. 필요하면 소유자와 별도 보존 방법을 정합니다. 다른 사람의 변경을 임의로 커밋·덮어쓰기·삭제하거나 `reset --hard`, `clean`을 실행하지 마세요.
2. **반환된 작업 위치를 확인합니다.** 해당 경로에서 아래 읽기 전용 명령을 실행합니다. 이 경로가 의도한 저장소의 등록된 worktree인지 원래 프로젝트의 `git worktree list --porcelain`과 대조합니다. `HEAD`와 브랜치가 반환 정보와 다른 경우 또는 detached HEAD라면 그대로 기록하고 먼저 원인을 확인하세요.

    ```sh
    git status --short
    git branch --show-current
    git rev-parse HEAD
    git diff --stat
    git diff
    git diff --cached
    git ls-files --others --exclude-standard
    ```

    `git diff`는 추적 중인 미스테이징 변경, `git diff --cached`는 스테이징 변경을 보여 줍니다. 새 미추적 파일은 목록에만 나오므로 내용을 별도로 읽어야 합니다. Git이 무시하는 파일과 하위 저장소의 내부 변경은 이 목록만으로 완전히 확인할 수 없습니다. 비밀·개인정보는 공유하거나 커밋하기 전에 제외합니다.
3. **커밋된 변경도 확인합니다.** 실행 시작 시 기록한 기준 커밋과 위에서 확인한 작업 `HEAD`를 비교합니다. 아래 `<기준-커밋>` 자리표시자를 실제 확인한 기준 커밋 ID로 바꿉니다. `HEAD`는 현재 작업 위치의 확인된 커밋을 뜻합니다. 기준을 모르면 시작 기록·브랜치 이력을 먼저 살피고 임의로 확정하지 마세요.

    ```sh
    git log --oneline <기준-커밋>..HEAD
    git diff --stat <기준-커밋> HEAD
    git diff <기준-커밋> HEAD
    ```

    이 비교는 커밋된 차이만 보여 주므로 앞 단계의 미커밋·미추적 결과도 함께 검토합니다. 원래 브랜치가 진행된 경우 기준 이후 양쪽의 변경과 충돌 가능성을 확인하고, 파일·테스트 결과가 Seed의 각 기준에 맞는지 검토하세요. 상태 `complete`나 평가 결과만으로 실제 프로젝트에 안전하게 적용됐다고 판단하지 않습니다.
4. **사용자가 검토하고 통합 방법을 결정합니다.** 미커밋 결과가 있으면 소유자와 함께 무엇을 보존하고 커밋할지 먼저 결정합니다. 대상 브랜치·변경 범위·충돌·기존 사용자 변경을 확인한 뒤에만 적절한 PR 또는 통합 방법을 선택합니다. 승인 전에 merge하지 마세요. 이 문서는 자동 통합이나 충돌 없는 적용을 보장하지 않습니다.
5. **정리 전 결과를 보존합니다.** 필요한 파일·커밋·브랜치와 테스트 근거가 실제로 보존되고 원래 변경이 안전한지 확인하기 전에는 worktree나 브랜치를 삭제하지 마세요. 미추적·무시 파일과 별도 작업자의 결과도 확인합니다. 정리 동작의 조건은 [정리 안내](/docs/cleanup-detail/)를 참조하세요.

위 Git 조회 명령은 임시 합성 저장소에서만 검증한 읽기 예시이며 실제 호스트의 자동 커밋이나 모든 worktree 동작을 보장하지 않습니다.


### 하위 프로젝트의 실행 위치 구분 {#subproject-result}

Git 저장소 안의 하위 프로젝트를 작업 대상으로 선택했다면 **worktree 루트와 앱 실행·검증 디렉터리가 다를 수 있습니다**. 제품 main `592c667f`와 release `0.59.9`의 관리 worktree 준비는 원본 저장소 기준의 상대 하위 경로를 유지합니다. 예를 들어 실제 선택된 원본 프로젝트가 `/repo/apps/web`이고 반환된 `worktree_path`가 `/managed/task`라면 작업 디렉터리는 `/managed/task/apps/web`가 될 수 있습니다. 이 예시 경로를 그대로 사용하지 마세요.

두 판본의 CLI 실행 경로는 `workspace.effective_cwd`를 런타임·worker·실행 작업 디렉터리에 사용합니다. 조사한 MCP in-process 실행 분기도 이를 사용하지만 결과 메타데이터의 `worktree_path`는 worktree **루트**입니다. `effective_cwd`가 모든 응답에 별도 필드로 제공된다고 가정하지 마세요. 실제 선택된 원본 프로젝트, 저장소 루트, 실행 기록과 반환 worktree를 대조해 대응하는 하위 디렉터리를 확인합니다. 프로젝트가 다른 경로로 해석되었거나 기록이 불충분하면 README·테스트 경로를 임의로 정하지 말고 실제 실행 위치부터 확인합니다. 다른 호스트 위임·worktree 비사용 경로에 같은 변환을 무조건 적용하지 않습니다.

Git 변경 검토는 worktree 전체를 대상으로 하되, 앱의 README·패키지 설정·시작·종료·테스트 명령은 실제 실행한 하위 프로젝트를 기준으로 확인합니다. 루트의 다른 앱을 실행하거나 테스트한 결과를 해당 Seed의 검증으로 대신하지 마세요. 모노레포의 실행 규약이 대상 지정 또는 저장소 전체 검사를 루트에서 실행하도록 한다면 그 유효한 루트 명령을 사용할 수 있습니다. 명령의 작업 디렉터리와 실제 대상·검증 범위를 함께 확인합니다. 상대 검증 설정과 명령도 이 차이를 고려해 확인합니다. 원본 프로젝트에서 새로 생성한 미추적 설정이 worktree로 자동 전달된다는 뜻은 아닙니다.

근거: [main 경로 보존](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/worktree.py#L716-L760), [main CLI 실행 위치](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py#L889-L958), [release CLI 실행 위치](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/run.py#L889-L958), [main MCP 실행 위치](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/execution_handlers.py#L1583-L1590). 이는 고정 소스의 정적 대조이며 실제 하위 프로젝트의 모델 실행·앱 검증은 미시험입니다.

## 다음 행동

대상과 검증 명령이 맞으면 [진행상태 확인](/docs/progress-detail/)에서 같은 실행을 추적합니다. 테스트나 실행이 실패하면 [실패 복구](/docs/recovery-detail/)로 이동하세요. 작업 범위가 잘못됐다면 실행 전에 Seed와 검증 명령을 수정합니다.
