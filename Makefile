.PHONY: open-slide open-chap18 open-chap34

OPEN ?= open

open-slide: open-chap18 open-chap34

open-chap18:
	$(OPEN) Chap18/Chap18_Slide.html

open-chap34:
	$(OPEN) Chap34/Chap34_Slide.html
