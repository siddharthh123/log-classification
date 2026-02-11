# from sentence_transformers import SentenceTransformer
# import joblib
#
# # Load the sentence transformer model
# transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
# # Load the saved classifier model
# classifier_model = joblib.load('models/log_classifier.joblib')
#
# def classify_with_bert(log_message):
#
#     # Compute embeddings for the log message
#     message_embedding = transformer_model.encode(log_message)
#
#     probabilities = classifier_model.predict_proba([message_embedding])[0]
#     if max(probabilities) >0.5:
#         return "Unclassified"
#     predicted_label = classifier_model.predict([message_embedding])[0]
#     return predicted_label
#     # Predict the class
#     predicted_class = classifier_model.predict([message_embedding])[0]
#
#     return predicted_class
#
# if __name__ == "__main__":
#     logs = [
#         "alpha.osapi_compute.wsgi.server - 12.10.11.1 - API returned 404 not found error",
#         "GET /v2/3454/servers/detail HTTP/1.1 RCODE 404 len: 1583 time: 0.1878400",
#         "System crashed due to drivers errors when restarting the server",
#         "Ladle!! nhi ho paya",
#         "Multiple login failures occurred on user 6454 account",
#         "Server A790 was restarted unexpectedly during the process of data transfer"
#     ]
#
#     for log in logs:
#         label = classify_with_bert(log)
#         print(log, "->", label)

import joblib
from sentence_transformers import SentenceTransformer

model_embedding = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight embedding model
model_classification = joblib.load("models/log_classifier.joblib")


def classify_with_bert(log_message):
    embeddings = model_embedding.encode([log_message])
    probabilities = model_classification.predict_proba(embeddings)[0]
    if max(probabilities) < 0.5:
        return "Unclassified"
    predicted_label = model_classification.predict(embeddings)[0]

    return predicted_label


if __name__ == "__main__":
    logs = [
        "alpha.osapi_compute.wsgi.server - 12.10.11.1 - API returned 404 not found error",
        "GET /v2/3454/servers/detail HTTP/1.1 RCODE   404 len: 1583 time: 0.1878400",
        "System crashed due to drivers errors when restarting the server",
        "Hey bro, chill ya!",
        "Multiple login failures occurred on user 6454 account",
        "Server A790 was restarted unexpectedly during the process of data transfer"
    ]
    for log in logs:
        label = classify_with_bert(log)
        print(log, "->", label)
