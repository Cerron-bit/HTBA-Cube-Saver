# HTBA-Cube-Saver
An analysis-tool for your HTB Academy Learning Paths, providing the optimal way to go through the required modules in order to save money using the cube cashback system.

## Results
Cube Saver does provide a detailed overview about the cheapest strategy possible with your current cube balance and even anticipates how many cubes you exactly need to buy in order to complete your goals.
The strategy provided will include:
- Remaining cubes after following the strategy.
- Number of modules you can get with your current cube balance.
- Optimal Path through those modules in order to cover them with your balance.
- Remaining modules that could not be covered by your cube balance, sorted by Tier.
- Total costs, Savings with the provided strategy and the remaining costs.
- Modules which you will have to buy, sorted by Tier.
- Modules which you can get for free, sorted by Tier.
- Anticipated remaining costs: This will be the number of cubes you definitely need to get.

### Example Output
<img width="798" height="347" alt="image" src="https://github.com/user-attachments/assets/58014c0c-4ed6-47e3-9339-14ab3ec96dd2" />


## Requirements
There are no requirements, because the tool does in fact have no dependencies at all!

## User Guide
Before starting Cube Saver you should get all the necessary information needed for the analysis.
It needs your current cube balance, as well as the number of modules per Tier from your persued learning path.
After you got that information, just start the cli using `python3 cube_saver.py`.
You will be asked for the aforementioned numbers and receive all details about the cheapest strategy with respect to your current cube balance afterwards.
