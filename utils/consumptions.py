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