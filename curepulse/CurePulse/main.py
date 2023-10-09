# from DataLoader.MongoDBLoader import MongoDBLoader
# from .controller import Controller
# from Preprocessor.DataPreprocessor import DataPreprocessor
# from Clustering.agglomerative import Agglomerative

# loader = MongoDBLoader()
# score = 'Agent_Accent_Score'
# processor = DataPreprocessor(loader.get_data('2023-09-08'))
# model = Agglomerative()
# df = processor.select_data()
# data = processor.split_and_sort(df, score)
# column_name = f'{score}_Star_Rating'
# for key in data.keys():
#     if score == 'Agent_Accent_Score':
#         labels = model.fit_transform(data[key].values, 2, self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key), model_name='kmeans')
#     else:
#         labels = model.fit_transform(data[key].values, 2, self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key))
#     data[key].df[column_name] = labels




