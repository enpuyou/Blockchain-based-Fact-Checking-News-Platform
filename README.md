# blockchain-based-fact-checking-news-platform

The project here is a final project submitted for the cryptocurrency course. It
proposes a proof of concept for a decentralized news platform that integrates
third-party fact-checkers as well as crowdsourced community evaluations. Such a
platform relies on the community to evaluate and verify the authenticity of a
news article. With this approach, we hope that the news storage and evaluation process
would be secure yet not controlled by a single organization or entity;
it also encourages the community to get more involved in societal development
and informed on social issues.

The project has implemented a simple blockchain structure in Python. It covers
some of the core features of a typical blockchain, including transactions,
proof-of-work, mining, etc. It incorporated the Merkle tree structure into the
block for the storage of user-submitted evaluations. Essentially, each block
would contain articles/claims with evaluations/ratings coming from third-parties
([Google Fact Checking API](https://developers.google.com/fact-check/tools/api))
and users.

### Commands

The project uses `pipenv` to manage library dependencies. To install the
dependencies, please type the following command into the terminal:

```shell
pipenv install
```

After successfully installing the dependencies, `blockchain.py` can be executed
with the following command:

```shell
pipenv run python src/blockchain.py
```

The command would display a sample output containing the Merkle tree as well as the
constructed blocks in the form of a dictionary.

We have also attempted to implement a simple API for the `blockchain.py` with
[`FastAPI`](https://fastapi.tiangolo.com) in `main.py`. Due to the time constraint,
it is only a basic API that covers the functions like adding transactions and
mining. To execute and have a simple API framework running on the localhost, you
can type the following command into the terminal:

```shell
pipenv run uvicorn src.main:node --reload
```

You can also visit `http://127.0.0.1:8000/#docs` to see a visual representation
of the framework.

To run the test cases for the project, please type the following command:

```shell
pipenv run pytest tests
```

#### Sample Output

```shell
[{'hash': '0026d3b0417944aced50f4a54d778e3a84fd736792fe9afb1491be8108e29468',
  'index': 1,
  'news': {'mean': 3.5,
           'review': ['False',
                      'False',
                      'Pants on Fire',
                      'False',
                      'Lacks Context',
                      'Out of Context',
                      'False',
                      'False',
                      'No Evidence',
                      'Distorts the Facts'],
           'stdev': 1.8708286933869707,
           'value': 'coronavirus is a hoax',
           'variance': 3.5},
  'nonce': 229,
  'previous_hash': '008f6bcb16941fe8e92280815931b780efd9b178bf082f4cf7177bf8e5310091',
  'timestamp': '2021-02-12 04:02:17.933808',
  'transactions': 'ecc3e0e80e48af9c78cec2a446399b2a98ecda6dbf7ef6446cfbf3730feff804'},
 {'hash': '00f7d7932f8f12af37de848c06e890f50b3fcfc437ce8f080dbabf24c52a1e31',
  'index': 2,
  'news': {'mean': 8.5,
           'review': ['The Pfizer vaccine has an efficacy rate of over 90%. '
                      'The 99.96% figure is not an efficacy rate but the '
                      'proportion of people vaccinated in Israel who did not '
                      'later test positive for the virus.',
                      'Mostly true'],
           'stdev': 3.605551275463989,
           'value': 'vaccine is good',
           'variance': 13.0},
  'nonce': 578,
  'previous_hash': '0026d3b0417944aced50f4a54d778e3a84fd736792fe9afb1491be8108e29468',
  'timestamp': '2021-02-12 04:02:18.517646',
  'transactions': 'd165578d6b1b487d31e7029de4140f4c6144f2fb13026f3d7d277eccb7248ddb'}]
```
