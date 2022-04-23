# Related work
Let's look at related work: punctuation and capitalization for ASR.
Nvidia models:
* https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/punctuationcapitalization_en_us_bert_base
* https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/punctuation_en_bert
* https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/punctuation_en_distilbert

Which were trained on Tatoeba, Books from the Project Gutenberg, and Transcripts from Fisher English Training Speech corpora.

# Datasets
### Tatoeba sentences
https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2
https://storage.yandexcloud.net/jbos/eng_sentences.tsv.bz2

### Books from the Project Gutenberg that were used as part of the LibriSpeech corpus
* https://www.openslr.org/resources/12/original-books.tar.gz
* https://storage.yandexcloud.net/jbos/original-books.tar.gz

Processed: https://storage.yandexcloud.net/jbos/gutenberg.tsv.gz

### Transcripts from Fisher English Training Speech
Pay-walled

### OSS Docs
* https://github.com/JetBrains/intellij-sdk-docs/archive/d0a992512fb3f7036fddad1a4ba815458baf7d19.zip
* https://github.com/JetBrains/kotlin-web-site/archive/589636c4bb9bfdc8bd87ab9f150f6c22d809e598.zip
* https://github.com/microsoft/vscode-docs/archive/a03ef83075081dda33db75352b4527387cec2d27.zip
* https://github.com/microsoft/TypeScript-Website/archive/a76e4f2f3beb6dcfba85e1b9378567e7b666983a.zip

Processed: https://storage.yandexcloud.net/jbos/oss.tsv.gz

### Twitter
https://www.kaggle.com/datasets/ayhmrba/elon-musk-tweets-2010-2021
https://storage.yandexcloud.net/jbos/archive.zip

### Email
https://storage.googleapis.com/kaggle-data-sets/55/120/compressed/emails.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20220417%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220417T101822Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=9a2e974f7eae3644a79ce5c597d05332fb2f2af4bf0987dfd299a3617436a170da72fce451123a09b42aa6d1bc6e109f19f318b9ef148d2f04f090aff57aadcc94587bcb89e10543939eefba6a9cab8bb88c332a4ebd415ca386e525456c000076cc0d619dc371fa14731589631a37758606866a08615cb509bd48ff614b6c50e2c641b454a2e607fd4dada1fc5f74d7c483d8bdaa6adcf8ea7df8805340676c6b61b714c7f67db72fbf5db909ac3ca2c4760eab920a59bb7c387b93a8f1a7d6e24bbf7f2f80943d9b5b176afb77f8bb628eb95d4793ee52aeab9dd2510d68fc8e6540bb9e66fd75ce9ef3f6a5c791057b737fd701a6ac4922982ac72f2b6789
https://storage.yandexcloud.net/jbos/emails.csv.zip

### Wikipedia
```
from datasets import load_dataset
wiki = load_dataset("wikipedia", "20220301.en")
```