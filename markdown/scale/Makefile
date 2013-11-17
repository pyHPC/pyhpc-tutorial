all: slides pages

slides: petsc4py-tutorial.md pyclaw-anatomy.md
	pandoc petsc4py-tutorial.md -t dzslides -s --mathjax  -o petsc4py-tutorial-slides.html
	pandoc pyclaw-anatomy.md -t slidy -s --mathjax  -o pyclaw-anatomy-slides.html

pages: petsc4py-tutorial.md pyclaw-anatomy.md
	pandoc -t html5 -s --mathjax petsc4py-tutorial.md -o petsc4py-tutorial.html
	pandoc -t html5 -s --mathjax pyclaw-anatomy.md -o pyclaw-anatomy.html

deploy: slides pages
	rsync -v -r ./  aron@ahmadia.net:domains/aron.ahmadia.net/web/public/pyhpc

clean: 
	rm *.html
