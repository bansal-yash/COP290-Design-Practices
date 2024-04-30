run: install
	g++ -fopenmp main.cpp -o main
	./main $(strategy) $(symbol) $(n) $(x) $(p) $(max_hold_days) $(c1) $(c2) $(oversold_threshold) $(overbought_threshold) $(adx_threshold) $(train_start_date) $(train_end_date) $(symbol1) $(symbol2) $(threshold) $(stop_loss_threshold) $(start_date) $(end_date)
	rm main

install:
	pip install jugaad-data pandas matplotlib
clean:
