run: install
	python3 main.py $(SYMBOL) $(num_years)

install:
	pip install jugaad-data datetime openpyxl pandas matplotlib numpy pyarrow h5py tables lxml tabulate sqlalchemy
	clear

clean:
	rm $(SYMBOL).csv $(SYMBOL).dta $(SYMBOL).feather $(SYMBOL).h5 $(SYMBOL).html $(SYMBOL).json $(SYMBOL).md 
	rm $(SYMBOL).parquet $(SYMBOL).pkl $(SYMBOL).sql $(SYMBOL).txt $(SYMBOL).xlsx $(SYMBOL).xml $(SYMBOL).png
	rm $(SYMBOL)_compress.png
	rm -r __pycache__ decompressed_folder compressed_folder