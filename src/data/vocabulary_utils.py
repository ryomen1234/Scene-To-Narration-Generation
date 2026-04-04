import re
from collections import Counter


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


class Vocabulary:
    def __init__(self, min_freq=1):
        self.min_freq = min_freq

        self.word2idx = {
            "<PAD>": 0,
            "<SOS>": 1,
            "<EOS>": 2,
            "<UNK>": 3,
        }

        self.idx2word = {idx: word for word, idx in self.word2idx.items()}

    def tokenize(self, text):
        return text.split()

    def __len__(self):
        return len(self.word2idx)

    def build_vocab(self, text):
        counter = Counter()

        text = clean_text(text)
        tokens = self.tokenize(text)

        counter.update(tokens)

        for word, freq in counter.items():
            if freq >= self.min_freq and word not in self.word2idx:
                idx = len(self.word2idx)
                self.word2idx[word] = idx
                self.idx2word[idx] = word

    def encode(self, text):
        text = clean_text(text)
        tokens = ["<SOS>"] + self.tokenize(text) + ["<EOS>"]

        return [
            self.word2idx.get(t, self.word2idx["<UNK>"])
            for t in tokens
        ] 

    def decode(self, seq):
        words = [
            self.idx2word.get(i, "<UNK>") for i in seq
        ]

        return " ".join(words)