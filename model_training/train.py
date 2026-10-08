# train the model on the data from data_gen.py
# run data_gen first then this

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


def train_model() :
    df = pd.read_csv('processes_data.csv')

    features = ['burst_time', 'io_frequency', 'memory_usage']
    target = 'process_type'

    X = df[features]
    y = df[target]

    # 80 % to learn .. 20 % to test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier(max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f'test accuracy : {accuracy * 100:.2f} %')

    joblib.dump(model, 'scheduler_model.pkl')
    print('model saved -> scheduler_model.pkl')


# end point
train_model()
