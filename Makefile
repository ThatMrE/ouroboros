# Repair Continuum — N-of-1 analysis pipeline entry point
#
#   make setup       install Python deps
#   make allocation  generate the sealed allocation keyfile (PAIRS=, SEED=)
#   make dry-run     run the pipeline on SIMULATED data + calibration checks
#   make all         setup + dry-run  (the pre-unblinding pipeline)
#   make analyze     run the REAL primary analysis (needs frozen, unblinded data)
#   make clean       remove caches and derived outputs
#
# Statistics/tooling only — no device control or administration logic.

PY      ?= python3
PIP     ?= pip3
ANALYSIS := analysis
DERIVED  := derived
KEYS     := keys
PAIRS    ?= 8
SEED     ?= 20260913
ALT      ?= greater

.DEFAULT_GOAL := help
.PHONY: help setup allocation dry-run all analyze clean

help:
	@echo "Repair Continuum N-of-1 — targets:"
	@echo "  make setup                 install deps ($(ANALYSIS)/requirements.txt)"
	@echo "  make allocation PAIRS=$(PAIRS) SEED=$(SEED)"
	@echo "                             generate sealed allocation -> $(KEYS)/allocation.csv"
	@echo "  make dry-run               simulated-data pipeline + calibration/power checks"
	@echo "  make all                   setup + dry-run (run BEFORE unblinding)"
	@echo "  make analyze ALT=$(ALT)      real primary analysis (needs $(DERIVED)/../data)"
	@echo "  make clean                 remove __pycache__ and $(DERIVED)/"

setup:
	$(PIP) install -r $(ANALYSIS)/requirements.txt

$(KEYS) $(DERIVED):
	mkdir -p $@

allocation: | $(KEYS)
	cd $(ANALYSIS) && $(PY) allocation.py --pairs $(PAIRS) --seed $(SEED) --out ../$(KEYS)/allocation.csv

dry-run: | $(DERIVED)
	cd $(ANALYSIS) && $(PY) dry_run.py | tee ../$(DERIVED)/dry_run_output.txt

all: setup dry-run
	@echo ""
	@echo "Pre-unblinding pipeline complete. Commit $(DERIVED)/dry_run_output.txt BEFORE unblinding."

analyze: | $(DERIVED)
	cd $(ANALYSIS) && $(PY) analyze.py --alt $(ALT)

clean:
	rm -rf $(ANALYSIS)/__pycache__ $(DERIVED)
