# Author: Hsiaoming Yang <lepture@me.com>
# Website: http://lepture.com

.PHONY: doc upload publish


doc:
	doki.py -t default --title=Felix\ Felicis --github=liquidluck README.rst > index.html

publish:
	git push origin gh-pages
