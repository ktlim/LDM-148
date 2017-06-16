export TEXMFHOME = lsst-texmf/texmf

LDM-148.pdf: *.tex local.bib
	latexmk -bibtex -pdf -f LDM-148.tex
