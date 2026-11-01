
import math
import matplotlib.pyplot as plt

from Zone_splitting_Ibrahim import (
    active_phone_users_in_city_A,
    channels_in_cell_n,
    carried_traffic,
    number_of_cells_C
)

# ---------------------------------
# Network Parameters
# ---------------------------------

N = 700           # Total available channels ثابث
population = 8_600_000 #ثابت
mobile_users_fraction = 0.8
average_call_minutes = [0.5,1,2,3] 
caller_fractions = 0.25

# Calculate traffic for each percentage
traffic_values = [
    active_phone_users_in_city_A(
        population,
        mobile_users_fraction,
        caller_fractions,
        call_duration
    )
    for call_duration in average_call_minutes
]


# ---------------------------------
# Number of Cells Calculation
# ---------------------------------

def calculate_cells(K, G, U):

    n = channels_in_cell_n(N, U)

    k = carried_traffic(n, G)

    C = math.ceil(number_of_cells_C(K, k))

    return C


# ---------------------------------
# Graph 1: Blocking Probability U=4
# ---------------------------------

U = 4  

blocking_10 = [
    calculate_cells(K, 0.01, U)
    for K in traffic_values
]

blocking_5 = [
    calculate_cells(K, 0.005, U)
    for K in traffic_values
]

plt.figure(figsize=(9, 6))

plt.plot(traffic_values, blocking_10,
         'k-s', label='Blocking = 1%')

plt.plot(traffic_values, blocking_5,
         'k-^', label='Blocking = 0.5%')

plt.title('Number of Cells vs Traffic\n'
          'Different Blocking Probabilities')

plt.xlabel('Traffic to be Serviced (Erlang)')
plt.ylabel('Number of Cells')

plt.legend()
plt.xticks(traffic_values)
plt.grid(True, linestyle=':', color='gray')
plt.tight_layout()

plt.savefig('Blocking_Comparison_UnitCell=4.png', dpi=300)
plt.show()

# ---------------------------------
# Graph 2: Blocking Probability U=7
# ---------------------------------

U = 7  # Fixed unit size

blocking_10 = [
    calculate_cells(K, 0.01, U)
    for K in traffic_values
]

blocking_5 = [
    calculate_cells(K, 0.005, U)
    for K in traffic_values
]

plt.figure(figsize=(9, 6))

plt.plot(traffic_values, blocking_10,
         'k-s', label='Blocking = 1%')

plt.plot(traffic_values, blocking_5,
         'k-^', label='Blocking = 0.5%')

plt.title('Number of Cells vs Traffic\n'
          'Different Blocking Probabilities')

plt.xlabel('Traffic to be Serviced (Erlang)')
plt.ylabel('Number of Cells')

plt.legend()
plt.xticks(traffic_values)
plt.grid(True, linestyle=':', color='gray')
plt.tight_layout()

plt.savefig('Blocking_Comparison_UnitCell=7.png', dpi=300)
plt.show()

# ---------------------------------
# Graph 3: Buffering Distance Blocking 0.5%
# ---------------------------------

G = 0.005  # Fixed blocking probability

belt_1 = [
    calculate_cells(K, G, 4)
    for K in traffic_values
]

belt_2 = [
    calculate_cells(K, G, 7)
    for K in traffic_values
]

plt.figure(figsize=(9, 6))

plt.plot(traffic_values, belt_1,
         'k-s', label='Belt = 1 (U = 4)')

plt.plot(traffic_values, belt_2,
         'k-^', label='Belt = 2 (U = 7)')

plt.title('Number of Cells vs Traffic\n'
          'Different Buffering Distances')

plt.xlabel('Traffic to be Serviced (Erlang)')
plt.ylabel('Number of Cells')

plt.legend()
plt.xticks(traffic_values)
plt.grid(True, linestyle=':', color='gray')
plt.tight_layout()

plt.savefig('Buffering_Comparison_Blocking=0.5%.png', dpi=300)
plt.show()
# ---------------------------------
# Graph 4: Buffering Distance Blocking 1%
# ---------------------------------

G = 0.01  # Fixed blocking probability

belt_1 = [
    calculate_cells(K, G, 4)
    for K in traffic_values
]

belt_2 = [
    calculate_cells(K, G, 7)
    for K in traffic_values
]

plt.figure(figsize=(9, 6))

plt.plot(traffic_values, belt_1,
         'k-s', label='Belt = 1 (U = 4)')

plt.plot(traffic_values, belt_2,
         'k-^', label='Belt = 2 (U = 7)')

plt.title('Number of Cells vs Traffic\n'
          'Different Buffering Distances')

plt.xlabel('Traffic to be Serviced (Erlang)')
plt.ylabel('Number of Cells')

plt.legend()
plt.xticks(traffic_values)
plt.grid(True, linestyle=':', color='gray')
plt.tight_layout()

plt.savefig('Buffering_Comparison.png_Blocking=1%.png', dpi=300)
plt.show()
