def mri_consumption(kw_idle, kw_scan, scan_time =60, idle_time = 60):
  """
  Calculates the energy consumption of an MRI scanner.

  Args:
    kw_idle (float): Power consumption in kilowatts (kW) during idle mode.
    kw_scan (float): Power consumption in kilowatts (kW) during scan mode.
    scan_time (int, optional): Duration of the scan in minutes. Defaults to 60.
    idle_time (int, optional): Duration of idle time in minutes. Defaults to 60.

  Returns:
    float: Total energy consumption in kilowatt-hours (kWh).
  """
  kwh = (scan_time*kw_scan)/60 + (idle_time*kw_idle)/60

  return kwh


def cooling_consumption(mri_consumption, scan_time = 60):
  """
  Calculates the energy consumption required for cooling an MRI machine.

  This function models the cooling energy based on the MRI machine's energy consumption
  and a simplified Coefficient of Performance (COP) for cooling systems.

  Args:
    mri_consumption (float): The energy consumption of the MRI machine in kWh.
    scan_time (int, optional): The duration of the MRI scan in minutes. Defaults to 60.

  Returns:
    float: The estimated energy consumption for cooling in kilowatt-hours (kWh).
  """
  #Keeping the Coefficient of Performance (COP) a constant, but following the equation aiming to allows expanding the tool later based on the location and time
  cop_t_amb = 3.0 - 0.05 * (20 - 15)
  h_load = 0.95 * mri_consumption

  e_cool = h_load/cop_t_amb * scan_time/60


  return e_cool