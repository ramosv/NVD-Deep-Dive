import json
import os
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import nltk
import json

nltk.download("punkt")
nltk.download("stopwords")


def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


custom_stop_words = set(ENGLISH_STOP_WORDS).union(
    {
        "file",
        "data",
        "information",
        "system",
        "security",
        "attack",
        "network",
        "user",
        "admin",
        "use",
        "access",
        "code",
        "service",
        "allow",
        "attack",
        "control",
        "vulnerability",
        "execute",
        "remote",
        "local",
        "via",
        "issue",
        "affect",
        "impact",
        "result",
    }
)


stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))


def tokenize_and_stem(text):
    text = "".join([char for char in text if char not in string.punctuation])
    tokens = word_tokenize(text)
    stems = [
        stemmer.stem(item)
        for item in tokens
        if item.lower() not in stop_words and not item.isdigit()
    ]
    return stems


def count_term_frequencies(descriptions):
    all_words = [word for desc in descriptions for word in tokenize_and_stem(desc)]
    term_frequencies = Counter(all_words)
    return term_frequencies


def preprocess_stop_words(stop_words_set):
    joined_stop_words = " ".join(stop_words_set)
    processed_stop_words = tokenize_and_stem(joined_stop_words)
    processed_stop_words_list = list(set(processed_stop_words))
    return processed_stop_words_list


def load_data(directory):
    descriptions = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                print(f"Now reviewing file: {file}")
                for item in data:
                    for desc in item["cve"]["descriptions"]:
                        if desc["lang"] == "en":
                            descriptions.append(desc["value"])
    return descriptions


def apply_tfidf(descriptions, stop_words):
    vectorizer = TfidfVectorizer(
        tokenizer=tokenize_and_stem,
        stop_words=stop_words,
        max_features=10000,
        ngram_range=(1, 2),
        strip_accents="unicode",
    )

    tfidf_matrix = vectorizer.fit_transform(descriptions)
    feature_names = vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names


def top_tfidf_feats(row, features, top_n=20):
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    return top_feats


def top_feats_in_doc(tfidf_matrix, features, doc_id, top_n=20):
    row = np.squeeze(tfidf_matrix[doc_id].toarray())
    return top_tfidf_feats(row, features, top_n)


if __name__ == "__main__":
    descriptions = load_data("all_data")
    custom_stop_words_list = list(custom_stop_words)
    processed_stop_words = preprocess_stop_words(custom_stop_words_list)

    tfidf_matrix, feature_names = apply_tfidf(descriptions, processed_stop_words)

    term_frequencies = count_term_frequencies(descriptions)
    top_term_freqs = term_frequencies.most_common(50)

    top_tfidf_features = []
    for doc_id in range(min(10, tfidf_matrix.shape[0])):
        top_features = top_feats_in_doc(tfidf_matrix, feature_names, doc_id, top_n=20)
        top_tfidf_features.append({f"document_{doc_id}": top_features})

    output_data = {
        "term_frequencies": top_term_freqs,
        "top_tfidf_features": top_tfidf_features,
    }

    save_to_json(output_data, "output_data.json")
