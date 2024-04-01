# 1. Contribution to the Assignment 3
Huo Yunchuan is responsible for the Monte Carlo methods.  
Zhu Xinrong is responsible for the other functions and UI design.  
Shi Haoyu is responsible for report production and support.
# 2. Description of the user interface
The user interface of **Option Pricer** consists of a clean and straightforward layout divided primarily into three main sections:
## Navigation Pane
- On the left-hand side, there's a sidebar that functions as the main navigation panel. It has a "Search" bar at the top, followed by a list of option types and calculation methods. 
- Each option type is selectable, with the currently selected option highlighted.
## Main Content Area
- When an option type is selected, the corresponding parameters appear in the main content area. The Parameter List in the main content area includes inputs for the specific type of option selected.
- Each input field is clearly labeled for user convenience. With a tooltip showing the full description of the parameter when hovered over or selected.
- This area is divided into two columns: the Parameter List on the left and the Calculation Result on the right. 
- The right column is reserved for the calculation output, with a "Result" field displayed beneath the "Calculation Result" header.
## Action and Information Elements
- There is a "Calculate!" button at the bottom of the Parameter List column, which triggers the calculation process. 
- At the top of the main content area, there's a question mark icon, which, when clicked, displays an "Information" pop-up providing guidance on the use of the selected calculation. 
- Additionally, a modal window prompts users to visit the GitHub Repository to access the Python Source Code for Calculation Implementation or the Graphical User Interface Program.

***As a reminder `option_type` should be `call` or `put`; `mc_method` should be `None` or `geometric`.***
# 3. Description of the functionalities of each class/function
## Black-Scholes European Options
Calculates European call or put option prices. It uses the Black-Scholes formula, where `d1` and `d2` are calculated using inputs such as spot price, strike price, risk-free rate, and volatility. The function will return the price for a call or put option and raises a ValueError for invalid option types.
## Implied Volatility
Estimates implied volatility by iteratively adjusting an initial guess using the Newton-Raphson method. It compares estimated option prices to the market price and adjusts using the option's Vega until the estimate is within an acceptable error range or the maximum iterations are reached.
## Closed-form formula for geometric Asian Options
Computes the price of geometric Asian options with adjusted volatility and drift for the geometric average of underlying asset prices. It uses the Black-Scholes formula and norm.cdf to calculate the option price for both call and put options, returning a ValueError for unrecognized option types.
## Geometric Basket Asian Options
Calculates basket's volatility, drift, and initial value considering asset volatilities and correlation.
Uses Black-Scholes to compute `d1` and `d2`.
Determines call or put price based on option type, using present value calculations.
Returns basket option price. Errors for invalid option types.
## Closed-form formula for arithmetic Asian Options
Performs a Monte Carlo simulation to estimate arithmetic Asian option prices. It uses a control variate approach with geometric Asian option prices for variance reduction. The function generates simulated asset paths, calculates payoffs, and provides a confidence interval for the estimated option price, adjusted if a geometric control variate is used.
## Arithmetic Basket Asian Options
Uses geometric function for initial geometric basket option price.
Conducts `M` Monte Carlo simulations for asset price paths, with correlation.
Calculates arithmetic means and payoffs per simulation against strike price.
Adjusts arithmetic payoffs with geometric control variate if specified.
Provides and returns confidence interval for option price.
## KIKO Put Option
Initializes seed and generates stock price paths with Sobol sequences.
Calculates growth factors to simulate paths.
Checks paths for knock-out or knock-in events to determine payoffs:
Knock-out: Payoff is discounted cash rebate.
Knock-in: Payoff is max of strike minus final price, discounted.
Neither: Payoff is zero.
Calculates mean and standard deviation of payoffs for confidence interval.
Returns price interval
## Binomial Tree for American Options
Divides total maturity time `T` by the number of steps `N` to determine each time step's length `dt`. Calculates factors (u and d) for potential upward and downward price movements per step.Determines the probability `p` of price moving up, essential for risk-neutral valuation. Creates a 2D array of potential asset prices at every node of the binomial tree using u and d. Calculates option values at maturity for all scenarios, allowing for intrinsic value assessment.Applies dynamic programming to calculate option value at each node by comparing holding versus exercising, factoring in the option's early exercise feature. Outputs the price of the American option as determined at the binomial tree's root.
# 4. Test cases and analysis
r = 0.05, T = 3, and S(0) = 100. The number of paths in Monte Carlo simulation is m = 100,000.
## Asian options
  |$\sigma$|$K$|$N$|Type|Result(MC without control variate)|Result(MC with control variate)|
  |---     |---|---|----|--    |--|
  |0.3     |100|50 |put |[14.554747390365758, 14.841884374039484]|[9.432604581746558, 9.454486940656475]|
  |0.3     |100|100|put |[14.574777238353066, 14.861782558211791]|[9.378126406220924, 9.400097932372505]|
  |0.4     |100|50 |put |[17.96051499924547, 18.363815159631812]|[14.499656659579774, 14.541430568045122]|
  |        |   |   |    |   |   |
  |0.3     |100|50 |call|[14.554747390365758, 14.841884374039484]|[14.722150618028456, 14.744032976938373]|
  |0.3     |100|100|call|[14.574777238353066, 14.861782558211791]|[14.600332241240556, 14.622303767392138]|
  |0.4     |100|50 |call|[17.96051499924547, 18.363815159631812]|[18.194216761134655, 18.2359906696]|

