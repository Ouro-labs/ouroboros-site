from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'content'
class SeedReviewIllustrationTest(unittest.TestCase):
 def test_partial_example_and_separate_paths(self):
  pages={'quickstart.md':['전체 Seed나 실제 출력·결과가 아닙니다','반환된 실제 Seed 파일 경로와 선택한 작업 폴더','전체를 다시 검토'], 'en/quickstart.md':['not a complete Seed or actual output or results','actual returned Seed file path and the selected working folder separately','review it all again'], 'zh/quickstart.md':['不是完整 Seed，也不是实际输出或结果','分别核对实际返回的 Seed 文件路径和所选工作文件夹','重新检查完整内容']}
  for name,phrases in pages.items():
   with self.subTest(page=name):
    s=(ROOT/name).read_text()
    for phrase in (*phrases,'`goal`','`constraints`','`acceptance_criteria`'):self.assertIn(phrase,s)
