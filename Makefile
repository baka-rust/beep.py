project := beep
flake8 := flake8


.PHONY: bootstrap
bootstrap:
	pip install -r requirements.txt

.PHONY: clean
clean:
	@find $(project) "(" -name "*.pyc" -o -name "coverage.xml" -o -name "junit.xml" ")" -delete

.PHONY: lint
lint:
	$(flake8) $(project)
