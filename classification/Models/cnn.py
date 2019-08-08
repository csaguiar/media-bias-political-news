"""
CNN model for bias classification using Tensorflow / Keras

Usage:
    python cnn.py --dataset <csv file with dataset> --embeddings <pickle file with embeddings>
"""
import pickle
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Embedding, Conv1D, MaxPooling1D, Flatten, Dropout
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
import os
import sys
import nltk
nltk.download('stopwords')
STOPWORDS = nltk.corpus.stopwords.words('english')
MODEL_NAME = "cnn"
VERSION = "1.0.0"
LOGS_FOLDER = "logs"

def load_embeddings(embedding_file):
    # Loads embeddings file and dicitionary
    with open(embedding_file, "rb") as fid:
        data = pickle.load(fid)

    return data["dictionary"], data["reversed_dictionary"], data["embeddings"]

def load_dataset(dataset_file):
    dataset = pd.read_csv(dataset_file)
    # Removing neutral articles
    return dataset[dataset["label"] >= 0]

def build_sequence(text, dictionary):
    sequence = []
    for token in text.split():
        if (token not in STOPWORDS):
            if token in dictionary:
                sequence.append(dictionary[token])
            else:
                sequence.append(0)
            
    return sequence    

def process_data(data, dictionary, length_threshold=1500):
    data["sequences"] = data["content"].apply(lambda t: build_sequence(t, dictionary))
    data["lenghts"] = data["sequences"].apply(lambda s: len(s))
    data = data[data["lenghts"] <= length_threshold]
    max_length = data["lenghts"].max()
    X = data["sequences"].values
    y = data["label"].values

    X = pad_sequences(X, padding='post', maxlen=max_length)

    return X, y

def train(X, y, embeddings, model_params, test_size=0.25):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=test_size)
    vocab_size, embeddings_size = embeddings.shape
    max_length = X.shape[1]
    print(max_length)
    model = Sequential(
        [
            Embedding(vocab_size, embeddings_size, weights=[embeddings], input_length=max_length, trainable=False),
            Conv1D(filters=64, kernel_size=4, activation='relu'),
            MaxPooling1D(pool_size=3),
            Conv1D(filters=64, kernel_size=4, activation='relu'),
            MaxPooling1D(pool_size=3),
            Flatten(),
            Dense(10, activation="relu", kernel_initializer='random_normal'),
            Dropout(0.5),
            Dense(1, activation='sigmoid', kernel_initializer='random_normal')
        ]
    )

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    # Tensorboard callback
    base_logdir = "scalars/{}_{}".format(MODEL_NAME, VERSION)
    logdir = os.path.join(LOGS_FOLDER, base_logdir)
    callback_tensorboard = TensorBoard(log_dir=logdir)
    
    epochs = model_params["epochs"]
    batch_size = model_params["batch_size"]
    history = model.fit(
        X_train,
        y_train,
        epochs=epochs, 
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        callbacks=[callback_tensorboard]
    )

    return model, history

def save_model(model):
    saved_model_name = "{}_{}.json".format(MODEL_NAME, VERSION)
    model_json = model.to_json()
    with open(saved_model_name, "w") as json_file:
        json_file.write(model_json)    


def load_model(model_filename):
    with open(model_filename, "r") as json_file:
        model_json = json_file.read()
        model = model_from_json(model_json)

    return model    

if __name__ == "__main__":
    dataset_file = None
    embedding_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--dataset":
            dataset_file = sys.argv[i+1]
        elif arg == "--embeddings":
            embedding_file = sys.argv[i+1]
    
    if (dataset_file is not None) and (embedding_file is not None):
        print("=> Loading Dataset")
        data = load_dataset(dataset_file)
        print("=> Loading Embeddings")
        dictionary, reversed_dictionary, embeddings = load_embeddings(embedding_file)
        print("=> Processing data")
        X, y = process_data(data, dictionary)
        print("=> Training model")
        model_params = {
            "epochs": 50,
            "batch_size": 32
        }
        model, history = train(X, y, embeddings, model_params)
        save_model(model)
    else:
        print("Something went wrong!")