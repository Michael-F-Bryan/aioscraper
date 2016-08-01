PROJECT = aioscraper
DOCS = docs
BROWSER = xdg-open
TEMP_CHANGELOG = temp_changes.md
CHANGELOG = CHANGES.rst


bump-patch:
	bumpversion patch

bump-minor:
	bumpversion minor

bump-major:
	bumpversion major

auto-changelog:
	auto-changelog --output=$(TEMP_CHANGELOG)
	pandoc --from=markdown --to=rst -o $(CHANGELOG) $(TEMP_CHANGELOG)
	$(RM) $(TEMP_CHANGELOG)

docs: auto-changelog
	sphinx-apidoc $(PROJECT) -o $(DOCS)
	$(RM) $(DOCS)/modules.rst
	$(MAKE) -C $(DOCS) html
	$(BROWSER) $(DOCS)/_build/html/index.html


.PHONY: docs bump-patch bump-minor bump-major auto-changelog
