"""Check that PowerShell run examples end before normal prose."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.pre=0;self.buff=[];self.blocks=[];self.paragraphs=[];self.p=None
    def handle_starttag(self,tag,attrs):
        if tag=='pre':self.pre+=1;self.buff=[]
        if tag=='p' and not self.pre:self.p=[]
    def handle_endtag(self,tag):
        if tag=='pre':self.blocks.append(''.join(self.buff));self.pre-=1
        if tag=='p' and self.p is not None:self.paragraphs.append(''.join(self.p));self.p=None
    def handle_data(self,data):
        if self.pre:self.buff.append(data)
        elif self.p is not None:self.p.append(data)
class VenvDirectTest(unittest.TestCase):
    def test_three_languages_end_run_fence_and_resume_prose(self):
        for path,following in (('quickstart','실행은 코드와 파일을 변경'),('en/quickstart','Execution can change code and files'),('zh/quickstart','执行过程可能会更改代码和文件')):
            with self.subTest(path=path):
                p=Page();p.feed((ROOT/'site/docs'/path/'index.html').read_text())
                blocks=[x for x in p.blocks if '$OuroborosPython' in x and '-m ouroboros run' in x]
                self.assertEqual(len(blocks),1);self.assertNotIn(following,blocks[0]);self.assertTrue(any(following in x for x in p.paragraphs))
                self.assertTrue(any('$OuroborosPython' in x and '-m ouroboros --version' in x for x in p.blocks))
if __name__=='__main__':unittest.main()
