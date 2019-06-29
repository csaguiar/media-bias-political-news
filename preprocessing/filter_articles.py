import re


CONSERVATIVE = {
    "reason.com": {
        "name": "Reason",
        "level": 1
    },
    "washingtontimes.com": {
        "name": "The Washington Times",
        "level": 1
    },
    "nationareview.com": {
        "name": "National Review",
        "level": 2
    },
    "washingtonexaminer.com": {
        "name": "Washington Examiner",
        "level": 1
    },
    "thefederalist.com": {
        "name": "The Federalist",
        "level": 2
    },
    "foxnews.com": {
        "name": "Fox News",
        "level": 2
    },
    "nypost.com": {
        "name": "New York Post",
        "level": 2
    },
    "theblaze.com": {
        "name": "The Blaze",
        "level": 2
    },
    "dailycaller.com": {
        "name": "The Daily Caller",
        "level": 2
    },
    "dailywire.com": {
        "name": "The Daily Wire",
        "level": 2
    },
    "spectator.org": {
        "name": "Spectator",
        "level": 2
    }
}

LIBERAL = {
    "newyorker.com": {
        "name": "The New Yorker",
        "level": 2
    },
    "motherjones.com": {
        "name": "Mother Jones",
        "level": 2
    },
    "slate.com": {
        "name": "Slate",
        "level": 2
    },
    "msnbc.com": {
        "name": "MSNBC",
        "level": 2
    },
    "cnn.com": {
        "name": "CNN",
        "level": 2
    },
    "washingtonpost.com": {
        "name": "The Washington Post",
        "level": 1
    },
    "theguardian.com": {
        "name": "The Guardian",
        "level": 1
    },
    "nytimes.com": {
        "name": "The New York Times",
        "level": 1
    },
    "theatlantic.com": {
        "name": "The Atlantic",
        "level": 1
    },
    "nbcnews.com": {
        "name": "NBC News",
        "level": 1
    }
}


CENTRAL = {
    "reuters.com": {
        "name": "Reuters",
        "level": 0
    },
    "csmonitor.com": {
        "name": "The Christian Science Monitor",
        "level": 0
    },
    "fivethirtyeight.com": {
        "name": "FiveThirtyEight",
        "level": 0
    },
    "bbc.com": {
        "name": "BBC News",
        "level": 0
    },
    "forbes.com": {
        "name": "Forbes",
        "level": 0
    }
}

ALL_SOURCES = {**CENTRAL, **LIBERAL, **CONSERVATIVE}
SELECTED_DOMAINS = ALL_SOURCES.keys()

DOMAINS_TO_BE_REMOVED = [
    "radio.foxnews.com",
    "video.foxnews.com",
    "money.cnn.com",
    "s2.washingtonpost.com",
    "video.newyorker.com",
    "jobs.washingtonpost.com",
    "live.washingtonpost.com",
    "feeds.foxnews.com"
]


def mask_string(dataset):
    return dataset["content"].apply(lambda x: isinstance(x, str))


def mask_content_size(dataset, size_threshold=300):
    return dataset["content"].apply(len) > size_threshold


def clean_publication_name(publication):
    # Leaving only the domain
    return re.sub(r"(https?://)?(www([0-9])?\.)?", "", publication)


def create_domain(dataset):
    dataset["domain"] = dataset["publication"].apply(clean_publication_name)
    return dataset


def filter_by_content_size(dataset):
    is_string = mask_string(dataset)
    dataset = dataset[is_string]
    enough_content = mask_content_size(dataset)
    return dataset[enough_content]

def filter_by_domain(dataset):
    # # Filter to keep entries where the domain is valid
    def keep_by_domain(domain):
        check = [(c in domain and domain not in DOMAINS_TO_BE_REMOVED) for c in SELECTED_DOMAINS]
        return max(check)

    mask_domain = dataset["domain"].apply(keep_by_domain)

    return dataset[mask_domain]


def filter_by_content(dataset):
    # Filter to keep texts that doesn't contain texts that reference them as
    # a non-relevant article
    contains_text_to_be_removed = ["cnn sport", "cnn business"]

    def keep_by_text(text):
        check = [(check in text.lower()) for check in contains_text_to_be_removed]
        return not max(check)

    mask_text = dataset["content"].apply(keep_by_text)

    return dataset[mask_text]


def filter_by_url(dataset):
    url_pattern_to_be_removed = [
        "theguardian.com/music/",
        "theguardian.com/technology/"
    ]

    def keep_by_url(url):
        check = [(check in url) for check in url_pattern_to_be_removed]
        return not max(check)

    mask_url = dataset["url"].apply(keep_by_url)

    return dataset[mask_url]


def normalize_domains(dataset):
    def normalize(domain):
        response = domain
        for check in SELECTED_DOMAINS:
            if check in domain:
                response = check

        return response

    dataset["domain"] = dataset["domain"].apply(normalize)

    return dataset


def include_bias_side(dataset):
    liberal_list = LIBERAL.keys()
    conservative_list = CONSERVATIVE.keys()

    def bias_side(domain):
        if domain in liberal_list:
            response = 0
        elif domain in conservative_list:
            response = 1
        else:
            response = -1

        return response

    def bias_level(domain):
        domain_meta = ALL_SOURCES.get(domain, {})
        return domain_meta.get("level")

    dataset["label"] = dataset["domain"].apply(bias_side).astype(int)
    dataset["level"] = dataset["domain"].apply(bias_level).astype(int)

    return dataset


def filter(dataset):
    return (
        dataset.pipe(filter_by_content_size)
               .pipe(create_domain)
               .pipe(filter_by_domain)
               .pipe(filter_by_content)
               .pipe(filter_by_url)
               .pipe(normalize_domains)
               .pipe(include_bias_side)
    )
