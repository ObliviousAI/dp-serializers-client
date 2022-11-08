import json
import opendp_logger
opendp_logger.enable_logging()

import opendp.transformations as trans
from opendp.mod import enable_features
enable_features("contrib")

def test_serialize_deserialize():
    income_preprocessor = (
        # Convert data into a dataframe where columns are of type Vec<str>
        trans.make_split_dataframe(separator=",", col_names=["hello", "world"]) >>
        # Selects a column of df, Vec<str>
        trans.make_select_column(key="income", TOA=str)
    )

    expected_ast = """{"func": "make_chain_tt", "module": "combinators", "type": "Transformation", "args": {"_tuple": true, "_items": [{"func": "make_select_column", "module": "transformations", "type": "Transformation", "args": {"_tuple": true, "_items": []}, "kwargs": {"key": "income", "TOA": "py_type:str"}}, {"func": "make_split_dataframe", "module": "transformations", "type": "Transformation", "args": {"_tuple": true, "_items": []}, "kwargs": {"separator": ",", "col_names": ["hello", "world"]}}]}, "kwargs": {}}"""
    
    # the ast to json to be sent
    json_obj = json.dumps(json.loads(income_preprocessor.to_json())['ast'])

    # assert expected value
    assert json_obj == expected_ast
