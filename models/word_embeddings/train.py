import csv
import collections
import numpy as np
import random
import tensorflow as tf
import math
import pickle
import sys


def save_variable_to_pickle(data, filename):
    handle = open(filename, 'wb')
    pickle.dump(data, handle)
    handle.close()

class Input:
    """docstring for Input."""
    def __init__(self, *args, **kwargs):
        self.filename = args[0]
        self.select_label = kwargs.get("select_label")
        self.output_name = kwargs.get("output_name", "untitled")
        self.text_corpus = None
        self.data = None
        self.count = None
        self.dictionary = None
        self.reversed_dictionary = None
        self.vocabulary_size = None

    def read_data(self):
        with open(self.filename) as csvfile:
            data = csv.DictReader(csvfile)
            text_corpus = []
            for row in data:
                if (self.select_label is None or
                        row["label"] == self.select_label):
                    text_corpus.append(row["content"].split())

        self.text_corpus = text_corpus

        return self.text_corpus

    def build_dataset(self, n_words):
        """Process raw inputs into a dataset."""
        count = [['UNK', -1]]
        count.extend(
            collections.Counter(x for document in self.text_corpus for x in document).most_common(n_words - 1))

        dictionary = dict()
        for word, _ in count:
            dictionary[word] = len(dictionary)
        data = list()
        unk_count = 0
        for sentence in self.text_corpus:
            for word in sentence:
                if word in dictionary:
                    index = dictionary[word]
                else:
                    index = 0  # dictionary['UNK']
                    unk_count += 1
                data.append(index)

        count[0][1] = unk_count
        reversed_dictionary = dict(
            zip(dictionary.values(), dictionary.keys()))

        self.vocabulary_size = len(dictionary)
        self.data = data
        self.count = count
        self.dictionary = dictionary
        self.reversed_dictionary = reversed_dictionary

        return data, count, dictionary, reversed_dictionary

    def save_to_file(self):
        data = {
            "dictionary": self.dictionary,
            "reversed_dictionary": self.reversed_dictionary
        }
        save_variable_to_pickle(data, "{}_input.pickle".format(self.output_name))


class Model:
    """docstring for Model."""
    def _default_params(self):
        return {
            "valid_size": 16,
            "valid_window": 100,
            "num_sampled": 64,
            "batch_size": 128,
            "embedding_size": 128,
            "skip_window": 1,
            "num_skips": 2,
            "num_steps": 100001
        }


    def __init__(self, *args, **kwargs):
        self.data_index = 0
        self.input = args[0]
        self.params = {**self._default_params(), **kwargs}
        valid_window = self.params["valid_window"]
        valid_size = self.params["valid_size"]
        self.params["valid_examples"] = np.random.choice(valid_window, valid_size, replace=False)
        self.output_name = kwargs.get("output_name", "untitled")
        self.final_embeddings = None

    def generate_batch(self):
        batch_size = self.params.get("batch_size")
        num_skips = self.params.get("num_skips")
        skip_window = self.params.get("skip_window")

        assert batch_size % num_skips == 0
        assert num_skips <= 2 * skip_window
        vocabulary = self.input.data

        batch = np.ndarray(shape=(batch_size), dtype=np.int32)
        context = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
        span = 2 * skip_window + 1  # [ skip_window input_word skip_window ]
        buffer = collections.deque(maxlen=span)

        for _ in range(span):
            buffer.append(vocabulary[self.data_index])
            self.data_index = (self.data_index + 1) % len(vocabulary)

        for i in range(batch_size // num_skips):
            target = skip_window  # input word at the center of the buffer
            targets_to_avoid = [skip_window]
            for j in range(num_skips):
                while target in targets_to_avoid:
                    target = random.randint(0, span - 1)
                targets_to_avoid.append(target)
                # this is the input word
                batch[i * num_skips + j] = buffer[skip_window]
                # these are the context words
                context[i * num_skips + j, 0] = buffer[target]
            buffer.append(vocabulary[self.data_index])
            self.data_index = (self.data_index + 1) % len(vocabulary)
        # Backtrack a little bit to avoid skipping words in the end of a batch
        self.data_index = (self.data_index + len(vocabulary) - span) % \
            len(vocabulary)
        return batch, context

    def train(self):
        graph = tf.Graph()
        batch_size = self.params.get("batch_size")
        valid_examples = self.params.get("valid_examples")
        num_sampled = self.params.get("num_sampled")
        embedding_size = self.params.get("embedding_size")
        num_steps = self.params.get("num_steps")
        vocabulary_size = self.input.vocabulary_size

        # Building the Graph
        with graph.as_default():
            train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
            train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
            valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

            embeddings = tf.Variable(
                tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
            embed = tf.nn.embedding_lookup(embeddings, train_inputs)

            # Construct the variables for the NCE loss
            nce_weights = tf.Variable(
                tf.truncated_normal([vocabulary_size, embedding_size],
                                    stddev=1.0 / math.sqrt(embedding_size)))
            nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

            # Compute the average NCE loss for the batch.
            # tf.nce_loss automatically draws a new sample of the negative labels each
            # time we evaluate the loss.
            loss = tf.reduce_mean(
              tf.nn.nce_loss(weights=nce_weights,
                             biases=nce_biases,
                             labels=train_labels,
                             inputs=embed,
                             num_sampled=num_sampled,
                             num_classes=vocabulary_size))

            # Construct the SGD optimizer using a learning rate of 1.0.
            optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)

            # Compute the cosine similarity between minibatch examples and all embeddings.
            norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
            normalized_embeddings = embeddings / norm
            valid_embeddings = tf.nn.embedding_lookup(
              normalized_embeddings, valid_dataset)
            similarity = tf.matmul(
              valid_embeddings, normalized_embeddings, transpose_b=True)

            # Add variable initializer.
            init = tf.global_variables_initializer()

        with tf.Session(graph=graph) as session:
            # We must initialize all variables before we use them.
            init.run()
            print('Initialized')

            average_loss = 0

            for step in range(num_steps):
                batch_inputs, batch_labels = self.generate_batch()
                feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}

                # We perform one update step by evaluating the optimizer op (including it
                # in the list of returned values for session.run()
                _, loss_val = session.run([optimizer, loss], feed_dict=feed_dict)
                average_loss += loss_val

                if step % 2000 == 0:
                    if step > 0:
                        average_loss /= 2000
                        # The average loss is an estimate of the loss over the last 2000 batches.
                        print('Average loss at step ', step, ': ', average_loss)
                        average_loss = 0

            self.final_embeddings = normalized_embeddings.eval()

    def export_embeddings_vocab(self):
        data = {
            "dictionary": self.input.dictionary,
            "reversed_dictionary": self.input.reversed_dictionary,
            "embeddings": self.final_embeddings
        }
        save_variable_to_pickle(data, "{}_embedding_vocab.pickle".format(self.output_name))


if __name__ == '__main__':
    select_label = None
    num_words = 10000
    for i, arg in enumerate(sys.argv):
        if arg == "--dataset":
            dataset_file = sys.argv[i+1]
        elif arg == "--output":
            output_name = sys.argv[i+1]
        elif arg == "--select":
            select_label = sys.argv[i+1]
        elif arg == "--num-words":
            num_words = int(sys.argv[i+1])

    input = Input(dataset_file, output_name=output_name, select_label=select_label)
    input.read_data()
    input.build_dataset(num_words)

    model = Model(input, output_name=output_name)
    model.train()
    model.export_embeddings_vocab()
