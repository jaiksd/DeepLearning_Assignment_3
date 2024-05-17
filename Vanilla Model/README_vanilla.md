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


## Dataset
- We use [Aksharantar dataset](https://drive.google.com/uc?export=download&id=1tGIO4-IPNtxJ6RQMmykvAfY_B0AaLY5A) dataset for our experiments.
## Wandb Report Link: 
[Report wandb](https://wandb.ai/cs23m030/Assignment_3_DL/reports/CS6910-Assignment-3--Vmlldzo3OTU3MzY4)
## Vanilla Seq2Seq:
### Following are the hyperparameters:
- **Usage** 
```
parser.add_argument('-wp' , '--wandb_project', help='Project name used to track experiments in Weights & Biases dashboard' , type=str, default='Assignment_3_DL_test')
parser.add_argument('-we', '--wandb_entity' , help='Wandb Entity used to track experiments in the Weights & Biases dashboard.' , type=str, default='cs22s030')
parser.add_argument('-ct', '--cell_type', help="Choices:['rnn','gru','lstm']", type=str, default='gru')
parser.add_argument('-b', '--batch_size', help="Batch size used to train neural network.", type=int, default=128)
parser.add_argument('-o', '--optim', help = 'choices: [ "adam", "nadam"]', type=str, default = 'adam')
parser.add_argument('-lr', '--learning_rate', help = 'Learning rate used to optimize model parameters', type=float, default=0.0002)
parser.add_argument('-em', '--embedding_size', help='size of embedding', type=int, default=512)
parser.add_argument('-hs', '--hidden_size', help='choices:[64,128,256,512]',type=int, default=512)
parser.add_argument('-dp', '--dropout', help='choices:[0,0.2,0.3]',type=float, default=0.1)
parser.add_argument('-nl', '--num_layers', help='Number of layers in network ',type=int, default=3)
parser.add_argument('-bidir', '--bidirectional', help='Choices:["True","False"]',type=bool, default=False)
parser.add_argument('-tf', '--teacher_forcing', help='choices:[0,0.2,0.3,0.5,0.7]',type=float, default=0.7)

```
 - To run train_a.py :
 - Note add '!' before any command only if you are running in colab or kaggle , else no need to add '!' before any command to run in command line
    - first Load dataset using :
     ```
     !wget 'https://drive.google.com/uc?export=download&id=1tGIO4-IPNtxJ6RQMmykvAfY_B0AaLY5A' -O data.zip && unzip -q data.zip

     ```
- This will run code for some default parameters. To generate the best result refer the below configuration:
- To run the code with default parameters
 ```
 !python train_a.py

 ```
-To run the code with custom parameters
```
!python train_vanilla.py -wp Assignment_3_DL_test -we cs22s030 -ct gru -b 128 -o adam -lr 0.0002 -em 512 -hs 512 -dp 0.1 -nl 3 -bidir False -tf 0.7
```
 
## Author
[Jai Kishan Dewangan]([https://github.com/Shreyash007](https://github.com/jaiksd/DeepLearning_Assignment_3))
CS23M030
 
