export TEXMFHOME = lsst-texmf/texmf

LDM-148.pdf: *.tex
	latexmk -bibtex -pdf -f LDM-148.tex
