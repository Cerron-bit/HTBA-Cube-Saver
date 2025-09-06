# Please enter those for calculation.
cubes = 0
modules_per_tier = [0, 0, 0, 0, 0]

# standard values for initialisation.
cashback = [10, 10, 20, 100, 200]
costs = [10, 50, 100, 500, 1000]
# the costs after the modules cashback is subtracted.
true_costs = []
# priority of tier-rank.
internal_tier_values = [1, 2, 3, 4, 5]
input_steps = [
    'Please enter your balance of cubes:                            ',
    'How many Tier 0 modules are required?                          ',
    'How many Tier I modules are required?                          ',
    'How many Tier II modules are required?                         ',
    'How many Tier III modules are required?                        ',
    'How many Tier IV modules are required?                         '
]


def get_inputs() -> None:
    """
    Enforces input restrictions and sets cubes and modules_per_tier.
    """
    # initialise variables.
    round = 0
    tmp = 0
    # go through all required inputs.
    while round < len(input_steps):
        # enforce input restrictions.
        while True:
            try:
                tmp = int(input(input_steps[round]))
                if tmp < 0:
                    raise ValueError
                break
            except ValueError:
                print('Please enter a non-negative integer.')
        # set the values.
        if round == 0:
            global cubes
            cubes = tmp
        else:
            modules_per_tier[round - 1] = tmp
        round += 1

def get_true_costs() -> None:
    """
    Calculates the remaining costs after receiving cashback from completing the module.
    """
    for tier in range(5):
        actual_cost = costs[tier] - cashback[tier]
        true_costs.append(actual_cost)

def convert_to_1_0_knapsack() -> tuple[list[int], list[int]]:
    """
    Convert bounded knapsack problem to 1-0 knapsack problem.
    :return: the weights and values of the knapsack problem.
    """
    ks_weights = []
    ks_values = []
    for tier in range(5):
        number_of_modules = 0
        while number_of_modules < modules_per_tier[tier]:
            ks_weights.append(true_costs[tier])
            ks_values.append(internal_tier_values[tier])
            number_of_modules += 1
    return ks_weights, ks_values

def get_dp_table(weights: list[int], values: list[int]) -> list[list[int]]:
    """
    Uses the 1-0 knapsack algorithm to find the best configuration of modules
    to get the most out of your square cubes.
    :param weights: a list of costs per module.
    :param values: a list of importance per module.
    :return: a table of modules configurations.
    """
    # Initialise the dp_table.
    number_of_modules = len(weights)
    dp_table = [[0 for _ in range(cubes + 1)] for _ in range(number_of_modules + 1)]

    # Fill table dp_table from bottom up.
    for i in range(number_of_modules + 1):
        for w in range(cubes + 1):
            if i == 0 or w == 0:
                dp_table[i][w] = 0
            elif weights[i - 1] <= w:
                dp_table[i][w] = max(values[i - 1] + dp_table[i - 1][w - weights[i - 1]], dp_table[i - 1][w])
            else:
                dp_table[i][w] = dp_table[i - 1][w]
    return dp_table

def int_to_tier_str(last_tier: int) -> str:
    """
    Converts an integer into a string representation of its tier rank.
    :param last_tier: the tier rank as integer.
    :return: the string representation of the tier rank.
    """
    tier_str = "Tier "
    if last_tier == 0:
        tier_str += '0'
    elif last_tier < 4:
        tier_str += 'I' * last_tier
    else:
        tier_str += 'IV'
    return tier_str

def aggregate_tier_str(counter, tier) -> str:
    """
    Aggregates the number of modules of one tier into a compact
    string representation.
    :param counter: the number of modules of one tier.
    :param tier: the tier rank.
    :return: the string representation.
    """
    string = ''
    string += str(counter) + 'x '
    string += int_to_tier_str(tier)
    return string

def compress_path(module_path) -> str:
    """
    Compresses the path_list to a string.
    :param module_path: the module path as list.
    :return: the compressed path as string.
    """
    path_string = ''
    module_counter = 1
    # initialise with non-existent tier for start.
    last_tier = -1
    path_index = 0

    while path_index < len(module_path):
        # check if this is the first entry.
        if path_index == 0:
            last_tier = module_path[path_index]
        # Check if this is the last entry.
        elif path_index == len(module_path) - 1:
            if path_string != '':
                path_string += ' => '
            if module_path[path_index] == last_tier:
                module_counter += 1
                path_string += aggregate_tier_str(module_counter, last_tier)
            else:
                # add second to last entry first.
                path_string += aggregate_tier_str(module_counter, last_tier)
                path_string += ' => '
                path_string += aggregate_tier_str(1, module_path[path_index])
        # If this entry is somewhere in the middle.
        else:
            if module_path[path_index] == last_tier:
                module_counter += 1
            else:
                if path_string != '':
                    path_string += ' => '
                path_string += aggregate_tier_str(module_counter, last_tier)
                # reset variables.
                last_tier = module_path[path_index]
                module_counter = 1
        # update loop variable.
        path_index += 1
    return path_string

