# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = site

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

.PHONY: clean all

all:
	$(SPHINXBUILD) -b html $(SPHINXOPTS) . $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in '$(BUILDDIR)'."

clean:
	rm -rf $(BUILDDIR)/*

cache-clean:
	rm -rf $(BUILDDIR)/.doctrees

publish: clean all
	./publish.sh
