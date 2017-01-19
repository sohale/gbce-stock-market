A minimal Stock Exchange with Companies and Time Series of Trades.

See `market.py` and `tests.py`. To start, use `./run.sh`


## Currently three representations of TradeSeries are implemented.

* A Python list of Trade objects
* A numpy array of a struct. 
* A numpy record-array, i.e. a series of numpy arrays for each attributes
* A selection of a list of Trade objects, i.e. a generator on the list object. This is generated from 

All these formats are convertible to each other, and each is suitable for one form of computation. e.g. in-memory, batch processing, etc.

## Next step:
* A DataFrame representation
* A database link (e.g. sqlite3)

## Future directions:
 
Useful for purposes of Streaming, low-latency, distributed, pipe, etc

* Selectors in style of jQuery, MapReduce, RxJS, etc 
* Online streams
* Big data, etc
* Linux bash pipe (text representation), and CSV
