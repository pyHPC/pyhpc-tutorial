all: slides pages

slides: petsc4py-tutorial.md
	pandoc petsc4py-tutorial.md -t dzslides -s --mathjax  -o petsc4py-tutorial-slides.html

pages: petsc4py-tutorial.md
	pandoc -t html5 -s --mathjax petsc4py-tutorial.md -o petsc4py-tutorial.html

deploy: slides pages
	rsync -v -r ./  aron@ahmadia.net:domains/aron.ahmadia.net/web/public/

clean: 
	rm *.html