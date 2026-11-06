# Pending installation guidance review summary

This is a retrospective summary of static reviews conveyed in the work conversation, not an original signed review or approval. Its hash establishes only the identity of this text, not reviewer identity or independence, factual truth, complete privacy, translation, or real host or installation behavior. Gate and approval remain pending.

| Page | Current source SHA-256 | Current generated SHA-256 |
| --- | --- | --- |
| quickstart.md | fc09661f6bb6e3b391197a54d14c8e1d6b9cb07879f5b6238e6626f25fe20e46 | 565c289cbd9571edaace77de0fa88876aa18ff9df4923c9c5cd06882034be5f9 |
| en/quickstart.md | 7427e73e1a919a35c542cfc01b962f9781fd524c34ab494583917609f8d9b20d | bd6ad12f9fe4ce82d36585d42edf912dfc6b54dec471fef05a8159535e17c608 |
| zh/quickstart.md | 7969f86942f0c56dee2e4016937abd808eed825ded9178b481c39430e2e4d009 | df7cc00363b6654fcd3d65d057ad4244ccd619f02004dbdd05754cb9eeb7864d |
| first-run-detail.md | e19b0e23c3d273dece9d7e752d3b2acc261f8e038edf25155701923da5fe8a33 | 5bab8436bd983678a665ad28e605ceef93aeaff9a55ea0a634fcdfbcdc617d88 |

The cdff69ea intermediate snapshot was not approved: an independent P2 found overgeneralized no-argument setup instructions. After the three quickstarts were revised (8d2bd20b), an independent P1 found the first-run venv section still led users through the problematic setup. The final first-run correction produced 51ee6cf6; independent static source reviews of the four final pages and a separate integration re-review reported the P1 resolved. These are static reviews, not proof of a successful installation, host connection or first task.

Compared with c82fbdfb, each quickstart adds four fixed 592 source links: setup.py#L4806-L4861, claude_setup.py#L27-L64, adapter.py#L1201-L1215 and pyproject.toml#L74-L82. First-run adds the internal runtime-support-detail link; no links were removed. Existing 92-group and earlier delta evidence remains separately scoped. Full facts, personal information and every language/host remain unverified.
