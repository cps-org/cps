# Makefile for Sphinx documentation

# You can set these variables from the command line.
POETRY        = poetry
POETRYOPTS    =
SPHINXOPTS    = --color
SPHINXBUILD   = sphinx-build
BUILDDIR      = _site

.PHONY: clean all

all:
	$(POETRY) $(POETRYOPTS) run -- $(SPHINXBUILD) -b html $(SPHINXOPTS) . $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in '$(BUILDDIR)'."

clean:
	rm -rf $(BUILDDIR)/*

cache-clean:
	rm -rf $(BUILDDIR)/.doctrees

publish: clean all
	./publish.sh
