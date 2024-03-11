# %% 

import pandas as pd
from utils.run_opendc import runOpenDC
import matplotlib.pyplot as plt

from utils.plot_carbon_emission import plot_emissions

start_date = "2022-10-07"
end_date = "2022-10-14"
topology = "277"

workload_name = f"{start_date}_{end_date}"

# %%

#########################################################################################
#### RUN OPENDC START
#########################################################################################

runOpenDC(f"{start_date}_{end_date}", topology, "Output/")

#########################################################################################
#### RUN OPENDC END
#########################################################################################

# %%

#########################################################################################
#### LOAD INPUT TRACES START
#########################################################################################

df_trace = pd.read_parquet(f"Input/input_traces/{workload_name}/trace.parquet")
df_meta = pd.read_parquet(f"Input/input_traces/{workload_name}/meta.parquet")
df_energy = pd.read_parquet(f"Input/input_traces/{workload_name}/energy.parquet")

#########################################################################################
#### LOAD INPUT TRACES END
#########################################################################################

# %%

#########################################################################################
#### LOAD RESULTS START
#########################################################################################

df_server = pd.read_parquet(f"Output/workload={workload_name}/topology={topology}/server.parquet")
df_host = pd.read_parquet(f"Output/workload={workload_name}/topology={topology}/host.parquet")
df_service = pd.read_parquet(f"Output/workload={workload_name}/topology={topology}/service.parquet")

def add_absolute_timestamp(df, start_dt):
    df["absolute_timestamp"] = start_dt + pd.to_timedelta(df["timestamp"], unit="ms")


add_absolute_timestamp(df_host, df_meta["start_time"].min())
add_absolute_timestamp(df_server, df_meta["start_time"].min())
add_absolute_timestamp(df_service, df_meta["start_time"].min())


#########################################################################################
#### LOAD RESULTS END
#########################################################################################

# %%


plot_emissions(df_host, start_date, end_date)


# %%

df_host.energy_usage