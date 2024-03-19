GNUMAKEFLAGS := --no-builtins --no-builtin-variables
.SUFFIXES:

ifeq ($(OS),Windows_NT)
--which := where
--null := nul
RM := rmdir /s /q
else
--which := which
--null ?= /dev/null
RM := rm -rf
endif

POETRY ?= $(shell $(--which) poetry 2> $(--null))

ifeq ($(POETRY),)
$(error Could not find the `poetry` command. \
	Please make sure you have installed poetry, \
	and that it is on your system's PATH environment variable. \
	If you don't have poetry installed, \
	please visit https://python-poetry.org \
	for instructions on its installation)
endif

srcdir := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
venv := $(notdir $(realpath $(shell $(POETRY) env info --path 2> $(--null))))

build.flags += $(if $(BUILDER),-b $(BUILDER),-b html)
build.flags += $(if $(NOCOLOR),,--color)
build.flags += $(if $(SPHINXOPTS),$(SPHINXOPTS))

SRCDIR ?= $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
OUTDIR ?= $(join $(SRCDIR),_site)

.PHONY: all setup cache-clean clean clean.venv purge

all: setup
	$(POETRY) run sphinx-build ${build.flags} "${SRCDIR}" "${OUTDIR}"

clean.cache:
	$(RM) "$(join $(OUTDIR),.doctrees)"

clean.venv:
	$(POETRY) env remove "${venv}"

clean:
	$(RM) "$(OUTDIR)"

purge: clean.venv clean

setup:
	@$(POETRY) check
	@$(POETRY) install

publish: clean all
	./publish.sh
