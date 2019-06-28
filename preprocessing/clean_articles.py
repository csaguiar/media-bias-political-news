from nltk.tokenize import RegexpTokenizer
import re

TOKENIZER = RegexpTokenizer(r'\w+')


# Function to expand contractions
def expand_contractions(content, contractions_dict):
    for original, replacement in contractions_dict.items():
        content = content.replace(original, replacement)

    return content


# Function with rules for each especific domain
def clean_by_domain(content, domain):
    if domain == "reuters.com":
        content = re.sub(r"^(.*?) - ", "", content)

    if domain == "cnn.com":
        content = content.replace("(CNN)", "")

    if domain == "foxnews.com":
        content = re.sub(r"\n(.*?) contributed to this report.", "", content)
        content = content.replace("CLICK HERE TO GET THE FOX NEWS APP", "")

    if domain == "slate.com":
        content = content.replace("Get The Angle in Your Inbox Slate's daily newsletter rounds up the stories you need to read. We encountered an issue signing you up. Please try again. Please enable javascript to use form. Email address: Thanks for signing up! You can manage your newsletter subscriptions at any time.", "")

    if domain == "bbc.com":
        content = content.replace("Image copyright Reuters Image caption", "")
        content = content.replace("Related Topics", "")

    return content


def clean_general_rules(content):
    response = content.replace("U.S.", "United States")
    response = content.replace("U.S", "United States")
    response = content.replace("Associated Press", "")

    return response


# Function to clean a text based on the article entry
def clean_text(row, contractions_dict):
    content = row["content"]
    domain = row["domain"]
    # Especific cleaning by domain
    content = clean_by_domain(content, domain)

    # General rules
    content = clean_general_rules(content)

    # lowercase
    content = content.lower()

    # Expand contractions
    content = expand_contractions(content, contractions_dict)

    return ' '.join(TOKENIZER.tokenize(content))


def clean_dataset(dataset, contractions_dict):
    dataset["content"] = dataset.apply(lambda row: clean_text(row, contractions_dict), axis=1)

    return dataset
