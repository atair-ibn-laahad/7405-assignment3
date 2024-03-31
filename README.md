# 7405-assignment3
assignment3

## To implement new methods
implement your methods in the ./tasks package, and import it to the api_entries.py file.
Add a new entry in the `function_map` dict, that's it.
> You should **add PyDoc comments** to your def to provide extra information in the UI,
> and **TYPINGS for parameters is necessary** for the api to know how to communicate with the UI.
   
The UI set will automatically accept the newly implemented methods and display it in the list.

## Run the project
Create a new virtual environment, or use an existing one, install all necessary requirements.
And then you can choose:
1. Build / [download](https://github.com/Xrondev/HKU7405-optionPricer-UI) the GUI program, place the exe/AppImage/dmg file (others is not necessary) under `./GUI/` 
and then run the `main.py`
2. run the different method by importing them to `test.py`
3. run the `api_entries.py` to start a local/remote server, and use `requests` or a browser to invoke the methods. The
API doc is located on `http://127.0.0.1:7405/doc`. And you can find the url function map in `api_entries.py -> function_map`
4. run the `api_entries.py` to start a local/remote server, and build/download the Graphical User Interface program from
[Here](https://github.com/Xrondev/HKU7405-optionPricer-UI). The repo is configured to automatically compile the GUI program for Mac/Linux/Windows
you can find a package of unpacked file with exe/AppImage/dmg in the Actions page the latest successful build.

## Tasks

1. Implement Black-Scholes Formulas for European call/put options.
2. Implied volatility calculations.
3. Implement closed-form formulas for geometric Asian call/put options and geometric basket
call/put options.
4. Implement the Monte Carlo method with control variate technique for arithmetic Asian
call/put options.
5. Implement the Monte Carlo method with control variate technique for arithmetic mean
basket call/put options. For the arithmetic mean basket options, you only need to
consider a basket with two assets.
6. Implement the Quasi-Monte Carlo method for a KIKO-put option. Calculate the price
and the Delta of a given option.
7. The Binomial Tree method for American call/put options.
8. A graphical user interface for users to easily price various options with your pricer.