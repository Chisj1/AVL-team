import pandas as pd
import model.preprocessor as Preprocessor
import pickle


def load_model():
    with open('./model/phishing.pkl', 'rb') as f:
        return pickle.load(f)


def check(url):
    model = load_model()
    data = pd.DataFrame(Preprocessor.process_url(url), index=[0])
    return bool(model.predict(data)[0])
