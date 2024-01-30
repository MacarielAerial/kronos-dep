# Kronos

## Code Examples

1. Download Timetable Data as a CSV
```sh
poetry run python -m kronos.pipelines.download_df_timetable -psj credentials/kronos-408821-b353d5af55b8.json -pdt data/01_raw/df_timetable.csv
```

2. Save NER Annotation Input as a TXT
```sh
poetry run python -m kronos.pipelines.save_ner_annotation_input -pdt data/01_raw/df_timetable.csv -pnai data/01_raw/ner_annotation_input.txt
```

3. Use NER Annotator to annotate timetable cell data https://tecoholic.github.io/ner-annotator/

4. Split full NER annotation data into train and dev sets
```sh
poetry run python -m kronos.pipelines.split_ner_annotations -pna ./data/01_raw/annotations.json -pta ./data/01_raw/train_annotations.json -pda ./data/01_raw/dev_annotations.json
```

5. Parse JSON formatted annotations into DocBin formatted annotations

```sh
poetry run python -m kronos.pipelines.convert_jsons_to_docbins -ptj ./data/01_raw/train_annotations.json -pdj ./data/01_raw/dev_annotations.json -ptd ./data/02_intermediate/train_annotations.spacy -pdd ./data/02_intermediate/dev_annotations.spacy
```

6. Populate basic NER training configuration file with default values

```sh
poetry run python -m spacy init fill-config ./src/kronos/conf_default/base_config.cfg ./data/02_intermediate/config.cfg
```

7. Train a customer NER component in a spacy pipeline

```sh
poetry run python -m spacy train ./data/02_intermediate/config.cfg --output ./data/03_primary/ --paths.train ./data/02_intermediate/train_annotations.spacy --paths.dev ./data/02_intermediate/dev_annotations.spacy
```

8. Parse a mixed node type layout networkx graph from timetable dataframe

```sh
poetry run python -m kronos.pipelines.df_to_mixed_layout_nx_g -pdt data/01_raw/df_timetable.csv -pmlng data/03_primary/mixed_layout_nx_g.json
```

## Notes

### Example config.cfg for Spacy NER Training
```
[paths]
train = null
dev = null
# Swap in local path to downloaded spacy pipeline
vectors = "./local_dependencies/en_core_web_lg-3.7.1/en_core_web_lg/en_core_web_lg-3.7.1"
init_tok2vec = null

[system]
gpu_allocator = null
seed = 0

[nlp]
lang = "en"
pipeline = ["tok2vec","ner"]
batch_size = 1000
disabled = []
before_creation = null
after_creation = null
after_pipeline_creation = null
tokenizer = {"@tokenizers":"spacy.Tokenizer.v1"}
vectors = {"@vectors":"spacy.Vectors.v1"}

[components]

[components.ner]
factory = "ner"
incorrect_spans_key = null
moves = null
scorer = {"@scorers":"spacy.ner_scorer.v1"}
update_with_oracle_cut_size = 100

[components.ner.model]
@architectures = "spacy.TransitionBasedParser.v2"
state_type = "ner"
extra_state_tokens = false
hidden_width = 64
maxout_pieces = 2
use_upper = true
nO = null

[components.ner.model.tok2vec]
@architectures = "spacy.Tok2VecListener.v1"
width = ${components.tok2vec.model.encode.width}
upstream = "*"

[components.tok2vec]
factory = "tok2vec"

[components.tok2vec.model]
@architectures = "spacy.Tok2Vec.v2"

[components.tok2vec.model.embed]
@architectures = "spacy.MultiHashEmbed.v2"
width = ${components.tok2vec.model.encode.width}
attrs = ["NORM","PREFIX","SUFFIX","SHAPE"]
rows = [5000,1000,2500,2500]
include_static_vectors = true

[components.tok2vec.model.encode]
@architectures = "spacy.MaxoutWindowEncoder.v2"
width = 256
depth = 8
window_size = 1
maxout_pieces = 3

[corpora]

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = ${paths.dev}
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[corpora.train]
@readers = "spacy.Corpus.v1"
path = ${paths.train}
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[training]
dev_corpus = "corpora.dev"
train_corpus = "corpora.train"
seed = ${system.seed}
gpu_allocator = ${system.gpu_allocator}
# Increase dropout to reduce overfitting
dropout = 0.3
accumulate_gradient = 1
# Earlier stopping because less data tends to result in faster overfitting
patience = 1000
max_epochs = 0
max_steps = 20000
eval_frequency = 200
frozen_components = []
annotating_components = []
before_to_disk = null
before_update = null

[training.batcher]
@batchers = "spacy.batch_by_words.v1"
discard_oversize = false
tolerance = 0.2
get_length = null

[training.batcher.size]
@schedules = "compounding.v1"
start = 100
stop = 1000
compound = 1.001
t = 0.0

[training.logger]
@loggers = "spacy.ConsoleLogger.v1"
progress_bar = false

[training.optimizer]
@optimizers = "Adam.v1"
beta1 = 0.9
beta2 = 0.999
L2_is_weight_decay = true
L2 = 0.01
grad_clip = 1.0
use_averages = false
eps = 0.00000001
learn_rate = 0.001

[training.score_weights]
ents_f = 1.0
ents_p = 0.0
ents_r = 0.0
ents_per_type = null

[pretraining]

[initialize]
vectors = ${paths.vectors}
init_tok2vec = ${paths.init_tok2vec}
vocab_data = null
lookups = null
before_init = null
after_init = null

[initialize.components]

[initialize.tokenizer]
```
