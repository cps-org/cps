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

SRCDIR ?= $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
OUTDIR ?= $(join $(SRCDIR),_site)

venv := $(notdir $(realpath $(shell $(POETRY) env info --path 2> $(--null))))

archive.flags += --create --gzip --verbose
archive.flags += --file=$(if $(ARCHIVE),$(ARCHIVE),cps-docs).tar.gz
archive.flags += --directory=$(OUTDIR)
ifneq ($(OS),Windows_NT)
archive.flags += --mode=a+rw
endif

setup.flags += --with=docs

build.flags += $(if $(BUILDER),-b $(BUILDER),-b html)
build.flags += $(if $(NOCOLOR),,--color)
build.flags += $(if $(SPHINXOPTS),$(SPHINXOPTS))

.PHONY: all setup html clean.venv clean.cache clean purge archive publish

all: html

setup:
	$(POETRY) check
	$(POETRY) install $(setup.flags)

html: setup
	$(POETRY) run sphinx-build $(build.flags) "$(SRCDIR)" "$(OUTDIR)"

clean.venv:
	$(if $(venv),$(POETRY) env remove "$(venv)",@echo "Nothing to do")

clean.cache:
	$(RM) "$(join $(OUTDIR),.doctrees)"

clean:
	$(RM) "$(OUTDIR)"

purge: clean.venv clean

archive: html
	tar $(archive.flags) .

publish: clean all
	./publish.sh
