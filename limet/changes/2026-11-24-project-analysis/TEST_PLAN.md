# TEST_PLAN — Analisi progetto / auto-onboarding

## Unit test

| Test | File | Copre |
| ---- | ---- | ----- |
| `test_analyze_requested_true` | `tests/test_config_loader.py` | R4: flag `analyze: true` → `True` |
| `test_analyze_requested_false_when_missing` | `tests/test_config_loader.py` | R4: flag assente → `False` |
| `test_intent_analyze` | `tests/test_hooks.py` | R5: prompt "analizza il progetto" → hint `/limet-analyze` |
| `test_intent_no_false_positive_analyze` | `tests/test_hooks.py` | R5: prompt neutro → nessun hint |
| `test_analyze_endpoint_sets_flag` | `tests/test_dashboard.py` | R3: POST `/api/analyze` setta flag |

## Test e2e (rif. E2E_VERIFICATION.md)

1. `limet:analyzer` su progetto fittizio → 7 doc non vuoti in `docs/`.
2. `/limet-analyze` → spawna analyzer e produce doc.
3. Dashboard → pagina "Analizza" → click → flag in `config.local.yaml`.
4. `python -m pytest tests -v` → verde.

## Comandi di riesecuzione

```bash
python -m pytest tests -v
claude plugin validate .
```
