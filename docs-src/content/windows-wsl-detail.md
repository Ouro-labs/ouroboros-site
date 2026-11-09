# Windows와 WSL 2에서 시작하고 진단하기

!!! warning "판본과 검증 범위"
    별도 표시가 없으면 이 안내는 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2)를 기준으로 합니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 설치한 호스트와 MCP 서버는 각각 다른 판본일 수 있습니다. 기존 합성·대역 시험은 명시된 조건에 한정되며 실제 모델·외부 서비스·모든 호스트의 실행을 입증하지 않습니다. 현재 설치의 도움말과 [제품 문서](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/docs)를 대조하고 구판 동작이 같다고 가정하지 마세요.


기준: 2026-11-04, Ouroboros source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2)의 [플랫폼 지원](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/platform-support.md), [Windows WSL 문제 해결](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/windows-wsl-troubleshooting.md), [설치 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/getting-started.md). 운영체제 조건과 WSL 명령은 확인일의 [Microsoft 설치 안내](https://learn.microsoft.com/en-us/windows/wsl/install)와 [기본 명령](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)을 함께 대조했다. **이번 조사는 Linux 호스트에서 문서·소스를 읽은 것이며 Windows, WSL 설치·인증·모델 실행은 시험하지 않았다.** 설치 버전의 도움말과 환경이 다를 수 있다.

## 어떤 환경에서 실행하는가

| 경로 | 고정 원본의 지원 범위와 주의 |
| --- | --- |
| Windows의 **WSL 2** | 권장되는 Windows 경로다. Linux 배포판 안에서 Ouroboros와 필요한 실행 런타임을 설치한다. Windows의 호스트와 WSL 내부의 프로그램·환경·경로는 각각 확인한다. WSL이 설치됐다는 것만으로 런타임 인증·MCP 연결·모든 프로젝트의 성공이 증명되지는 않는다. |
| **Windows 네이티브** PowerShell | 실험적이다. 원본은 Claude Code 경로를 실험적으로 표시하고 Codex CLI는 WSL 2 경로를 안내한다. 경로·프로세스·신호 처리 차이가 있으며 TUI에는 ANSI 지원 터미널이 필요하다. Windows Terminal을 권장하고 `cmd.exe` TUI는 지원하지 않는다. [원본 제한](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/platform-support.md#windows-native-caveats) |

WSL 내부에서 실제 작업 디렉터리를 확인하고 [첫 설치와 실행](/docs/first-run-detail/), [런타임별 설치](/docs/runtime-support-detail/)를 따른다. Git과 Python, 호스트 플러그인, 실행 CLI 및 인증은 별개다. source 기준 독립 Python 패키지는 Python 3.12 이상이 필요하며, 패키지 extra별 호환성은 [원본 지원표](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/platform-support.md#python-profile-matrix)를 확인한다. Windows에 설치된 CLI가 WSL에서도 자동으로 올바르게 실행되거나 그 반대라고 가정하지 않는다.

## 변경 전에 현재 상태 확인

Windows **PowerShell**에서 다음을 실행하면 WSL 버전·기본 설정과 설치된 배포판의 상태 및 WSL 1/2 여부를 확인할 수 있다. 오래된 WSL에서는 `--version`이 없을 수 있다. 출력에는 배포판 이름 등 환경 정보가 포함된다.

```powershell
wsl --version
wsl --status
wsl --list --verbose
```

`winver`로 Windows 버전과 빌드를 확인한다. Microsoft의 단일 `wsl --install` 경로는 Windows 10 버전 2004·빌드 19041 이상 또는 Windows 11을 전제로 한다. WSL 2 자체의 오래된 빌드별 수동 요구사항은 아키텍처와 패치 수준이 다르므로 [Microsoft 수동 설치 조건](https://learn.microsoft.com/en-us/windows/wsl/install-manual)을 확인한다. 펌웨어 가상화, Windows 선택 기능, 관리 권한, 네트워크 또는 배포판 다운로드 경로와 조직 정책도 설치 가능성에 영향을 준다. Windows 11 Home도 필요한 기능과 가상화가 있다면 WSL 2 호스트가 될 수 있다.

이미 Linux 배포판이 시작된다면 그 **WSL 셸**에서 다음처럼 설치 여부를 확인한다. 버전 출력은 연결 성공이나 모델 사용 성공의 증거가 아니다.

```bash
pwd
python3 --version
git --version
ouroboros --version
```

독립 CLI가 없다는 메시지가 나오면 호스트 플러그인만 설치된 상태인지와 WSL 내부 설치 환경을 [첫 실행](/docs/first-run-detail/)에서 구분한다. 명령과 인증 값을 출력·복사하지 말고 오류를 필요한 범위에서만 공유한다.

## 설치·변환은 시스템 변경

Microsoft의 `wsl --install`은 관리자 PowerShell에서 WSL과 가상 머신 기능을 활성화하고 Linux 배포판을 설치하며 재시작이 필요할 수 있다. 네트워크 다운로드와 디스크 사용도 수반한다. 이미 WSL이 설치됐는데 도움말만 표시되면 `wsl --list --online`으로 배포판을 조회한 뒤, Microsoft 안내의 `wsl --install -d <배포판>` 경로를 확인한다. 온라인 목록 조회도 네트워크가 필요하다. 다운로드가 0%에서 멈출 때 Microsoft는 `--web-download` 경로를 안내하지만, 조직 정책을 우회할 권한이 있다고 가정하지 않는다. 관리 장치의 정책·설치 권한은 담당자와 확인한다. [Microsoft 설치 및 문제 해결](https://learn.microsoft.com/en-us/windows/wsl/install).

기존 배포판을 `wsl --set-version`으로 1↔2 변환하는 것은 설정 변경이며 시간이 걸리거나 실패할 수 있다. Microsoft는 큰 프로젝트가 있으면 변환 전에 백업을 권한다. 기본 버전을 설정하는 `wsl --set-default-version 2`는 **새 배포판의 기본값**이며 기존 배포판을 자동 변환하지 않는다. 배포판 등록 해제·삭제는 사용자 데이터를 제거할 수 있으므로 진단 수단으로 임의 실행하지 않는다. [Microsoft 기본 명령](https://learn.microsoft.com/en-us/windows/wsl/basic-commands).

네이티브 Windows의 원본 PowerShell 설치 스크립트는 필요한 Git·uv 설치와 PATH·호스트 설정 변경을 수행할 수 있다. 스크립트 내용을 읽고 대상·권한·호스트를 확인한 뒤 선택한다. 이미 설치된 호스트 설정을 유지해야 한다면 설치·재구성 옵션의 영향을 먼저 확인한다. 이 안내 작성 중 설치 명령은 실행하지 않았다.

## 증상별로 범위를 좁히기

| 관찰 | 다음 확인 |
| --- | --- |
| `wsl --install`이 도움말만 출력 | Microsoft가 설명하는 이미 WSL이 설치된 경우일 수 있다. 설치된 배포판을 `wsl --list --verbose`로 확인하고 온라인 목록은 필요할 때 조회한다. 이 출력만으로 원인을 단정하지 않는다. |
| WSL 실행·가상 머신 오류 | Windows 빌드, 펌웨어 가상화와 선택 기능, 관리 정책을 확인한다. 설정 변경이나 재부팅 전 기존 작업과 장치 정책을 확인하고 [Microsoft 문제 해결](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting)을 따른다. |
| 배포판은 열리지만 `ouroboros`가 없음 | 현재 셸이 WSL 내부인지, 독립 CLI를 설치한 Python 환경과 PATH가 맞는지 확인한다. 호스트 플러그인 설치와 독립 CLI 설치는 다르다. [설치 경로](/docs/first-run-detail/#install-check). |
| 명령은 있으나 런타임·MCP 실패 | `--version`은 해당 프로그램의 성공적 인증을 증명하지 않는다. [진단 안내](/docs/diagnostics-detail/)에서 진단 범위와 출력 공유 시 주의, [통합 안내](/docs/integration-detail/)에서 별도 서버·런타임 경계를 확인한다. 진단에 따라 네트워크·파일 쓰기나 모델 비용이 발생할 수 있다. |
| 네이티브 Windows에서 검증 재실행이 불확정 | 고정 원본은 AppContainer 제한에서 `.cmd`/`.bat` 명령을 거부하고, replay 복사 시 symlink 권한이 필요할 수 있다고 설명한다. 이는 성공 판정이 아니다. 해당 런타임·명령과 [검사 패키지](/docs/check-package-detail/)의 범위를 확인한다. |

문제를 기록할 때 Windows 빌드, WSL/배포판 버전, 실제 실행 셸, 재현 단계, 예상과 실제 결과를 구분한다. 오류와 로그에는 사용자 경로·명령 인자·비밀이 포함될 수 있으므로 공개·전달 전 검토한다. 설치/변환 문제, WSL 내부 패키지 문제, 호스트 MCP·모델 인증 문제를 같은 오류로 합치지 않는다.

**검증 범위:** 고정 Ouroboros 문서와 Microsoft 공식 문서를 정적으로 대조했다. Microsoft가 제시한 버전 조건은 확인일 기준이며, 실제 Windows·WSL 명령, 설치, OS 기능 활성화, 기존 배포판 변환, 네이티브 샌드박스 및 모델 호출은 수행하지 않았다.
