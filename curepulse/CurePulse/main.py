from DataLoader.MongoDBLoader import MongoDBLoader
from .controller import Controller
from Preprocessor.DataPreprocessor import DataPreprocessor
from Clustering.agglomerative import Agglomerative

loader = MongoDBLoader()
score = 'Agent_Language_Scores'
processor = DataPreprocessor(loader.get_data('2023-10-13'))
model = Agglomerative()
df = processor.select_data()
data = processor.split_and_sort(df, score)
column_name = f'{score}_Star_Rating'
labels = model.fit_transform(data[score].values, 7, [], labels=[1, 2, 3, 3.5, 4, 4.5, 5], linkage='ward')
data[score].df[column_name] = labels
df = data[score].df.sort_values(by='SUM')
print(df[df[column_name]==4.5])




