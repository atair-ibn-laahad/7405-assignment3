import inspect
from typing import Callable
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Request, HTTPException

from tasks.implied_volatility import implied_volatility  # task 1
from tasks.black_scholes_european import black_scholes_european_options  # task 2
from tasks.asian_option import geometric as closed_asian_geometric  # task 3
from tasks.basket_option import geometric as basket_geometric  # task 3 geometric
from tasks.asian_option import arithmetic as closed_asian_arithmetic  # task 4
from tasks.basket_option import arithmetic as basket_arithmetic  # task 5
from tasks.kiko_put_option import mc as kiko  # task 6
from tasks.binomial_tree import binomial_tree_american_option  # task 7

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

function_map = {
    # url : {display_name, function}
    "black_scholes": {"display_name": "Black-Scholes European Options", "function": black_scholes_european_options},
    "implied_volatility": {"display_name": "Implied Volatility", "function": implied_volatility},
    "closed_asian": {"display_name": "Closed-form formula for geometric Asian Options",
                     "function": closed_asian_geometric},
    "basket_geometric_asian": {"display_name": "Geometric Basket Asian Options", "function": basket_geometric},
    "closed_arithmetic_asian": {"display_name": "Closed-form formula for arithmetic Asian Options",
                                "function": closed_asian_arithmetic},
    "basket_arithmetic_asian": {"display_name": "Arithmetic Basket Asian Options", "function": basket_arithmetic},
    "kiko": {"display_name": "KIKO Put Option", "function": kiko},
    "binomial_tree": {"display_name": "Binomial Tree for American Options", "function": binomial_tree_american_option}

}


def dynamic_parameters(function_name: str, request: Request):
    """
    This function used for recognizing the function and its parameters, and then execute the function with the parameters

    :param function_name: should be given in function_map
    :param request: FastAPI Request object
    :return:
    """
    if function_name in function_map:
        target_function = function_map[function_name]["function"]
        signature = inspect.signature(target_function)
        parameters = {}

        for name, parameter in signature.parameters.items():
            param_value = request.query_params.get(name)
            if param_value is not None:
                # Convert param_value to the correct type, handle exceptions as needed
                try:
                    parameters[name] = parameter.annotation(param_value)
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Invalid value for parameter {name}")
        return lambda: target_function(**parameters)
    else:
        raise HTTPException(status_code=404, detail="Function not found")


@app.get("/calc/{function_name}")
async def dynamic_route(execute: Callable = Depends(dynamic_parameters)):
    """
    dynamic routing, when a new function is implemented, add it to the function_map and it will be available in the API

    :param execute:
    :return:
    """
    try:
        result = execute()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TypeError as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/", name="routes")
def return_all_routes():
    """
    Return all routes and their parameters to the UI

    :return:
    """
    # return the url and display name and param list to UI
    result = {}
    for url, data in function_map.items():
        result[url] = {"display_name": data["display_name"],
                       "params": [param for param in inspect.signature(data["function"]).parameters.keys()],
                       "info": data["function"].__doc__}
    return result


import uvicorn

if __name__ == "__main__":
    uvicorn.run("api_entries:app", host="127.0.0.1", port=7405, reload=True)
