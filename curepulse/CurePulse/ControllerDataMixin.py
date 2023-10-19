class ControllerDataMixin:

    def get_labels_by_key(self, key):
        labels = {
            0: [1, 2],
            1: [3, 3.5],
            2: [4, 4.5, 5], 
            'us': [3, 3.5, 4, 4.5, 5],
            'canada_and_england': [2, 3, 3.5, 4], 
            'others': [1, 2],
            'Agent_Language_Scores': [1, 2, 3, 3.5, 4, 4.5, 5],
            'Agent_Langauge_Score_Percentage': [1, 2, 3, 3.5, 4, 4.5, 5]
        }

        list_scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
        aggregated_scores = [f'{score}_Agg' for score in list_scores]
        if key in aggregated_scores:
            return [1, 2, 3, 3.5, 4, 4.5, 5]
        return labels[key]
        
    def get_n_clusters_by_key(self, key):
        cluster_numbers = {
            0: 2, 
            1: 2, 
            2: 3, 
            'us': 5, 
            'canada_and_england': 4, 
            'others': 2, 
            'Agent_Language_Scores': 7,
            'Agent_Langauge_Score_Percentage': 7,
            }
        list_scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
        aggregated_scores = [f'{score}_Agg' for score in list_scores]
        if key in aggregated_scores:
            return 7
        return cluster_numbers[key]

    def get_cluster_name_by_key(self, key):
        cluster_names = {
            0: 'Negative', 
            1: 'Neutral', 
            2: 'Positive', 
        }
        if key in cluster_names:
            return cluster_names[key]
        return key