import pandas as pd
import tldextract
from typing import Optional, Dict
from urllib.parse import urlparse
from nltk.tokenize import RegexpTokenizer
import regex as re


def parse_url(url: str) -> Optional[Dict[str, str]]:
    try:
        no_scheme = not re.compile(r'^https?://').match(url)
        if no_scheme:
            parsed_url = urlparse(f"http://{url}")
            return {
                "scheme": None,  # not established a value for this
                "netloc": parsed_url.netloc,
                "path": parsed_url.path,
                "params": parsed_url.params,
                "query": parsed_url.query,
                "fragment": parsed_url.fragment,
            }
        else:
            parsed_url = urlparse(url)
            return {
                "scheme": parsed_url.scheme,
                "netloc": parsed_url.netloc,
                "path": parsed_url.path,
                "params": parsed_url.params,
                "query": parsed_url.query,
                "fragment": parsed_url.fragment,
            }
    except:
        return None


def get_num_subdomains(netloc: str) -> int:
    return netloc.count('.') + 1 if '.' in netloc else 0


def tokenize_domain(netloc: str) -> str:
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    split_domain = tldextract.extract(netloc)
    no_tld = f"{split_domain.subdomain}.{split_domain.domain}"
    tokens = [token for token in tokenizer.tokenize(no_tld) if len(token) > 1]
    return " ".join(tokens)


def process_url(url):
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    parsed_url = parse_url(url)
    length = len(url)
    tld = tldextract.extract(str(parsed_url['netloc'])).suffix
    tld = tld if tld else 'None'
    is_ip = bool(re.match(r"\d+\.\d+\.\d+\.\d+", parsed_url['netloc']))
    domain_hyphens = parsed_url['netloc'].count('-')
    domain_underscores = parsed_url['netloc'].count('_')
    path_hyphens = parsed_url['path'].count('-')
    path_underscores = parsed_url['path'].count('_')
    slashes = parsed_url['path'].count('/')
    full_stops = parsed_url['path'].count('.')
    num_subdomains = get_num_subdomains(parsed_url['netloc'])
    domain_tokens = tokenize_domain(parsed_url['netloc'])
    path_tokens = " ".join(tokenizer.tokenize(
        str(parsed_url['path']))) if parsed_url['path'] else ''

    return {"length": length,
            "tld": tld,
            "is_ip": is_ip,
            "domain_hyphens": domain_hyphens,
            "domain_underscores": domain_underscores,
            "path_hyphens": path_hyphens,
            "path_underscores": path_underscores,
            "slashes": slashes,
            "full_stops": full_stops,
            "num_subdomains": num_subdomains,
            "domain_tokens": domain_tokens,
            "path_tokens": path_tokens}


def process_file(csv_file):
    url_data = pd.read_csv(csv_file, nrows=1000)

    # Parse URLs
    url_data["parsed_url"] = url_data["x"].apply(parse_url)

    # Expand parsed_url dict into separate columns
    url_data = pd.concat([url_data.drop(['parsed_url'], axis=1),
                         url_data['parsed_url'].apply(pd.Series)], axis=1)

    # Extract features
    url_data[["length",
              "tld",
              "is_ip",
              "domain_hyphens",
              "domain_underscores",
              "path_hyphens",
              "path_underscores",
              "slashes",
              "full_stops",
              "num_subdomains",
              "domain_tokens",
              "path_tokens"]] = url_data["x"].apply(process_url).apply(pd.Series)

    url_data = url_data.drop(['scheme', 'netloc', 'path',
                              'params', 'query', 'fragment'], axis=1)
    url_data = url_data.dropna()
    # url_data_y = url_data.iloc[:,1].map({'bad' : 1, 'good' : 0})
    url_data_y = url_data['y']
    url_data = url_data.drop(url_data.columns[[0, 1, 2]], axis=1)

    return url_data, url_data_y
