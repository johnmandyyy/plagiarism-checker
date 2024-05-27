from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize
from transformers import pipeline
import re
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import random
import torch
import nltk

from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLTK components
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('stopwords')




lemmatizer = WordNetLemmatizer()


def extract_text_from_pdf(pdf_path):
    """Extract texts from PDF."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_valid_phrases(text):
    sentences = sent_tokenize(text)
    classifier = pipeline(
        "text-classification", model="bert-base-uncased", return_all_scores=True
    )
    valid_phrases = []

    for sentence in sentences:

        if re.match(r"^[A-Za-z][^\.:]*[\.:]$", sentence):

            scores = classifier(sentence)
            sentence_is_valid = scores[0][1]["score"] > 0.1

            if sentence_is_valid == True:
                if (
                    len(re.findall(r"\w+", sentence)) > 2
                ):  # Make it is 3 words so it can be phrase.
                    if sentence not in valid_phrases:
                        valid_phrases.append(sentence)

    return valid_phrases


def preprocess(text):
    tokens = word_tokenize(text)
    tokens = [
        lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()
    ]
    return tokens


def generate_paraphrases(text):
    tokens = preprocess(text)
    stop_words = set(stopwords.words("english"))
    paraphrases = []

    for i, token in enumerate(tokens):
        if token.lower() in stop_words or not token.isalpha():
            continue

        synonyms = set()
        for syn in wordnet.synsets(token):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace("_", " ")
                if synonym.lower() != token.lower():
                    synonyms.add(synonym)

        for synonym in synonyms:
            new_tokens = tokens.copy()
            new_tokens[i] = synonym
            paraphrases.append(" ".join(new_tokens))
    return paraphrases


def score_paraphrases(original_text, paraphrases):
    pass


def paraphrase(text):
    paraphrases = generate_paraphrases(text)
    return paraphrases


def get_texts_and_synonyms(valid_phrases):
    """Returns an interable dictionary that can be used to compare words."""
    __objects = []
    for phrase in valid_phrases:
        old_sentence = phrase.replace("\n", " ")
        options = paraphrase(old_sentence)
        new = ""
        if len(options) > 0:

            print(options[0])
            new = options[0]
            generated_index = random.randint(0, len(options) - 1)
            new = options[generated_index]

            __objects.append({"original_sentence": old_sentence, "new_sentence": new})

    return __objects


class TextPairDataset(Dataset):

    def __init__(self, dataframe, tokenizer, max_length):
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text1 = str(self.data.iloc[idx, 0])
        text2 = str(self.data.iloc[idx, 1])
        label = self.data.iloc[idx, 2]

        inputs = self.tokenizer(
            text1,
            text2,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        inputs = {key: val.squeeze(0) for key, val in inputs.items()}
        inputs["labels"] = torch.tensor(label, dtype=torch.long)

        return inputs


class BERTAlgorithm:

    def __init__(self):
        
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')

    def calculate_cosine(self, text_1, text_2):
        print("CALCULATING COSINE")
        inputs1 = self.tokenizer(text_1, return_tensors='pt', padding=True, truncation=True)
        inputs2 = self.tokenizer(text_2, return_tensors='pt', padding=True, truncation=True)

        # Obtain BERT embeddings
        with torch.no_grad():

            outputs1 = self.model(**inputs1)
            outputs2 = self.model(**inputs2)

        # Extract embeddings from BERT output
        embeddings1 = outputs1.last_hidden_state.mean(dim=1)  # Using mean pooling for simplicity
        embeddings2 = outputs2.last_hidden_state.mean(dim=1)

        # Calculate cosine similarity
        similarity_score = cosine_similarity(embeddings1, embeddings2)[0][0]
        return similarity_score


