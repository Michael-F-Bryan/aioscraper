PROJECT = aioscraper
DOCS = docs
BROWSER = xdg-open


bump-patch:
	bumpversion patch


docs:
	sphinx-apidoc $(PROJECT) -o $(DOCS)
	$(RM) $(DOCS)/modules.rst
	$(MAKE) -C $(DOCS) html
	$(BROWSER) $(DOCS)/_build/html/index.html


.PHONY: docs bump-patch
