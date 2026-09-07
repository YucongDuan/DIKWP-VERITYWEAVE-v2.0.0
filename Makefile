PYTHON ?= python

.PHONY: test demo conformance audit model-check test-browser verify

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

demo:
	PYTHONPATH=src $(PYTHON) -m dikwp_verityweave demo --output .verityweave-demo --reset

conformance:
	PYTHONPATH=src $(PYTHON) -m dikwp_verityweave conformance

audit:
	$(PYTHON) scripts_static_audit.py

model-check:
	PYTHONPATH=src $(PYTHON) formal/bounded_model_check.py --output validation/BOUNDED_MODEL_CHECK_RECEIPT.json

test-browser:
	node tests/test_browser_invariants.js

verify: test audit model-check test-browser
