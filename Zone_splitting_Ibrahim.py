import math
"""

    Z  zone_area
    N  city_spectrum_channels
    K  city_traffic          (carried busy-hour traffic, Erlang)
    G  acceptable_blocking
    U  cells_per_system_unit
    n  channels_in_cell
    a  offered_traffic_per_cell
    k  traffic_per_cell      (carried traffic a cell can serve)
    C  number_of_cells
    z  area_per_cell
    R  reuse_times
    Y  area_per_system_unit
    A  offered_traffic       (offered load used inside Erlang-B)
    B  blocking
"""

from erlang import  channels_N, capacity_A

def active_phone_users_in_city_A(population, mobile_users_fraction,percent_of_callers_from_mobile_users, average_call_minutes=3.0):
    return population*mobile_users_fraction*percent_of_callers_from_mobile_users*(average_call_minutes/60)

def channels_in_cell_n(spectrum_channels_N, cells_in_system_unit_U):
    """Average channels per cell n = N / U."""
    if cells_in_system_unit_U <= 0:
        raise ValueError("Cells per system unit must be positive")
    if spectrum_channels_N < 0:
        raise ValueError("City spectrum channels must be non negative")

    return spectrum_channels_N // cells_in_system_unit_U

def offered_traffic(channels_in_1_cell , blocking_rate_B):
    return capacity_A(channels_in_1_cell , blocking_rate_B)

def carried_traffic(channles_in_1_cell, blocking_rate_B):
    """Carried traffic k = (1 - G) * a that one cell can serve."""
    
    traffic = offered_traffic(channles_in_1_cell, blocking_rate_B)
    served_traffic = (1 - blocking_rate_B) * traffic
    return served_traffic

def number_of_cells_C(offered_traffic, offered_traffic_per_cell):#8
    """Target cell count C = A / a."""
    if offered_traffic_per_cell <= 0:
        raise ValueError("Traffic per cell must be positive")
    return offered_traffic / offered_traffic_per_cell

def area_per_cell_z(zone_area, cell_count):#9
    """Area per cell z = Z / C."""
    if cell_count <= 0:
        raise ValueError("Number of cells must be positive")
    return zone_area / cell_count

def reuse_times(cell_count, cells_per_system_unit):#10
    """How many times a frequency is reused in the zone: R = C / U."""
    if cells_per_system_unit <= 0:
        raise ValueError("Cells per system unit must be positive")
    return cell_count / cells_per_system_unit

def channels_needed_for_offered_traffic(offered_traffic_A, acceptable_blocking):
    """Channels required for given offered load and blocking: channels_N."""
    return channels_N(offered_traffic_A, acceptable_blocking)

def network_given_pupulation(
    spectrum_channels_N, blocking_rate_B,
    active_phone_users_in_city_A, Zone_area_Z,
    buffering_distance=1):
        # Use the already-computed active user count passed to this function.
    if buffering_distance==1:
        U=4
        
    elif buffering_distance==2:
        U=7
    else:
        raise ValueError("Buffering distance must be 1 or 2")    
        
    n=channels_in_cell_n(spectrum_channels_N,U)  
    
    #K = active_phone_users_in_city_A * (1 - blocking_rate_B)    
    k= carried_traffic(n,blocking_rate_B)
    a = offered_traffic(n, blocking_rate_B)
    C = math.ceil(number_of_cells_C(active_phone_users_in_city_A, a))
    
    R=reuse_times(C,U)
    
    z=area_per_cell_z(Zone_area_Z,C)
    
    return n,k,C,R,z

    