## Basket options
  |$S_1(0)$|$S_2(0)$|$K$|$N$|$\sigma_1$|$\sigma_2$|$\rho$|Type|Result(MC without control variate)|Result(MC with control variate)|
  |---|---|---|---|---|---|---|---|---|---|
  |100|100|100|100|0.3|0.3|0.5|put|[11.65439049323195, 11.857634344394349]|[8.964615088480985, 9.011996516951074]|
  |100|100|100|100|0.3|0.3|0.9|put|[11.65439049323195, 11.857634344394349]|[8.664060027233566, 8.711441455703655]|
  |100|100|100|100|0.1|0.3|0.5|put|[9.618865881272, 9.778317311211602]|[3.490288607354998, 3.5130903557126514]|
  |100|100|80 |100|0.3|0.3|0.5|put|[24.632250113352285, 24.8823094687517]|[2.044169769836111, 2.0942364944408607]|
  |100|100|120|100|0.3|0.3|0.5|put|[4.474111790663183, 4.610756187034878]|[27.872503026795645, 27.913435115569403]|
  |100|100|100|100|0.5|0.5|0.5|put|[16.80698724088817, 17.178373556050786]|[24.51961215274615, 24.665693653118858]|
  |   |   |   |   |   |   |   |    | |
  |100|100|100|100|0.3|0.3|0.5|call|[11.65439049323195, 11.857634344394349]|[21.424508270409014, 21.471889698879103]|
  |100|100|100|100|0.3|0.3|0.9|call|[11.65439049323195, 11.857634344394349]|[24.231088316411935, 24.278469744882024]|
  |100|100|100|100|0.1|0.3|0.5|call|[9.618865881272, 9.778317311211602]|[16.93588306948237, 16.95868481784002]|
  |100|100|80 |100|0.3|0.3|0.5|call|[24.632250113352285, 24.8823094687517]|[32.668098644924406, 32.71816536952915]|
  |100|100|120|100|0.3|0.3|0.5|call|[4.474111790663183, 4.610756187034878]|[19.380863067213784, 19.421795155987542]|
  |100|100|100|100|0.5|0.5|0.5|call|[16.80698724088817, 17.178373556050786]|[31.33520793445863, 31.48128943483134]|

## American Options
  |$S(0)$|$\sigma$|$K$|$N$|Type|Result
  |---|---     |---|---|----|--    
  |100|0.3 |100|50 |put |15.366074651699167
  |100|0.3 |100|100|put |15.387916838083495
  |100|0.3 |80|50|put |7.004608455954272
  |100|0.3 |120|50|put |27.376627732243026
  |100|0.5 |100|50 |put |18.662962142011235
  |100|0.1 |100|50 |put |11.747250716979286
  |   |     |   |   |    |     
  |100|0.3 |100|100 |call|24.62949251091947
  |100|0.3 |100|100|call|24.685533409682698
  |100|0.3 |80|50|call|34.59688241390361
  |100|0.3 |120|50|call|17.57142082935458
  |100|0.5 |100|50 |call|83.95635470175478
  |100|0.1 |100|50 |call|3.349262873267106
## Analysis
- Volatility ($\sigma$):This represents the standard deviation of the returns of the underlying asset. Higher volatility increases the option price because there's a greater chance that the option will end up in the money due to larger potential price movements.
- Strike Price ($K$): Higher strike prices usually decrease the price of call options and increase the price of put options, assuming all other factors remain constant.
- Correlation ($\rho$): The correlation measures how the prices of the two stocks in the basket move relative to each other. A high positive correlation (close to 1) means the stocks tend to move in the same direction, which could lower the price of a put and raise the price of a call, because the basket behaves more like a single stock.
- Number of observations ($N$): This refers to the number of points at which the underlying asset's price is sampled to compute the average. More observations can lead to a smoothing effect, which can lower the impact of volatility and thus potentially reduce the option price.
- Option Type (call/put): A call option gives the right to buy, and a put option gives the right to sell. They react differently to market conditions. The prices for calls and puts are affected inversely by the same underlying conditions, typically.
# 5. Extensions
## To implement new methods
implement your methods in the ./tasks package, and import it to the api_entries.py file.
Add a new entry in the `function_map` dict, that's it.
> You should **add PyDoc comments** to your def to provide extra information in the UI,
> and **TYPINGS for parameters is necessary** for the api to know how to communicate with the UI.

The UI set will automatically accept the newly implemented methods and display it in the list.