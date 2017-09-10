# bibtex2arxivSanity

Take advantage of Arxiv Sanity's awesome paper recommendations.

- Loads a BibTex file and extracts paper titles
- Logs in to your Arxiv Sanity account
- Searches for each BibTex paper title on Arxiv Sanity
- Saves the paper title on Arxiv Sanity that has the minimum Levenshtein distance between the BibTex title. If the minimum distance is greater than 10, nothing is saved.

## Requirements

PhantomJS and requirements.txt:

```
bibtexparser==0.6.2
editdistance==0.3.1
selenium==3.5.0
```

## Usage

```
python main.py --help
usage: main.py [-h] bibtex_file username password

Save articles in a BibTex file on your Arxiv Sanity account

positional arguments:
  bibtex_file  Path to BibTex file
  username     Your Arxiv Sanity username
  password     Your Arxiv Sanity password

optional arguments:
  -h, --help   show this help message and exit
```