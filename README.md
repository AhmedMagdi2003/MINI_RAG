# Mini Rag 
In this project we will get out of notebook, to make production with machin learning and deep learning 
by building well instructued project with clean code and fastapi for deployment.

## Requirements
1) python 3.8 or later (recommended 3.8)
2) mini condo download from here [mini_condo](https://www.anaconda.com/docs/getting-started/miniconda/install)
3) setup the enviroment
```bash
$ conda create -n mini-rag python=3.8
```
### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```
## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.