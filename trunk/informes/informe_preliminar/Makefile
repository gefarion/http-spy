#!/bin/bash
SOURCES=informe.tex
LOG_DIR=logs

all: informe

informe: $(SOURCES)
	pdflatex $^
	pdflatex $^	
	@if [ ! -d $(LOG_DIR) ]; then mkdir $(LOG_DIR); fi
	@if [ -f *.log ]; then mv *.log $(LOG_DIR); fi
	@if [ -f *aux ]; then mv *.aux $(LOG_DIR); fi
	@if [ -f *toc ]; then mv *.toc $(LOG_DIR); fi
	@if [ -f *out ]; then mv *.out $(LOG_DIR); fi
	@if [ -f *idx ]; then mv *.idx $(LOG_DIR); fi
	@if [ -f *ent ]; then mv *.ent $(LOG_DIR); fi
	clear; echo 'PDF COMPILADO!'
        
clean:
	rm -rfv $(LOG_DIR)
	rm -rfv informe.pdf
	
new: clean all
	
