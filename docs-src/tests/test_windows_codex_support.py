from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/'content'
class WindowsCodexSupportTest(unittest.TestCase):
    def test_native_codex_cli_is_not_offered_as_a_powershell_path(self):
        pages={
            'quickstart.md': {
                'unsupported':'Codex CLI는 네이티브 Windows에서 지원하지 않습니다.',
                'scope':'macOS/Linux/WSL2 터미널',
                'desktop':'전체 실행 지원을 입증하지 않습니다',
                'claude':'&amp; $OuroborosPython -m ouroboros setup --runtime claude-cli',
            },
            'en/quickstart.md': {
                'unsupported':'Codex CLI is not supported on native Windows',
                'scope':'macOS/Linux/WSL2 terminal',
                'desktop':'does not establish end-to-end native Windows Codex CLI support',
                'claude':'&amp; $OuroborosPython -m ouroboros setup --runtime claude-cli',
            },
            'zh/quickstart.md': {
                'unsupported':'不支持在原生 Windows 上使用 Codex CLI',
                'scope':'macOS/Linux/WSL2 终端',
                'desktop':'并不能证明原生 Windows Codex CLI 的端到端执行受支持',
                'claude':'&amp; $OuroborosPython -m ouroboros setup --runtime claude-cli',
            },
        }
        for name, expected in pages.items():
            with self.subTest(page=name):
                text=(ROOT/name).read_text()
                unsupported=text.index(expected['unsupported'])
                scope=text.index(expected['scope'])
                cli_command=text.index('ouroboros setup --runtime codex')
                desktop=text.index(expected['desktop'])
                http=text.index('ouroboros setup --runtime codex --mcp-mode http')
                self.assertLess(unsupported,cli_command)
                self.assertLess(scope,cli_command)
                self.assertLess(cli_command,desktop)
                self.assertLess(desktop,http)
                self.assertIn('docs/platform-support.md#L16-L27',text[unsupported:cli_command])
                self.assertNotIn('&amp; $OuroborosPython -m ouroboros setup --runtime codex',text)
                self.assertIn(expected['claude'],text)
                self.assertIn('127.0.0.1:8765/mcp',text)
