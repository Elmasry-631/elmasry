# -*- coding: utf-8 -*-
import ast
from pathlib import Path

from odoo.tests.common import TransactionCase


class TestHookSafety(TransactionCase):

    def test_manifest_does_not_register_destructive_pre_init_hook(self):
        manifest_path = Path(__file__).resolve().parents[1] / '__manifest__.py'
        manifest = ast.literal_eval(manifest_path.read_text(encoding='utf-8'))
        self.assertNotIn('pre_init_hook', manifest)
