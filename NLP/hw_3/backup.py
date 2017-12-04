# -*- coding: utf-8 -*-
from keras.layers.core import Activation, Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
from keras.utils.np_utils import to_categorical
import collections
import nltk
import numpy as np


def pre_data(xpath, ypath, max_features, max_sentence_len):
    maxlen = 0
    word_freqs = collections.Counter()
    num_recs = 0
    with open(xpath, 'r+') as f:
        for line in f:
            sentence = line.strip()
            words = nltk.word_tokenize(sentence.lower())
            if len(words) > maxlen:
                maxlen = len(words)
            for word in words:
                word_freqs[word] += 1
            num_recs += 1
    print('maxlen ', maxlen)
    print('wordscount ', len(word_freqs))

    ## 准备数据
    MAX_FEATURES = max_features
    MAX_SENTENCE_LENGTH = max_sentence_len
    vocab_size = min(MAX_FEATURES, len(word_freqs)) + 2
    word2index = {x[0]: i + 2 for i, x in enumerate(word_freqs.most_common(MAX_FEATURES))}
    word2index["PAD"] = 0
    word2index["UNK"] = 1
    print(word2index)
    index2word = {v: k for k, v in word2index.items()}
    X = []
    y = np.zeros(num_recs)
    i = 0
    with open(xpath, 'r+') as f:
        for line in f:
            sentence = line.strip()
            words = nltk.word_tokenize(sentence.lower())
            seqs = []
            for word in words:
                if word in word2index:
                    seqs.append(word2index[word])
                else:
                    seqs.append(word2index["UNK"])
            X.append(seqs)

    with open(ypath, 'r+') as f:
        for line in f:
            y[i] = int(line) - 1
            i += 1
    X = sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)

    return X, y, vocab_size, index2word


def main():

    X, y, vocab_size, index2word = pre_data('./train_x.txt', './train_y.txt', 7000, 53)

    Xtest, ytest, vocab_size_test, index2word_test = pre_data('./test_x.txt', './random.txt', 7000, 53)

    ## 网络构建
    EMBEDDING_SIZE = 256
    HIDDEN_LAYER_SIZE = 128
    BATCH_SIZE = 90
    NUM_EPOCHS = 1
    model = Sequential()
    model.add(Embedding(vocab_size, EMBEDDING_SIZE, input_length=53))
    model.add(LSTM(HIDDEN_LAYER_SIZE, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(5))
    model.add(Activation("softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam",metrics=["accuracy"])
    ## 网络训练
    y_cat = to_categorical(y, 5)
    ytest_cat = to_categorical(ytest, 5)
    print(Xtest.shape)
    print(ytest_cat.shape)
    model.fit(X,
              y_cat,
              batch_size=BATCH_SIZE, epochs=NUM_EPOCHS, validation_data=(Xtest, ytest_cat))
    ## 预测
    score, acc = model.evaluate(Xtest, ytest_cat, batch_size=BATCH_SIZE)
    print("\nTest score: %.3f, accuracy: %.3f" % (score, acc))
    result = open('MF1733061.txt', 'w')
    # 获取预测结果
    for i in range(len(Xtest)):
        xtest = Xtest[i].reshape(1, 53)
        ylabel = ytest[i]
        ypred = model.predict(xtest)[0]
        max = 0
        index = 0
        for j in range(5):
            if max < ypred[j]:
                max = ypred[j]
                index = j
        result.write(str(index+1)+'\n')
    result.close()



def multi_tag(data):
    result = np.zeros([len(data), 5])
    for i in range(len(data)):
        result[i] = 0
        result[i][int(data[i])] = 1

    return result


if __name__ == '__main__':
    main()
