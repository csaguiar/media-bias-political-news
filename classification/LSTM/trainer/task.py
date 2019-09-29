import argparse
import pickle
import subprocess
import os
import pandas as pd
from . import model
import nltk
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import (
    TensorBoard,
    ModelCheckpoint,
    EarlyStopping
)

WORKING_DIR = os.getcwd()
nltk.download('stopwords')
STOPWORDS = nltk.corpus.stopwords.words('english')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--job-dir',
        type=str,
        default="models",
        help='GCS location to write checkpoints and export models'
    )
    parser.add_argument(
        '--save-log',
        type=str,
        help='Where to save tensorboard files'
    )
    parser.add_argument(
        '--embedding-file',
        type=str,
        required=True,
        help='Embedding file name'
    )
    parser.add_argument(
        '--dataset-file',
        type=str,
        required=True,
        help='Dataset file name'
    )
    parser.add_argument(
        '--bucket-name',
        type=str,
        help='GCS bucket name'
    )
    parser.add_argument(
        "--num-epochs",
        type=int,
        default=200,
        help="Total number of epochs"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Batch size"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.001,
        help="Batch size"
    )
    parser.add_argument(
        "--model-type",
        type=str,
        help="Model Type"
    )
    parser.add_argument(
        "--early-stopping",
        type=bool,
        default=False,
        help="Early Stopping"
    )
    parser.add_argument(
        "--save-checkpoint",
        type=bool,
        default=True,
        help="Save checkpoint"
    )
    args, _ = parser.parse_known_args()
    return args


def get_path(job_dir, bucket_name, path):
    if "gs://" in job_dir:
        return gcp_path(bucket_name, path)
    else:
        return local_name(path)


def source_url(bucket_name, filename):
    return "gs://{0}/{1}".format(bucket_name, filename)


def gcp_path(bucket_name, filename):
    return "gs://{0}/{1}".format(bucket_name, filename)


def local_name(filename):
    return os.path.join(WORKING_DIR, filename)


def download_file_from_gc(source, destination):
    subprocess.check_call(
        [
            'gsutil',
            'cp',
            source,
            destination
        ]
    )


def download_files(bucket_name, filenames):
    local_files = []
    for filename in filenames:
        local_file = local_name(filename)

        if not os.path.exists(local_file):
            source_file = source_url(bucket_name, filename)

            download_file_from_gc(source_file, local_file)

        local_files.append(local_file)

    return local_files


def load_file_from_pickle(filename):
    with open(local_name(filename), "rb") as fid:
        data = pickle.load(fid)

    return data


def load_data(args):
    bucket_name = args.bucket_name
    embedding_file = os.path.join("data", args.embedding_file)
    dataset_file = os.path.join("data", args.dataset_file)
    filenames = [
        embedding_file,
        dataset_file
    ]

    download_files(bucket_name, filenames)

    embedding_data = load_file_from_pickle(embedding_file)
    embedding_data["vocab_size"] = len(embedding_data["dictionary"].keys())
    embedding_data["embedding_size"] = embedding_data["embeddings"].shape[1]
    dataset = pd.read_csv(local_name(dataset_file))

    return dataset, embedding_data


def build_sequence(text, dictionary):
    sequence = []
    for token in text.split():
        if (token not in STOPWORDS):
            if token in dictionary:
                sequence.append(dictionary[token])
            else:
                sequence.append(0)

    return sequence


def transform_data(dataset, dictionary, length_threshold=1500):
    dataset = dataset[dataset["label"] >= 0]
    sequences = dataset["content"].apply(
        lambda text: build_sequence(text, dictionary)
    )
    lengths = sequences.apply(lambda x: len(x))
    sequences = sequences[lengths <= length_threshold]

    X = sequences.to_numpy()
    max_length = max([len(x) for x in X])
    X = pad_sequences(X, padding='post', maxlen=max_length)
    y = (
        dataset.
        loc[lengths <= length_threshold, "label"].
        values
    ).reshape(-1, 1)

    return X, y


def get_callbacks(args):
    callbacks = []

    if args.save_log is not None:
        base_name = args.model_type
        # Tensorboard callback
        logdir = "{}/scalars/{}".format(args.save_log, base_name)
        callback_tensorboard = TensorBoard(
            log_dir=get_path(args.job_dir, args.bucket_name, logdir),
            histogram_freq=1
        )

        callbacks.append(callback_tensorboard)

    if args.save_checkpoint:
        base_name = args.model_type
        filemodel = "checkpoint-" + base_name + "-min_loss.hdf5"
        filename = os.path.join(args.job_dir, filemodel)
        callback_checkpoint = ModelCheckpoint(
            filename,
            save_best_only=True,
            mode="min",
            monitor="val_loss"
        )

        callbacks.append(callback_checkpoint)

    if args.early_stopping:
        callback_stopping = EarlyStopping(
            monitor="val_loss",
            patience=3,
            mode="min"
        )

        callbacks.append(callback_stopping)

    return callbacks


def train_and_evaluate(X, y, embedding_data, args):
    max_length = X.shape[1]

    model_dir = args.job_dir
    X_train, X_validation, y_train, y_validation = train_test_split(
        X,
        y,
        stratify=y,
        test_size=0.25
    )

    params = {
        'learning_rate': args.learning_rate,
        'vocab_size': embedding_data["vocab_size"],
        'embedding_size': embedding_data["embedding_size"],
        'embeddings': embedding_data["embeddings"],
        'max_length': max_length,
        'model_type': args.model_type
    }
    model_train = model.keras_model(model_dir, params)

    train_params = {
        "batch_size": args.batch_size,
        "validation_data": (X_validation, y_validation),
        "epochs": args.num_epochs,
        "verbose": 1,
        "callbacks": get_callbacks(args)
    }

    history = model_train.fit(X_train, y_train, **train_params)
    return history


if __name__ == '__main__':
    args = get_args()
    dataset, embedding_data = load_data(args)
    X, y = transform_data(dataset, embedding_data["dictionary"])
    train_and_evaluate(X, y, embedding_data, args)
