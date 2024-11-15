import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def summarizer(rawdocs):
    if not rawdocs.strip():
        return "", None, 0, 0

    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc]
    word_freq = {}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    if not word_freq:
        return "", None, len(rawdocs.split()), 0

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {}

    for sent in sent_tokens:
        sent_score = 0
        for word in sent:
            if word.text in word_freq.keys():
                sent_score += word_freq[word.text]
        if sent_score > 0:
            sent_scores[sent] = sent_score

    if not sent_scores:
        return "", None, len(rawdocs.split()), 0

    select_len = max(1, min(int(len(sent_tokens) * 0.3), len(sent_tokens)))
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = [sent.text for sent in summary]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.split()), len(summary.split())