.PHONY: all clean

all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	python3 code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	python3 code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log

# Dependency Questions

# 1. If code/preprocess.py is edited:
# Make will rebuild figure_5_2.png and figure_5_3.png and then recompile paper.pdf.
# It will NOT rerun did_analysis.py because its dependencies did not change.

# 2. If code/did_analysis.py is edited:
# Make will rebuild did_table.tex and then recompile paper.pdf.
# It will NOT rerun preprocess.py.

# 3. If paper/paper.tex is edited:
# Make will only recompile paper.pdf.
# No Python scripts will run.
