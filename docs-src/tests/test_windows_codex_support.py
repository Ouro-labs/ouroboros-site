from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/'content'
class WindowsCodexSupportTest(unittest.TestCase):
    def test_support_boundary_precedes_command_and_desktop(self):
        pages={'quickstart.md':('플랫폼 지원 경계','전체 실행 지원을 입증하지 않습니다','<p>Codex CLI를 이미 설치하고'), 'en/quickstart.md':('Platform support:','does not establish end-to-end native Windows Codex CLI support','<p>If Codex CLI is already installed'), 'zh/quickstart.md':('平台支持范围','并不能证明原生 Windows Codex CLI 的端到端执行受支持','<p>如果已经安装 Codex CLI')}
        for name,(warning,desktop,intro) in pages.items():
            with self.subTest(page=name):
                s=(ROOT/name).read_text(); command='&amp; $OuroborosPython -m ouroboros setup --runtime codex';i=s.index(warning);j=s.index(command);k=s.index(desktop);d=s.index('Codex Desktop',k+len(desktop));self.assertLess(i,s.index(intro));self.assertLess(i,s.index('ouroboros setup --runtime codex'));self.assertLess(i,j);self.assertLess(j,k);self.assertLess(k,d);self.assertIn('WSL2',s[i:j]);self.assertIn('docs/platform-support.md#L16-L27',s[i:j])
