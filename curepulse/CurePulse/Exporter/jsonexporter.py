
import numpy as np

class JsonExporter:
    def save_to_json(self, data, cluster_labels, date, score_name):
    clustered_data = np.concatenate((data[0].values, data[1].values,data[2].values), axis=0)
    json_data = {
        "Date": date,
        "ScoreName": score_name,
        "ClusteredData": [
            {'Score': data_point.tolist(), 'Star': int(cluster_label)}
            for data_point, cluster_label in zip(clustered_data, cluster_labels)
        ],
    }

    output_json_file = f'clustered_data_{date}_{score_name}.json'
    with open(output_json_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)