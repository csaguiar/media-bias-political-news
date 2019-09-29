from keras.layers import (
    Activation,
    Dense,
    BatchNormalization,
    Bidirectional,
    Embedding,
    Conv1D,
    MaxPooling1D,
    GlobalMaxPool1D,
    Flatten,
    Dropout,
    LSTM
)
from keras.models import Sequential
from keras.optimizers import Adam
from keras.initializers import VarianceScaling


def cnn_model(params):
    vocab_size = params.get("vocab_size")
    embedding_size = params.get("embedding_size")
    embeddings = params.get("embeddings")
    max_length = params.get("max_length")

    model = Sequential(
        [
            Embedding(
                vocab_size,
                embedding_size,
                weights=[embeddings],
                input_length=max_length,
                trainable=False
            ),
            Conv1D(
                filters=64,
                kernel_size=4,
                activation='relu',
                kernel_initializer=VarianceScaling()
            ),
            MaxPooling1D(pool_size=3),
            Dropout(0.5),
            Conv1D(
                filters=64,
                kernel_size=4,
                activation='relu',
                kernel_initializer=VarianceScaling()
            ),
            MaxPooling1D(pool_size=3),
            Dropout(0.5),
            Flatten(),
            Dense(10, activation=None, kernel_initializer=VarianceScaling()),
            Activation("relu"),
            Dropout(0.5),
            Dense(1, activation='sigmoid', kernel_initializer='glorot_normal')
        ]
    )

    return model


def lstm_model(params):
    vocab_size = params.get("vocab_size")
    embedding_size = params.get("embedding_size")
    embeddings = params.get("embeddings")
    max_length = params.get("max_length")

    model = Sequential(
        [
            Embedding(
                vocab_size,
                embedding_size,
                weights=[embeddings],
                input_length=max_length,
                trainable=False
            ),
            LSTM(
                units=50,
                return_sequences=True
            ),
            GlobalMaxPool1D(),
            Dropout(0.5),
            Dense(
                50,
                activation=None
            ),
            BatchNormalization(),
            Activation("relu"),
            Dropout(0.5),
            Dense(1, activation='sigmoid', kernel_initializer='glorot_normal')
        ]
    )

    return model


def bi_lstm_model(params):
    vocab_size = params.get("vocab_size")
    embedding_size = params.get("embedding_size")
    embeddings = params.get("embeddings")
    max_length = params.get("max_length")

    model = Sequential(
        [
            Embedding(
                vocab_size,
                embedding_size,
                weights=[embeddings],
                input_length=max_length,
                trainable=False
            ),
            Bidirectional(
                LSTM(
                    units=50,
                    return_sequences=True
                ),
            ),
            GlobalMaxPool1D(),
            Dropout(0.5),
            Dense(
                50,
                activation=None
            ),
            BatchNormalization(),
            Activation("relu"),
            Dropout(0.5),
            Dense(1, activation='sigmoid', kernel_initializer='glorot_normal')
        ]
    )

    return model


def keras_model(model_dir, params):
    model_type = params.get("model_type")
    learning_rate = params.get("learning_rate")

    if model_type == "cnn":
        model = cnn_model(params)
    elif model_type == "lstm":
        model = lstm_model(params)
    elif model_type == "bi_lstm":
        model = bi_lstm_model(params)

    optimizer = Adam(lr=learning_rate)

    model.compile(
        loss='binary_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy']
    )

    return model
