from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/'content'
class SeedFlowReadingTest(unittest.TestCase):
    def test_flow_and_exceptions(self):
        checks={
          'quickstart.md':['Interview 완료가 Seed 생성을 뜻하지는 않습니다','전체 YAML','실제 경로','테스트 명령과 범위를 설명하도록 요구하는지 확인하세요','`Start workflow now?`','`n`','YAML과 파일이 있으나','YAML만 있고','YAML이 없거나 생성이 실패·중단됨','MCP 서버를 사용할 수 없으면'],
          'en/quickstart.md':['An Interview ending does not mean a Seed was created','entire YAML','actual saved path','test commands and scope','`Start workflow now?`','`n`','YAML and file exist','YAML returned without a saved file or path','No YAML, or generation failed or was interrupted','If MCP is unavailable'],
          'zh/quickstart.md':['Interview 结束不等于 Seed 已创建','完整 YAML','实际保存路径','测试命令和范围','`Start workflow now?`','`n`','已有 YAML 和文件','已返回 YAML，但没有保存文件或路径','没有 YAML，或生成失败、中断','如果 MCP 不可用']}
        for name, phrases in checks.items():
            with self.subTest(page=name):
                text=(ROOT/name).read_text()
                for phrase in phrases:self.assertIn(phrase,text)