def get_paid_modules() -> tuple[list[int], str]:
    """
    Determine which modules can be covered by the current cube balance
    and plan the optimal path to do so.
    :return: the modules included and the optimal path through them.
    """
    # calculate global variable.
    get_true_costs()
    # get values for knapsack problem.
    weights, values = convert_to_1_0_knapsack()
    number_of_modules = len(weights)
    # solve knapsack problem.
    dp_table = get_dp_table(weights, values)
    # initialise variables to gather the results.
    modules_included = [0, 0, 0, 0, 0]
    module_path = []
    # set w to cubes so that we don't subtract from the real cube balance.
    w = cubes
    # traverse the dp_table backwards.
    for i in range(number_of_modules, 0, -1):
        if dp_table[i][w] != dp_table[i - 1][w]:
            # determine which modules where used.
            tier_number = dp_table[i][w] - dp_table[i - 1][w]
            # create the backwards path and sum up the covered modules.
            module_path.append(tier_number - 1)
            modules_included[tier_number - 1] += 1
            # update w for further traversal.
            w -= weights[i - 1]
    # reverse module_path to have it face from start to end.
    module_path = compress_path(list(reversed(module_path)))
    return modules_included, module_path

def calculate_savings(modules_included) -> tuple[int, int]:
    """
    Calculate the savings after using the proposed the strategy.
    :param modules_included: the modules included in the path.
    :return: the remaining cubes and the saved cubes.
    """
    remaining_cubes = cubes
    savings = 0
    for tier in range(5):
        remaining_cubes -= modules_included[tier] * true_costs[tier]
        savings += modules_included[tier] * costs[tier]
    return remaining_cubes, savings

def perform_analysis() -> None:
    """
    Performs the analysis and outputs the results in the terminal.
    """
    # calculate the optimal strategy and it's savings.
    modules_included, module_path = get_paid_modules()
    remaining_cubes, savings = calculate_savings(modules_included)

    # initialise aggregation variables.
    total_costs = 0
    needed_modules = 0
    paid_modules = 0
    remaining_modules = []
    # aggregate values into our aggregation variables.
    for tier in range(5):
        needed_modules += modules_per_tier[tier]
        paid_modules += modules_included[tier]
        remaining_modules.append(modules_per_tier[tier] - modules_included[tier])
        total_costs += modules_per_tier[tier] * costs[tier]

    # calculate what still needs to be covered.
    remaining_costs = total_costs - savings
    modules_to_buy, free_modules = filter_remaining_modules(remaining_modules, remaining_cubes)
    anticipated_savings = savings
    for tier in range(5):
        anticipated_savings += free_modules[tier] * costs[tier]
    anticipated_remaining_costs = total_costs - anticipated_savings

    # Print the results to the terminal.
    print('##################################################################################################')
    print('Current cube balance:                                    ' + str(cubes))
    print('Remaining cube balance:                                  ' + str(remaining_cubes))
    print('Modules financially covered by strategy:                 ' + str(paid_modules) + '/' + str(needed_modules))
    print('Optimal path through modules in tier-ranks:\n => ' + str(module_path))
    print('Remaining modules by tier-ranks:                         ' + str(remaining_modules))
    print('Total cube costs:                                        ' + str(total_costs))
    print('Covered cube costs:                                      ' + str(savings))
    print('Remaining cube costs:                                    ' + str(remaining_costs))
    print('##################################################################################################')
    print('Buying the modules from the highest tier down to the lowest after the strategy above results in...')
    print(' -> Modules to pay for by tier-ranks:                    ' + str(modules_to_buy))
    print(' -> Free modules through cashback by tier-ranks:         ' + str(free_modules))
    print(' -> Anticipated remaining costs:                         ' + str(anticipated_remaining_costs))
    print('##################################################################################################')


def filter_remaining_modules(remaining_modules, remaining_cubes) -> tuple[list[int], list[int]]:
    """
    Filter out all modules that will be covered by cashback.
    :param remaining_modules: a list of remaining modules.
    :param remaining_cubes: the remaining number of cubes.
    :return: a list of modules that need to be bought and a list of modules covered by cashback.
    """
    # copy remaining_modules, so that remaining_modules is still intact.
    copy_remaining_modules = remaining_modules.copy()
    modules_to_buy = [0, 0, 0, 0, 0]
    free_modules = [0, 0, 0, 0, 0]
    for tier in range(4, -1, -1):
        while copy_remaining_modules[tier] > 0:
            if remaining_cubes >= costs[tier]:
                # subtract the true_costs so the cashback is added back to the remaining_cubes.
                remaining_cubes -= true_costs[tier]
                free_modules[tier] += 1
            else:
                # just buy another module.
                remaining_cubes += cashback[tier]
                modules_to_buy[tier] += 1
            copy_remaining_modules[tier] -= 1
    return modules_to_buy, free_modules

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_inputs()
    perform_analysis()
