A minimal Stock Exchange with Companies and Time Series of Trades.

See `commanline_example.sh` for usage.
Also see `market.py` and `tests.py`. To start, use `./run.sh`

## Usage:
```
./gbce init  # deletes and initialises the state of the market on disk
./gbce company ABC 12 50
./gbce company JUC 15 30
./gbce show
./gbce buy GIN £10.0 3    # to be added to command line interface
./gbce sell ALE £5.0 2    # to be added to command line interface
./gbce all-share-index    # to be added to command line interface
./gbce volume-weighted GIN 15  # to be added to command line interface
```

## Data Structures:
Currently three representations of TradeSeries are implemented.

* A Python list of Trade objects
* A numpy array of a struct. 
* A numpy record-array, i.e. a series of numpy arrays for each attributes
* A selection of a list of Trade objects, i.e. a generator on the list object.

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

## Major issue:
The float should not be used for currencies. There solution has two necessary parts:

* Storing fixed point (or integer * 100) instead of `float`s, or floats with assertions to check if they have exactly two decimals (next significant digit should be < 0.000001). Another solution is to use python packages available for money (as a data type): `python-money`, `decimal`, `QuantLib`, custom types, etc. Such solutions have the potential to cause performance issues.

* The rates should not be stored. Instead, the absolute money. For example in the Trade objects, instead of storing the (quantity, price), we should store (total,quantity). The price should be calculated using a function (e.g. a getter). This is especially important in the original representation (model) that the type of money variables should not be a float.
A similar solution is needed in other classes.

## Requirements:
* Linux
* Python 2
* numpy, pickle
