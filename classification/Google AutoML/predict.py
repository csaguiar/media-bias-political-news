'''
Call Google AutoML Api to get the predictions of the custom model

Don't forget to add the path to the key file, more info in:
https://cloud.google.com/docs/authentication/getting-started
export GOOGLE_APPLICATION_CREDENTIALS=key-file-path

Usage:
    python predict.py <project_id> <model_id>
'''
import sys
import pandas as pd
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'text_snippet': {'content': content, 'mime_type': 'text/plain' }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

if __name__ == '__main__':
    project_id = sys.argv[1]
    model_id = sys.argv[2]

    dataset_test = pd.read_csv("dataset_oos_google.csv")
    data_pred = []
    for i, row in dataset_test.iterrows():
        print(i)
        try:
            request = get_prediction(row["content"], project_id,  model_id)
            name1 = request.payload[0].display_name
            score1 = request.payload[0].classification.score
            name0 = request.payload[1].display_name
            score0 = request.payload[1].classification.score
            data_pred.append(dict([(name1, score1), (name0, score0)]))
        except:
            # Error adds a dummy value
            data_pred.append(dict([("1", -9999), ("0", -9999)]))


    data_pred = pd.DataFrame(data_pred)

    data_pred.to_csv("predictions.csv", index=False)
