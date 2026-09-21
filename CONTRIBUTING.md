# Contributing

Start with [Community and feedback](COMMUNITY.md) and the [roadmap](ROADMAP.md).
Documentation corrections, reproducible setup reports and fictional research
counterexamples are the current priorities. Discuss substantial code changes
and contribution terms with the maintainer before starting them. The existing
rights notice remains unchanged; no new license is introduced by this guide.

For a proposed change, explain the reader's problem, the resulting behavior,
how to verify it, and any remaining limitation. Use fictional examples and
keep generated personal state outside tracked files.

Before a commit or pull request, run the existing repository checks:

```sh
python3 scripts/privacy_check.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/easy_setup.py init --dry-run
git diff --check
```

Review the exact staged diff as well. Documentation changes should distinguish
available public behavior, private development and planned work. Do not turn
an implementation note, mockup or historical test into a claim of current
public availability.
