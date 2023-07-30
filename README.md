# CardExtractor
Repo to extract cards from pdf scan

## Setup
 - Install requirements.txt
 - Download poppler build for windows [here](https://github.com/oschwartz10612/poppler-windows/releases/)
 - Set env variable POPPLER_PATH to point to path\to\poppler-xx.xx.xx\Library\bin
 - Download source pdf and place it in img_src/AgricolaFrWm.pdf
 
 ## Run
 Run split_pdf_to_image to split up the pdf then process_cards to process all the cards one by one.