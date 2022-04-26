# Demo
[ugramm.8052.ru](http://ugramm.8052.ru) | [Swagger API  Docs](http://ugramm.8052.ru/apidocs/)

![Screenshot](https://github.com/nazarov-yuriy/ugramm/raw/main/docs/img/demo.png)

# Deployment
### Run
```bash
cd service && docker-compose up
```

### Test & Build & Run
On Ubuntu 20.04
```bash
PREFIX=firefish  # update docker-compose.yml if changed
sudo apt install -y python3 python3-pip libmecab-dev
pip install flake8 pytest
pip install -r service/backend/requirements.txt
pytest
cd service
cd third_party && docker build -t "$PREFIX/languagetool:5.7.0" . && cd ..
cd backend && docker build -t "$PREFIX/ugramm:0.2" . && cd ..
docker-compose up
```
See tests at [service/backend/test](https://github.com/nazarov-yuriy/ugramm/tree/main/service/backend/test)


# Task
The task is to suggest where to place commas in a given text.

# Related work
* Grazie
* Grammarly
* LanguageTool | [Standalone version](https://forum.languagetool.org/t/is-the-standalone-version-of-languagetool-still-available-for-download/6537)
* NVIDIA NeMo | [Standalone version](https://catalog.ngc.nvidia.com/models?query=nemo&orderBy=weightPopularDESC)
* FullStop | [Standalone version](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large)

# Quality

### Data
There are a lot of domains when we are talking about text data:
* prose
* encyclopedia articles
* subtitles
* emails
* technical documentation
* instant messages
* ... etc.

All these domains have different properties.
And it's hard to develop a system which performs equally well on all of them.
Let's select 3 datasets which could be biased towards different domains:
* [Tatoeba](http://tatoeba.org/en/) - english texts from books/songs/etc. translated to Japanese
* [Project Gutenberg in LibriSpeech](https://paperswithcode.com/dataset/librispeech) - books
* Technical documentation for [JetBrains](https://github.com/JetBrains) and [Microsoft](https://github.com/microsoft) products

### Metrics
Punctuation quality could be measured in many ways:
* Accuracy
* Recall/Precision/F1
* ROC-AUC

On different scales:
* sub-word/token level
* word level
* sentence level

Let's use **word level F1-score** for all comparisons.

### Models
See model training in [quality/models](https://github.com/nazarov-yuriy/ugramm/tree/main/quality/models)

Graphs at [Weights & Biases](https://wandb.ai/firefish/huggingface/runs/d2fn8fhs)

### Systems performance
| Model \ Test set   | Tatoeba   | OSS Docs  | Gutenberg | Total     |
|--------------------|-----------|-----------|-----------|-----------|
| NeMo BERT          | 0.805     | 0.701     | 0.636     | 0.655     |
| FullStop           | 0.757     | 0.723     | 0.623     | 0.648     |
| Ours DistilRoBERTa | 0.846     | 0.824     | 0.826     | 0.827     |
| Ours RoBERTa       | **0.868** | **0.851** | **0.864** | **0.862** |

Table 1. Word level F1-scores

More details in notebooks: [quality/evaluation](https://github.com/nazarov-yuriy/ugramm/tree/main/quality/evaluation)
