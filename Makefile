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

ifeq (${POETRY},)
$(error Could not find the `poetry` command. \
	Please make sure you have installed poetry, and that it is on your system's PATH environment variable. \
	If you don't have poetry installed, please visit https://python-poetry.org for instructions on its installation.)
endif

venv ?= $(shell $(POETRY) env info --path 2> $(--null))

srcdir := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

build.flags += $(if $(BUILDER),-b $(BUILDER),-b html)
build.flags += $(if $(NOCOLOR),,--color)
build.flags += $(if $(SPHINXOPTS),$(SPHINXOPTS))

SRCDIR ?= $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
OUTDIR ?= $(join $(SRCDIR),_site)

.PHONY: all setup cache-clean clean

all: $(if $(venv),,setup)
	$(POETRY) run sphinx-build ${build.flags} "${SRCDIR}" "${OUTDIR}"

cache-clean:
	$(RM) "$(join $(OUTDIR),.doctrees)"

clean:
	$(RM) "$(OUTDIR)"

setup:
	$(POETRY) install

publish: clean all
	./publish.sh
