import os
print("RUNNING FROM:", os.path.abspath(os.getcwd()))

# # from processor_regex import classify_with_regex
# #
# # def classify_logs(logs):
# #     labels = []
# #     for source, log_msg in logs:
# #         label = classify_log(source, log_msg)
# #         labels.append(label)
# #     return labels
# #
# #
# # def classify_log(source, log_message):
# #     if source == "LegacyCRM":
# #         return None
# #
# #     label = classify_with_regex(log_message)
# #
# #     if label is None:
# #         return None
# #
# #     return label
# #
# #
# # # def classify_logs(logs):
# # #     labels = []
# # #     for source, log_msg in logs:
# # #         label = classify_log(source, log_msg)
# # #         labels.append(label)
# # #     return labels
# # #
# # #
# # # def classify_log(source, log_message):
# # #     # 1. If source is LegacyCRM → handled separately (your comment said LLM)
# # #     if source == "LegacyCRM":
# # #         # Placeholder: implement LLM logic or fallback later
# # #         return "LegacyCRM_Log"
# # #
# # #     # 2. Try regex classification first (cheap + fast)
# # #     label = classify_with_regex(log_message)
# # #
# # #     # 3. If regex fails → fallback to ML/BERT model
# # #     if label is None:
# # #         # Placeholder: replace with your ML/BERT model
# # #         # Example:
# # #         # label = bert_model.predict([log_message])[0]
# # #         return "ML_Predicted_Label"
# # #
# # #     return label
# #
# #
# #
# # if __name__ == "__main__":
# #     logs = [
# #         "User User123 logged in.",
# #         "Backup started at 12:00.",
# #         "Backup completed successfully.",
# #         "System updated to version 1.0.0.",
# #         "File file1.txt uploaded successfully by user user1.",
# #         "Ladle!! nhi ho paya",
# #     ]
# #
# #     for log in logs:
# #         print(classify_with_regex(log))
# #
# #
# #
# from processor_regex import classify_with_regex
# from processor_bert import classify_with_bert
# # from processor_llm import classify_with_llm
#
# def classify(logs):
#     labels = []
#     for source, log_msg in logs:
#         label = classify_log(source, log_msg)
#         labels.append(label)
#     return labels
#
#
# def classify_log(source, log_msg):
#     if source == "LegacyCRM":
#         label = classify_with_llm(log_msg)
#     else:
#         label = classify_with_regex(log_msg)
#         if not label:
#             label = classify_with_bert(log_msg)
#     return label
#
# def classify_csv(input_file):
#     import pandas as pd
#     df = pd.read_csv(input_file)
#
#     # Perform classification
#     df["target_label"] = classify(list(zip(df["source"], df["log_message"])))
#
#     # Save the modified file
#     output_file = "output.csv"
#     df.to_csv(output_file, index=False)
#
#     return output_file
#
# if __name__ == '__main__':
#     classify_csv("test.csv")
#     logs = [
#         ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
#         ("BillingSystem", "User 12345 logged in."),
#         ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
#         ("AnalyticsEngine", "Backup completed successfully."),
#         ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
#         ("ModernHR", "Admin access escalation detected for user 9429"),
#         ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
#         ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
#         ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
#         ("LegacyCRM", " The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025")
#     ]
#     labels = classify(logs)
#
#     for log, label in zip(logs, labels):
#         print(log[0], "->", label)

from processor_regex import classify_with_regex
from processor_bert import classify_with_bert


def classify(logs):
    labels = []
    for source, log_msg in logs:
        labels.append(classify_log(source, log_msg))
    return labels


def classify_log(source, log_msg):
    # Regex first
    label = classify_with_regex(log_msg)

    # If regex fails → fallback to BERT
    if not label:
        label = classify_with_bert(log_msg)

    return label


def classify_csv(input_file):
    import pandas as pd
    df = pd.read_csv(input_file)

    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

    output_file = "output.csv"
    df.to_csv(output_file, index=False)
    return output_file


if __name__ == '__main__':
    # Correct CSV path
    classify_csv("resources/test.csv")

    logs = [
        ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
        ("BillingSystem", "User 12345 logged in."),
        ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
        ("AnalyticsEngine", "Backup completed successfully."),
        ("ModernHR", "GET /v2/..."),
        ("ModernHR", "Admin access escalation detected for user 9429"),
        ("LegacyCRM", "Case escalation for ticket ID 7324 failed because agent inactive."),
        ("LegacyCRM", "Invoice generation aborted for order ID 8910 due to tax module error."),
        ("LegacyCRM", "Feature 'BulkEmailSender' is deprecated."),
        ("LegacyCRM", "ReportGenerator module to be retired in version 4.0.")
    ]

    labels = classify(logs)

    for log, label in zip(logs, labels):
        print(log[0], "->", label)
