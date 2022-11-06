import tempfile
from dp_serial.client.diffprivlib import serialize_pipeline
import requests
import json
import pickle
import pandas as pd
import numpy as np
from io import StringIO

class Client():
    def __init__(self, url, team_name = None):
        self.url = url
        self.headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        if team_name:
            self.team_name = team_name
            self.headers["x-oblv-user-name"] =  team_name

    def diffprivlib(self, pipeline):
        pipeline_str = serialize_pipeline(pipeline)
        pipeline_json = json.loads(pipeline_str)
        res = self._exec("diffprivlib", pipeline_json)
        if res.status_code == 200:
            return pickle.loads(res.content)
        else:
            print(f"Error while processing Diffprivlib request in enclave status code: {res.status_code} message: {res.text}")
            return res.text

    def opendp(self, opendp_pipeline) -> pd.DataFrame:
        opendp_json = json.loads(opendp_pipeline.to_json())
        res = self._exec("opendp", opendp_json)
        if res.status_code == 200:
            data = res.content.decode('utf8')
            df = pd.DataFrame(StringIO(data))
            return df
        else:
            print(f"Error while processing OpenDP request in enclave status code: {res.status_code} message: {res.text}")
            return res.text

    def synth(self, model, eps, delta = 0, select_cols = [], mul_matrix: np.ndarray = np.array([])) -> pd.DataFrame:
        res = self._exec("smartnoise_synth", {
            "model": model, 
            "epsilon": eps, 
            "delta": delta,
            "select_cols": select_cols,
            "mul_matrix": mul_matrix.tolist()
        })
        if res.status_code == 200:
            data = res.content.decode('utf8')
            df = pd.read_csv(StringIO(data))
            return df
        else:
            print(f"Error while executing provided query in enclave status code: {res.status_code} message: {res.text}")
            return res.text

    def sql(self, query, eps, delta) -> pd.DataFrame:
        res = self._exec("smartnoise_sql", {
            "query_str": query, 
            "epsilon": eps, 
            "delta": delta
        })
        if res.status_code == 200:
            data = res.content.decode('utf8')
            df = pd.read_csv(StringIO(data))
            return df
        else:
            print(f"Error while executing provided query in enclave status code: {res.status_code} message: {res.text}")
            return res.text

    def sql_privacy_estimate(self, query, eps, delta) -> dict:
        res = self._exec("smartnoise_sql_cost", {
            "query_str": query, 
            "epsilon": eps, 
            "delta": delta
        })
        if res.status_code == 200:
            return res.content.decode('utf8')
        else:
            print(f"Error while executing provided query in enclave status code: {res.status_code} message: {res.text}")
            return res.text

    def get_total_epsilon(self):
        res = requests.get(self.url+"/" + "total_epsilon", headers=self.headers)
        if res.status_code == 200:
            return res.content.decode('utf8')
        else:
            print(f"Error while fetching total_delta used status code: {res.status_code} message: {res.text}")
            return res.text

    def get_total_delta(self):
        res = requests.get(self.url+"/" + "total_delta", headers=self.headers)
        if res.status_code == 200:
            return res.content.decode('utf8')
        else:
            print(f"Error while fetching total_delta used status code: {res.status_code} message: {res.text}")
            return res.text
    
    def get_score(self):
        res = requests.get(self.url+"/" + "score", headers=self.headers)
        if res.status_code == 200:
            return res.content.decode('utf8')
        else:
            print(f"Error while fetching total_delta used status code: {res.status_code} message: {res.text}")
            return res.text

    def get_accuracy(self):
        res = requests.get(self.url+"/" + "accuracy", headers=self.headers)
        if res.status_code == 200:
            return res.content.decode('utf8')
        else:
            print(f"Error while fetching total_delta used status code: {res.status_code} message: {res.text}")
            return res.text

    def submit_predictions_comp(self, submission: pd.DataFrame):

        tmp = tempfile.NamedTemporaryFile()
        # Open the file for writing.
        with open(tmp.name, 'w') as f:
            submission.to_csv(f, index=False)
        # make prediciton dataframe and save to file
        # pred_df = pd.DataFrame(data=predictions, columns = ['labels'],index = test_x.index)
        # pred_df.to_csv('submission.csv')
        response = requests.post(self.url+'/submit', files = {"file": open(tmp.name, "rb")})
        return response.content

    def _exec(self, endpoint, body_json: dict):
        # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(self.url+"/"+endpoint, json=body_json, headers=self.headers)
        return r


