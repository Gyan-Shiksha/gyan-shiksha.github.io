import base64
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('github_state', Path(__file__).with_name('github_state.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


class StateTests(unittest.TestCase):
    def call(self, command, path, api):
        with patch('sys.argv', ['github_state',command,'--state',str(path)]), patch.object(g,'api',api), patch.dict(os.environ, {'GITHUB_SHA':'observed-parent'}):
            g.main()

    def test_first_pull_has_no_state_and_performs_no_write(self):
        calls=[]
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'state.json'
            self.call('pull',path,lambda *args: calls.append(args))
            self.assertFalse(path.exists())
            self.assertTrue(json.loads(path.with_suffix('.meta.json').read_text())['new_branch'])
        self.assertEqual(len(calls),1)

    def test_existing_branch_missing_state_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'state.json'
            def api(endpoint,*args): return {'object':{}} if endpoint.startswith('/git/ref/') else None
            with self.assertRaises(RuntimeError): self.call('pull',path,api)
            self.assertFalse(path.exists())

    def test_read_existing_state_records_blob_sha(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'state.json'
            content=b'{"schema":1}'
            def api(endpoint,*args):
                return {'object':{}} if endpoint.startswith('/git/ref/') else {'encoding':'base64','content':base64.b64encode(content).decode(),'sha':'original-blob'}
            self.call('pull',path,api)
            self.assertEqual(path.read_bytes(),content)
            self.assertEqual(json.loads(path.with_suffix('.meta.json').read_text())['sha'],'original-blob')

    def test_update_has_optimistic_concurrency_guard(self):
        calls=[]
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'state.json'; path.write_text('{"schema":1}')
            path.with_suffix('.meta.json').write_text(json.dumps({'new_branch':False,'sha':'expected-blob'}))
            def api(endpoint,method,data): calls.append((endpoint,method,data)); return {'content':{'sha':'updated-blob'}}
            self.call('push',path,api)
            self.assertEqual(calls[0][2]['sha'],'expected-blob')
            self.assertEqual(json.loads(path.with_suffix('.meta.json').read_text())['sha'],'updated-blob')

    def test_bootstrap_creates_ref_only_after_complete_state_commit(self):
        calls=[]
        def api(endpoint,method='GET',data=None):
            calls.append((endpoint,method,data))
            if endpoint.startswith('/git/commits/') and method=='GET': return {'tree':{'sha':'base-tree'}}
            if endpoint=='/git/trees': return {'sha':'new-tree'}
            if endpoint=='/git/commits': return {'sha':'new-state-commit'}
            if endpoint=='/git/refs': return {'ref':'refs/heads/news-monitor-state'}
            return {'sha':'first-blob'}
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'state.json'; path.write_text('{"schema":1}')
            path.with_suffix('.meta.json').write_text(json.dumps({'new_branch':True,'sha':None}))
            self.call('push',path,api)
            self.assertEqual(calls[1][2]['tree'][0]['content'],'{"schema":1}')
            self.assertEqual(calls[3][0],'/git/refs')
            self.assertEqual(calls[3][2]['sha'],'new-state-commit')
            self.assertFalse(json.loads(path.with_suffix('.meta.json').read_text())['new_branch'])


if __name__=='__main__': unittest.main()
