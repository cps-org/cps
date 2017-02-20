DOCUMENTS = \
  common-package-specification.html

%.html: %.rst
	rst2html "$<" "$@"

all: $(DOCUMENTS)
