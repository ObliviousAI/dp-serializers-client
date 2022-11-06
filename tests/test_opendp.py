import dp_serial.opendp_logger.trans as trans

def test_serialize_deserialize():
    income_preprocessor = (
        # Convert data into a dataframe where columns are of type Vec<str>
        trans.make_split_dataframe(separator=",", col_names=["hello", "world"]) >>
        # Selects a column of df, Vec<str>
        trans.make_select_column(key="income", TOA=str)
    )

    expected_json= """{"version": "0.6.1", "ast": {"func": "make_chain_tt", "module": "comb", "type": "Transformation", "args": {"_tuple": true, "_items": [{"func": "make_select_column", "module": "trans", "type": "Transformation", "args": {"_tuple": true, "_items": []}, "kwargs": {"key": "income", "TOA": "py_type:str"}}, {"func": "make_split_dataframe", "module": "trans", "type": "Transformation", "args": {"_tuple": true, "_items": []}, "kwargs": {"separator": ",", "col_names": ["hello", "world"]}}]}, "kwargs": {}}}"""
    # the ast to json to be sent
    json_obj = income_preprocessor.to_json()

    # assert expected value
    assert json_obj == expected_json