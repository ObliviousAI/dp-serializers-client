# DP Serializers Client
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/)


# Client package for DP Serializer

The dp-seriel-client enables serialization of popular Differential Privacy frameworks.
The client in dp-serializers-client makes it possible to serialize and query data with a corresponding server running.


## Creating Enclave Client:
```python
from dp_serial.client.client import Client
enclave_client = Client("http://localhost:3031")
```
Once client is initialized it can be used to send requests to respective DP frameworks.

## Querying OpenDP
```python
import dp_serial.opendp_logger.trans as trans
import dp_serial.opendp_logger.meas as meas
import dp_serial.opendp_logger.comb as comb

pipeline = comb.make_pureDP_to_fixed_approxDP(
    trans.make_split_dataframe(separator=",", col_names=["col_1", "col_2", "col_3"]) >>
    trans.make_select_column(key="key_name", TOA=str) >>
    trans.make_cast(TIA=str, TOA=int) >>
    trans.make_impute_constant(0) >> 
    trans.make_clamp(bounds=(0, 1)) >>
    trans.make_bounded_sum((0, 1)) >>
    meas.make_base_discrete_laplace(scale=1.)
)

opendp_result = competition_enclaves.opendp(pipeline)

print(opendp_result) #Data from API server with DP applied
```

## Querying Diffprivlib
```python
from sklearn.pipeline import Pipeline
from diffprivlib import models

#Diffprivlib LR Pipeline 
lr_pipe = Pipeline([
    ('lr', models.LogisticRegression(data_norm=5))
])
trained_model = competition_enclaves.diffprivlib(splr_pipe, y_column="y_return") # Trained model from API Server with DP applied
```

## Querying Smartnoise-Synth
```python
cols_to_select = ["col_1", "col_2", "col_3"]
mat = numpy.array([[0.001,0.1,0.001], [0.01,0.1,0.02], [0.41,0.1,0.3]])

mwem_synthetic_data = competition_enclaves.synth("MWEM", 1, 0.0001, select_cols=cols_to_select, mul_matrix=mat)

print(mwem_synthetic_data) #Synthetic Data from API server
```

## Querying Smartnoise-SQL

```python
query_result = competition_enclaves.sql("SELECT col_1, COUNT(col_2) as ret_col_2 FROM comp.comp GROUP BY col_3", 1,0.0001)

print(query_result) # Resulting data from APIs with DP applied
```
