# CS6910-Assignment3
## Problem Statement
Use recurrent neural networks to build a transliteration system, using pytorch.

## Prerequisites

```
python 3.9
numpy 1.21.5
pytorch
wget
```
 - Clone/download  this repository
 - I have conducted all my experiments in Google Collab, for running in google colab, install wandb and wget(for importing dataset) using following command 
 - Enable GPU on colab for faster training
 
  ``` 
  !pip install wandb 
  !pip install wget
  ```
 - For running locally, install wandb and other required libraries using following command  
  ``` 
  pip install wandb
  pip install numpy
  pip install pytorch
  ```




# CS6910_Assignment_3

## Wandb Report Link: 
[Report wandb](https://wandb.ai/cs23m030/Assignment_3_DL/reports/CS6910-Assignment-3--Vmlldzo3OTU3MzY4)
## Vanilla Seq2Seq:
### To run the code:
- **Usage** 
```
usage: Dl3_Vanilla_Seq2Seq.py
       [-h]
       [-wp WANDB_PROJECT]
       [-we WANDB_ENTITY]
       [-ct CELL_TYPE]
       [-b BATCH_SIZE]
       [-o OPTIMIZER]
       [-lr LEARNING_RATE]
       [-em EMBEDDING_SIZE]
       [-hs HIDDEN_SIZE]
       [-dp DROPOUT]
       [-nl NUM_LAYERS]
       [-bidir BIDIRECTIONAL]
       [-tf TEACHER_FORCING]

```
 - To run code in cloab :
    - first Load dataset using :
     ```
     !wget 'https://drive.google.com/uc?export=download&id=1uRKU4as2NlS9i8sdLRS1e326vQRdhvfw' -O dataset.zip && unzip -q dataset.zip

     ```
     - After loading the dataset and mounting the .py file in colab run:
      ```
      !python3 "/content/drive/My Drive/Colab Notebooks/Dl3_Vanilla_Seq2Seq.py"
      ```
- This will run code for some default parameters. To generate the best result refer the below configuration:
 ```
 sweep_config= {
    'parameters' : {
        'cell_type' : { 'values' : ['gru'] },
        'dropout' : { 'values' : [0.1]},
        'embedding_size' : {'values' : [512]},
        'num_layers' : {'values' : [3]},
        'batch_size' : {'values' : [128]},
        'hidden_size' : {'values' : [512]},
        'bidirectional' : {'values' : [False]},
        'learning_rate':{"values": [0.0002]},
        'optim':{"values": ['adam']},
       'teacher_forcing':{"values":[0.7]}
    }
}

 ```
 
 ## Attention Seq2Seq:
### To run the code:
- **Usage** 
```
usage: Dl3_Attn_Seq2Seq.py
       [-h]
       [-wp WANDB_PROJECT]
       [-we WANDB_ENTITY]
       [-ct CELL_TYPE]
       [-b BATCH_SIZE]
       [-o OPTIMIZER]
       [-lr LEARNING_RATE]
       [-em EMBEDDING_SIZE]
       [-hs HIDDEN_SIZE]
       [-dp DROPOUT]
       [-nl NUM_LAYERS]
       [-bidir BIDIRECTIONAL]
       [-tf TEACHER_FORCING]

```
 - To run code in cloab :
    - first Load dataset using :
     ```
     !wget 'https://drive.google.com/uc?export=download&id=1uRKU4as2NlS9i8sdLRS1e326vQRdhvfw' -O dataset.zip && unzip -q dataset.zip

     ```
     - After loading the dataset and mounting the .py file in colab run:
      ```
      !python3 "/content/drive/My Drive/Colab Notebooks/Dl3_Attn_Seq2Seq.py" 
      ```
- This will run code for some default parameters. To generate the best result refer the below configuration:
```
sweep_config= {
    'parameters' : {
        'cell_type' : { 'values' : ['lstm'] },
        'dropout' : { 'values' : [0.2]},
        'embedding_size' : {'values' : [256]},
        'num_layers' : {'values' : [1]},
        'batch_size' : {'values' : [32]},
        'hidden_size' : {'values' : [512]},
        'bidirectional' : {'values' : [False]},
        'learning_rate':{"values": [0.001]},
        'optim':{"values": ['nadam']},
       'teacher_forcing':{"values":[0.1]}
    }
}

``` 
 
