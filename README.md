# Boolean model of information retrieval
 This program will interpret documents, index the words into a dictionary and finally, it will be possible to search through docs with boolean method

## Documents Interpreting
In the first part of `main.py` the code will use the `GetDocText.py` module to read all the available docs and then index it. After reading the text, below tasks are operated on them:
- splitting and tokenizing the words from the text
- preprocess token (lower case + punctuations removal + excluding dirty tokens)
- indexing tokens into the dictionary (docID + tokenPosision + frequency)
## Loging activity
On each program run, a full log will be saved in `./log` with the name of `[Date + Time]` which contains below information:
- available documents
- dictionary data
- entered query and results
## Searching for query
The program will ask you to enter your desired query, which can contains up to 3 word and 2 operator
> for example: `that WITH he WITH is` is an acceptable query
allowed operator are:
- AND
- OR
- WITH
- NEAR #
which can place within the the query tokens
Finally, all possible answers (related documnets) will be shown

> ## `CreateText.py`
> This is an option provided in case you don't have access to documents to interpret or want to try some new documents. This script will find requested topic in Wikipedia and put it as a plain text document in `docs/` directory