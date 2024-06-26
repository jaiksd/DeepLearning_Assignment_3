# -*- coding: utf-8 -*-
"""train_vanilla.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17wnhyY56-k2pq0lDpwJRHeDOylEj6gvr
"""

# -*- coding: utf-8 -*-

import torch # Importing the PyTorch library
import torch.nn as nn # Importing the neural network module from PyTorch
# Checking if CUDA (GPU) is available, and setting the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# For generating random numbers: importing random
# For deep learning framework: importing torch
# For data manipulation and analysis: importing pandas as pd
# For displaying progress bars: importing tqdm
# For mathematical operations: importing math
# For building neural networks: importing torch.nn as nn
# For plotting graphs: importing matplotlib.pyplot as plt
# For optimization algorithms: importing torch.optim as optim
# For computer vision tasks: importing torchvision
# For numerical computations: importing numpy as np
# For handling file paths: importing pathlib
# For image transformations: importing torchvision.transforms as transforms
# For additional neural network functions: importing torch.nn.functional as F
# For interacting with the operating system: importing os
# For accessing standard datasets: importing torchvision.datasets as datasets

import wandb
import argparse
import random
import torch
from tqdm import tqdm
import pandas as pd
import math
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.optim as optim
import torchvision
import numpy as np
import pathlib
import torchvision.transforms as transforms
import torch.nn.functional as F
from torch import optim
import os
from torch import nn
import torchvision.datasets as datasets
from torch.utils.data import (
    DataLoader, random_split
)
from torchvision.datasets import ImageFolder

# Setting PYTHONHASHSEED environment variable to control hash randomization: setting os.environ["PYTHONHASHSEED"] to "1"
# Setting the random seed for Python: seeding random number generator with seed 1
# Setting the random seed for CUDA devices: seeding CUDA random number generator with seed 1
# Setting the random seed for all CUDA devices: seeding random number generators for all CUDA devices with seed 1
# Setting the random seed for numpy: seeding numpy random number generator with seed 1
# Setting the random seed for PyTorch: seeding PyTorch random number generator with seed 1
# Setting PyTorch to use deterministic algorithms for cuDNN: setting torch.backends.cudnn.deterministic to True
# Disabling cuDNN benchmark mode to ensure deterministic computation: setting torch.backends.cudnn.benchmark to False

os.environ["PYTHONHASHSEED"] = str(1)
random.seed(1)
torch.cuda.manual_seed(1)
torch.cuda.manual_seed_all(1)
np.random.seed(1)
torch.manual_seed(1)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


# For data manipulation and analysis
# For deep learning framework
# For building neural networks
# For data loading and handling
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

'''
The class Vocabulary is employed to generate Word_Vocab from the training dataset.
'''
class Word_Vocab:
    """
    Parameters:
      trg_lang (string): The name of the target language.
      src_lang (string): The name of the source language.
      file_path (string): The path to the CSV file containing the training dataset.

    Raises:
      ValueError: If the specified file_path does not exist.


    """
    def __init__(self, file_path, src_lang, trg_lang):
      # Class constructor to initialize the translation dataset
        # Parameters:
        #   - file_path: Path to the CSV file containing translations
        #   - src_lang: Source language column name in the CSV file
        #   - trg_lang: Target language column name in the CSV file
        # Read the CSV file into a Pandas DataFrame.
        # Read the CSV file into a Pandas DataFrame.
        def get_translations():
          return pd.read_csv(file_path, header=None, names=[src_lang, trg_lang])
        self.translations = get_translations()
        # It will drop any rows with missing values
        self.translations.dropna()
        def enumeration_across_trg():
           return {char: i+3 for i, char in enumerate(sorted(list(set(''.join(self.translations[trg_lang].tolist())))))}
        self.src_lang = src_lang
        def enumeration_across_src():
            return {char: i+3 for i, char in enumerate(sorted(list(set(''.join(self.translations[src_lang].tolist())))))}
        self.trg_lang = trg_lang
        # Create a dictionary that maps each character in the source language to an integer index.
        self.trg_vocab = enumeration_across_trg()
        # Create a dictionary that maps each character in the target language to an integer index.
        self.src_vocab = enumeration_across_src()

        def set_0():
          return 0
        # Add special tokens to the vocabularies.
        self.trg_vocab['<'] = set_0()
        self.src_vocab['<'] = set_0()
        def set_1():
            return 1
        def set_2():
            return 2
        self.trg_vocab['<unk>'] = set_2()
        self.src_vocab['<pad>'] = set_1()
        self.trg_vocab['<pad>'] = set_1()

        self.src_vocab['<unk>'] = set_2()

        # Extract the unique characters in the source and target languages
        src_chars = sorted(set(''.join(self.translations[src_lang])))
        trg_chars = sorted(set(''.join(self.translations[trg_lang])))

        def get_char_to_idx1():
          return {char: idx+3 for idx, char in enumerate(trg_chars)}
        # Assign an index to each character in the source and target languages
        self.t_char_to_idx = get_char_to_idx1()
        self.t_char_to_idx['<unk>']=2
        self.t_idx_to_char = {idx: char for char, idx in self.t_char_to_idx.items()}
        def get_char_to_idx2():
            return {char: idx+3 for idx, char in enumerate(src_chars)}
        self.s_char_to_idx = get_char_to_idx2()
        self.s_char_to_idx['<unk>']=2

        self.s_idx_to_char = {idx: char for char, idx in self.s_char_to_idx.items()}


    def utitlity_3(x,y):
        if(x>y):
          return 1
        else:
          return 0
    def ret_all_vocab(self):
           return self.src_vocab,self.trg_vocab,self.t_char_to_idx,self.t_idx_to_char,self.s_char_to_idx,self.s_idx_to_char
    def get(self):
         # This function returns the source and target vocabularies, as well as the dictionaries that map characters to integer indexes and vice versa.
        return self.ret_all_vocab()



class TransliterationDataset(Dataset):
    """
   Function Parameters:
    - src_lang (string): Specifies the source language from which translation originates.
    - trg_lang (string): Specifies the target language into which translation is done.
    - trg_vocab (Word_Vocab): Refers to the vocabulary tailored for the target language.
    - file_path (string): Indicates the precise location of the CSV file containing the training data.
    - src_vocab (Word_Vocab): Refers to the vocabulary customized for the source language.
    Raises:
     - ValueError: Raised if the provided file_path does not exist.

    """
    def __init__(self, file_path, src_lang, trg_lang,src_vocab,trg_vocab,t_char_to_idx):
        """
          Initializes the TransliterationDataset.

          Parameters:
              - file_path (string): Path to the CSV file containing translations.
              - src_lang (string): Source language column name in the CSV file.
              - trg_lang (string): Target language column name in the CSV file.
              - src_vocab (Word_Vocab): Vocabulary customized for the source language.
              - trg_vocab (Word_Vocab): Vocabulary tailored for the target language.
              - t_char_to_idx (dict): Dictionary mapping characters to integer indexes for target language.
          """
        self.src_lang = src_lang
        def set_reading_csv():
          return pd.read_csv(file_path, header=None, names=[src_lang, trg_lang])
        def set_max_scr_len():
          return max([len(word) for word in self.translations[src_lang].tolist()])+1
        self.translations = set_reading_csv()
        self.translations.dropna()
        def set_trg_len():
          return max([len(word) for word in self.translations[trg_lang].tolist()])+1
        self.t_char_to_idx = t_char_to_idx
        self.trg_lang = trg_lang
        self.trg_vocab = trg_vocab
        self.src_vocab = src_vocab
        self.max_src_len = set_max_scr_len()

        self.max_trg_len = set_trg_len()

    def __len__(self):
        return len(self.translations)

    def __getitem__(self, idx):
        def set_trans_trg():
            return self.translations.iloc[idx][self.trg_lang]

        src_word = self.translations.iloc[idx][self.src_lang]
        def trg_vocab():
          return [self.trg_vocab.get(char, self.src_vocab['<unk>']) for char in trg_word]
        trg_word = set_trans_trg()
        # Initialize the start-of-word token
        sow=0

        # Convert source and target words to lists of Word_Vocab indices
        src = [self.src_vocab.get(char, self.src_vocab['<unk>']) for char in src_word]
        trg = trg_vocab()
        # Insert the start-of-word token at the beginning
        trg.insert(0, sow)
        def ret_len_tar():
            return len(trg);

        src.insert(0, sow)
        def ret_src_len():
            return len(src)
        def trg_pad_set():
          return [self.trg_vocab['<pad>']] * (self.max_trg_len - trg_len)

        trg_len = ret_len_tar()
        src_len = ret_src_len()


        # Pad the source and target sequences with the <pad> token
        src_pad = [self.src_vocab['<pad>']] * (self.max_src_len - src_len)
        trg_pad = trg_pad_set()
        # Extend the source and target sequences with padding
        src.extend(src_pad)
        trg.extend(trg_pad)
        def ret_trg_len():
          return torch.LongTensor(trg)
        # Convert source and target sequences to tensors
        src = torch.LongTensor(src)
        trg = ret_trg_len()

        return src, trg, src_len, trg_len

def data_loading(bs):
    '''
    This function is designed to load data into batches, with the batch size being specified as an argument.
    '''
    # Define the paths for the train, validation, and test CSV files
    def get_test_data_path():
      return "/content/aksharantar_sampled/hin/hin_test.csv"
    def get_val_data_path():
      return "/content/aksharantar_sampled/hin/hin_valid.csv"
    def get_train_data_path():
      return "/content/aksharantar_sampled/hin/hin_train.csv"
    test_path  = get_test_data_path()
    val_path  = get_val_data_path()
    train_path  = get_train_data_path()
    vocab = Word_Vocab(train_path, 'src', 'trg')
    def set_data_p():
        return True
    src_vocab,trg_vocab,t_char_to_idx,t_idx_to_char,s_char_to_idx,s_idx_to_char=vocab.get()
    # Create data loaders
    test_loader = DataLoader(TransliterationDataset(test_path, 'src', 'trg',src_vocab,trg_vocab,t_char_to_idx), batch_size=bs, shuffle=False)
    val_loader =DataLoader(TransliterationDataset(val_path, 'src', 'trg',src_vocab,trg_vocab,t_char_to_idx), batch_size=bs, shuffle=False)
    train_loader = DataLoader(TransliterationDataset(train_path, 'src', 'trg',src_vocab,trg_vocab,t_char_to_idx), batch_size=bs, shuffle=True)
    set_data_p()
    return train_loader,test_loader,val_loader,t_idx_to_char,s_idx_to_char
train_loader,test_loader,val_loader,t_idx_to_char,s_idx_to_char=data_loading(32)

def string_indices(trg, t_idx_to_char):
    """
    This function processes batches of indices into strings with the assistance of the supplied index-to-character mapping.

    Parameters:
        t_idx_to_char (Dict): A dictionary associating indices with characters.
        trg (Tensor): Tensor data containing encoder words, structured as batch_size x sequence_length.

    """

    sq=trg.shape[1]
    bs=trg.shape[0]
    strings = []

    i=0
    while i<(bs):
        chars = []
        for j in range(sq):
            def get_char(t_idx_to_char,trg,i,j):
                return t_idx_to_char[trg[i,j].item()]
            if trg[i,j].item() in t_idx_to_char:
                char = get_char(t_idx_to_char,trg,i,j)
                chars.append(char)
        string = ''.join(chars)

        strings.append(string)
        i+=1
    return strings

# Model

class Encoder(nn.Module):
    def __init__(self, input_dim, embedded_size,hidden_dim, num_layers,bidirectional, cell_type,dp):
        """
        Initializes the Encoder module.

        Parameters:
            - input_dim (int): Dimensionality of the input data.
            - embedded_size (int): Dimensionality of the embedding space.
            - hidden_dim (int): Dimensionality of the hidden state.
            - num_layers (int): Number of recurrent layers.
            - bidirectional (bool): Specifies if the encoder is bidirectional.
            - cell_type (str): Type of recurrent cell ('rnn', 'lstm', or 'gru').
            - dp (float): Dropout probability.
        """
        super(Encoder, self).__init__()
        def utility_u1(x):
            return x>0
        self.bidirectional=bidirectional
        def set_hiddim():
          return hidden_dim
        self.input_dim = input_dim
        self.hidden_dim = set_hiddim()
        def set_emd():
            return embedded_size
        self.cell_type = cell_type
        self.embedded_size=set_emd()
        def set_drop():
          return nn.Dropout(dp)
        self.num_layers = num_layers



        self.dropout = set_drop()

        # Determine the directionality of the encoder (1 for unidirectional, 2 for bidirectional)
        def check_dir():
          if bidirectional:
            return 2
          else:
            return 1
        self.dir=check_dir()
        # Create an embedding layer
        self.embedding = nn.Embedding(input_dim,embedded_size)

        def set_lstm():
            return nn.LSTM(embedded_size, hidden_dim, num_layers, dropout=dp,bidirectional=bidirectional)
        def set_gru():
            return  nn.GRU(embedded_size, hidden_dim, num_layers, dropout=dp,bidirectional=bidirectional)
        def set_rnn():
            return nn.RNN(embedded_size, hidden_dim, num_layers, dropout=dp,bidirectional=bidirectional)
        # Create the recurrent layer based on the specified cell type
        if cell_type == 'rnn':
              self.rnn = set_rnn()
        elif cell_type == 'lstm':
              self.rnn = set_lstm()
        elif cell_type == 'gru':
              self.rnn = set_gru()
        else:
            raise ValueError("Invalid cell type. Choose 'rnn', 'lstm', or 'gru'.")

    def forward(self, src):
        embedded = self.dropout(self.embedding(src))
        if self.cell_type != 'lstm':
            output, hidden = self.rnn(embedded)
            return output,hidden
        else:
            output, (hidden, cell) = self.rnn(embedded)
            return output, (hidden, cell)


class Decoder(nn.Module):
    """
        Initializes the Decoder module.

        Parameters:
            - output_dim (int): Dimensionality of the output data.
            - embedded_size (int): Dimensionality of the embedding space.
            - hidden_dim (int): Dimensionality of the hidden state.
            - num_layers (int): Number of recurrent layers.
            - bidirectional (bool): Specifies if the decoder is bidirectional.
            - cell_type (str): Type of recurrent cell ('rnn', 'lstm', or 'gru').
            - dp (float): Dropout probability.
    """
    def __init__(self, output_dim,embedded_size, hidden_dim, num_layers,bidirectional,cell_type,dp):
        super(Decoder, self).__init__()
        def utility_u1(x):
            return x>0
        self.cell_type = cell_type
        def set_bidir():
            return nn.Dropout(dp)
        self.output_dim = output_dim
        self.num_layers = num_layers
        def set_hidden():
            return hidden_dim
        self.bidirectional=bidirectional
        def get_emd():
            return embedded_size
        self.dropout = set_bidir()
        self.embedded_size=embedded_size
        def check_bidir():
            if bidirectional:
              return 2
            else:
              return 1
        self.hidden_dim = set_hidden()
        self.dir=check_bidir()
        def set_lstm():
            return nn.LSTM(embedded_size, hidden_dim, num_layers,dropout=dp)
        def set_rnn():
            return nn.RNN(embedded_size, hidden_dim, num_layers,dropout=dp)
        def set_gru():
            return nn.GRU(embedded_size, hidden_dim, num_layers,dropout=dp)
        # Create an embedding layer
        self.embedding = nn.Embedding(output_dim,embedded_size)
        # Create the recurrent layer based on the specified cell type
        if cell_type == 'lstm':
            self.rnn = set_lstm()
        elif cell_type == 'rnn':
            self.rnn = set_rnn()
        elif cell_type == 'gru':
            self.rnn = set_gru()
        else:
            raise ValueError("Invalid cell type. Choose 'rnn', 'lstm', or 'gru'.")

        # Create the output fully connected layer
        self.fc_out = nn.Linear(hidden_dim, output_dim)

    def forward(self, input, hidden):
        embedded = self.dropout(self.embedding(input))
        output, hidden = self.rnn(embedded, hidden)
        def utility5(x,y):
          if x>y:
              return 1
          else :
              return 0
        output = self.fc_out(output)
        output = F.log_softmax(output, dim=1)
        return output, hidden

class Seq2Seq(nn.Module):
    """
        Initializes the Seq2Seq model.

        Parameters:
            - encoder (Encoder): The encoder module.
            - decoder (Decoder): The decoder module.
            - cell_type (str): Type of recurrent cell ('rnn', 'lstm', or 'gru').
            - bidirectional (bool): Specifies if the encoder is bidirectional.
    """
    def __init__(self, encoder, decoder,cell_type,bidirectional):
        super(Seq2Seq, self).__init__()
        def utility_u1(x):
            return x>0
        self.cell_type=cell_type
        def get_bidir():
            return bidirectional
        self.encoder = encoder
        self.bidirectional=get_bidir()
        def set_dec():
            return decoder
        self.decoder = set_dec()

    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        def get_bsize(a):
            return trg.shape[a]
        batch_size = get_bsize(1)
        #print(batch_size)
        max_len = get_bsize(0)
        #print(max_len)
        trg_vocab_size = self.decoder.output_dim
        outputs = torch.zeros(max_len, batch_size, trg_vocab_size).to(device)
        encoder_output, encoder_hidden = self.encoder(src)

        if self.bidirectional:
            if self.cell_type!='lstm':
                hidden_concat = torch.add(encoder_hidden[0:self.encoder.num_layers,:,:], encoder_hidden[self.encoder.num_layers:,:,:])/2
            else:
                hidden_concat = torch.add(encoder_hidden[0][0:self.encoder.num_layers,:,:], encoder_hidden[1][0:self.encoder.num_layers,:,:])/2
                cell_concat = torch.add(encoder_hidden[0][self.encoder.num_layers:,:,:], encoder_hidden[1][self.encoder.num_layers:,:,:])/2
                hidden_concat = (hidden_concat, cell_concat)

        else:
            hidden_concat= encoder_hidden

        decoder_hidden = hidden_concat
        # Initialize decoder input with the start token
        decoder_input = (trg[0,:]).unsqueeze(0)
        #print("decoder input shape",decoder_input.shape)
        t=1
        while t < trg.shape[0] :

            # Pass the decoder input and hidden state through the decoder
            decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden)
            def utility4(x,y):
                if x>y:
                    return 1
                else:
                    return 0
            # Store the decoder output in the outputs tensor
            def ret_dec_output():
                return decoder_output
            outputs[t] = ret_dec_output()
            max_pr, idx=torch.max(decoder_output,dim=2)
            def ret_trg():
                return trg.shape[1]
            idx=idx.view(ret_trg())
            if torch.rand(1) >= teacher_forcing_ratio:
                decoder_input= idx.unsqueeze(0)
            else:
                decoder_input= trg[t,:].unsqueeze(0)
            t+=1

        decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden)

        return outputs

def Word_Accuracy1(model,t_idx_to_char,data_loader, criterion):
    '''
    This function computes the word-level accuracy following each epoch of training.

    Parameters:
    model: The trained model instance.
    t_idx_to_char: A mapping from target indices to characters.
    data_loader: DataLoader object for the validation or test dataset.
    criterion: The loss criterion employed during model training.
    '''
    model.eval()
    def set_zero():
        return 0
    epoch_loss = set_zero()
    num_total = set_zero()
    num_correct = set_zero()
    with torch.no_grad():
        for batch_idx, (src, trg, src_len, trg_len) in enumerate(data_loader):
            # Convert target indices to string for comparison
            string_trg=string_indices(trg,t_idx_to_char)
            # Move tensors to the device
            def set_permute(var):
                return var.permute(1, 0)
            src = set_permute(src)
            src = src.to(device)
            def output_reshape(output):
                return output[1:].reshape(-1, output.shape[2])
            trg = set_permute(trg)
            trg = trg.to(device)
            # Perform forward pass through the model
            output = model(src, trg, 0)
            # turn off teacher forcing
            output = output_reshape(output)
            trg = trg[1:].reshape(-1) # exclude the start-of-sequence token

            # Calculate the loss
            output = output.to(device)
            def get_bs(trg_len):
                return trg_len.shape[0]
            loss = criterion(output, trg)
            epoch_loss += loss.item()

            batch_size = get_bs(trg_len)


            seq_length = int(trg.numel() / batch_size)

            def get_predicted_indices(seq_length,predicted_indices):
                return predicted_indices.reshape(seq_length,-1)

            # Convert the output to predicted characters
            predicted_indices = torch.argmax(output, dim=1)
            predicted_indices = get_predicted_indices(seq_length,predicted_indices)
            predicted_indices = predicted_indices.permute(1, 0)
            # Convert predicted indices to strings
            string_pred=string_indices(predicted_indices,t_idx_to_char)

            for i in range(batch_size):
                num_total+=1
                def getlen_str():
                    return string_pred[i][:len(string_trg[i])] == string_trg[i]
                # Compare the predicted string with the target string
                if getlen_str():
                    num_correct+=1

    print("Total",num_total)
    def cal_acc(num_correct,num_total):
        return ((num_correct) /num_total) * 100
    print("Correct",num_correct)

    return cal_acc(num_correct,num_total), (epoch_loss/(len(data_loader)))

def Word_Accuracy2(model,t_idx_to_char,s_idx_to_char,data_loader, criterion):
    '''
    This function is used for the test data
    Parameters:
    model: Trained model object.
    t_idx_to_char: Index-to-character mapping for the target language.
    s_idx_to_char: Index-to-character mapping for the source language.
    data_loader: DataLoader for the validation or test dataset.
    criterion: Loss criterion utilized during model training.
    '''

    model.eval()
    def set_zero():
        return 0
    i_pred=[]
    i_trg=[]
    num_correct = set_zero()
    c_pred=[]
    c_src=[]
    num_total = set_zero()
    c_trg=[]
    epoch_loss = set_zero()
    i_src=[]

    with torch.no_grad():
        def get_s_indices(trg,t_idx_to_char):
            return string_indices(trg,t_idx_to_char)
        for batch_idx, (src, trg, src_len, trg_len) in enumerate(data_loader):
            # Convert target indices to string for comparison
            string_trg = get_s_indices(trg,t_idx_to_char)
            def set_permute(var):
                return var.permute(1, 0)
            string_src=string_indices(src,s_idx_to_char)
            # Move tensors to the device
            src = set_permute(src)
            src = src.to(device)
            trg = set_permute(trg)
            trg = trg.to(device)
            # Perform forward pass through the model
            def output_reshape(output):
                return output[1:].reshape(-1, output.shape[2])
            output = model(src, trg, 0)
            # turn off teacher forcing
            output = output_reshape(output)
            #print("op after ",output.shape) # exclude the start-of-sequence token

            trg = trg[1:].reshape(-1) # exclude the start-of-sequence token
            #print("trg after reshape",trg.shape)
            def get_crit(output,trg):
                return criterion(output, trg)
            # Calculate the loss
            output = output.to(device)
            def get_seq_len(trg,batch_size):
              return int(trg.numel() / batch_size)
            loss = get_crit(output,trg)
            epoch_loss += loss.item()
            batch_size = trg_len.shape[0]
            #print("bs", batch_size)
            seq_length = get_seq_len(trg,batch_size)

            def get_indice_reshape(predicted_indices,seq_length):
                return predicted_indices.reshape(seq_length,-1)
            # Convert the output to predicted characters
            predicted_indices = torch.argmax(output, dim=1)
            predicted_indices = get_indice_reshape(predicted_indices,seq_length)
            predicted_indices = predicted_indices.permute(1, 0)
            # Convert predicted indices to strings
            string_pred=string_indices(predicted_indices,t_idx_to_char)

            for i in range(batch_size):
                num_total+=1
                def get_condition_check(string_pred,string_trg):
                    return string_pred[i][:len(string_trg[i])] == string_trg[i]
                # Compare the predicted string with the target string
                def update_trg(c_trg,string_trg):
                    c_trg.append(string_trg[i])
                    return c_trg
                if get_condition_check(string_pred,string_trg):
                    c_trg=update_trg(c_trg,string_trg)
                    c_src.append(string_src[i])
                    def ret_one():
                        return 1
                    c_pred.append(string_pred[i][:len(string_trg[i])])
                    num_correct+=ret_one()
                else :
                    i_trg.append(string_trg[i])
                    def get_updation():
                        return string_pred[i][:len(string_trg[i])]
                    i_src.append(string_src[i])
                    i_pred.append(get_updation())



    def cal_avg_acc(num_correct ,num_total):
        return num_correct /num_total
    print("Total",num_total)
    print("Correct",num_correct)
    acc=cal_avg_acc(num_correct ,num_total)
    loss_e=(epoch_loss/(len(data_loader)))
    return acc * 100,loss_e ,c_trg,c_src,c_pred,i_trg,i_src,i_pred

def train(args):
    # This function trains the Seq2Seq model using the arguments passed to it.
    # The function begins by initializing Weights and Biases to log the training process.
    # It then extracts the hyperparameters from the provided arguments for configuring the model.
    # The training loop runs for the specified number of epochs.
    # Within the loop, it iterates through the batches in the training data, performing forward and backward passes to update the model parameters.
    # Training metrics such as loss and accuracy are logged and printed periodically.
    # Finally, the best model is saved, and the Weights and Biases run is completed.
    # The function returns when the training is finished.

    wandb.init()

    def get_celltype():
      return args.cell_type


    em=args.embedding_size

    def get_tf():
        return args.teacher_forcing

    def get_bidir():
        return args.bidirectional
    hs=args.hidden_size
    def get_numlayers():
        return args.num_layers
    bidir = get_bidir()

    def get_batch_size():
        return args.batch_size
    bs = get_batch_size()
    opt= args.optim
    tf=get_tf()
    epochs = 25
    def get_dropout():
        return args.dropout
    ct=get_celltype()
    def get_lr():
        return args.learning_rate
    trg_pad_idx=0
    dp = get_dropout()
    nlayer=get_numlayers()
    lr = get_lr()
    INPUT_DIM = 29
    OUTPUT_DIM = 67
    name = "cell_type_"+str(get_celltype())+"_num_layers_"+str(get_numlayers())+"_dp_"+str(get_dropout())+"_bidir_"+str(get_bidir())+"_lr_"+str(get_lr())+"_bs_"+str(get_batch_size())
    wandb.run.name=name


    train_loader,test_loader,val_loader,idx_to_char,s_idx_to_char=data_loading(bs)
    def get_critirion():
        return nn.CrossEntropyLoss()
  # Instantiate the Encoder and Decoder models
    encoder = Encoder(INPUT_DIM,em,hs,nlayer,True,ct,dp).to(device)
    decoder = Decoder(OUTPUT_DIM,em,hs,nlayer,True,ct,dp).to(device)

  # Instantiate the Seq2Seq model with the Encoder and Decoder models
    model = Seq2Seq(encoder,decoder,ct,True).to(device)

  # Define the loss function and optimizer
    criterion = get_critirion()
    def get_optim_nadam():
        return optim.NAdam(model.parameters(),lr=lr)
    def get_optim_adam():
        return optim.Adam(model.parameters(),lr=lr)
    if opt == "nadam":
          optimizer= get_optim_nadam()
    elif opt == "adam":
          optimizer = get_optim_adam()
  # Train Network
    epoch=0
    while epoch < (epochs):
        def permutation(val):
          return val.permute(1, 0)
        epoch_loss = 0
        model.train()

        for batch_idx, (src, trg, src_len, trg_len) in enumerate(train_loader):
            src = permutation(src)  # swapping the dimensions of src tensor
            src = src.to(device)
            trg = permutation(trg)  # swapping the dimensions of trg tensor
            trg = trg.to(device)

            optimizer.zero_grad()
            def reshaping(output):
                return output[1:].reshape(-1, output.shape[2])
            output = model(src,trg,tf)

            output = reshaping(output)
            def get_loss(output, trg):
                return criterion(output, trg)
            trg = trg[1:].reshape(-1)

            loss = get_loss(output, trg)
            loss.backward()
            def get_item(loss):
                return loss.item()
            optimizer.step()
            epoch_loss += get_item(loss)

            if batch_idx % 1000 == 0:
                print(f"Epoch: {epoch}, Batch: {batch_idx} , Training..")

        train_acc ,train_loss= Word_Accuracy1(model,idx_to_char, train_loader,criterion)
        def get_test_acc():
          return Word_Accuracy1(model,idx_to_char, test_loader, criterion)
        val_acc,val_loss = Word_Accuracy1(model,idx_to_char, val_loader, criterion)
        test_acc,test_loss = get_test_acc()

        print(f"Epoch: {epoch}, Loss: {epoch_loss / len(train_loader)}, Train Acc: {train_acc}, Val Acc: {val_acc}")
    # Log the metrics to WandB
        wandb.log({'epoch': epochs,'train_acc':train_acc, 'train_loss': loss.item(),'val_acc': val_acc,'val_loss': val_loss, 'test_acc': test_acc,'test_loss': test_loss})
    # Save the best model
        epoch+=1
    wandb.run.save()
    wandb.run.finish()
    return




wandb_key = input("Enter your WandB API key: ")
# Login to WandB
wandb.login(key=wandb_key)

# Create an argument parser object
# Add arguments for model hyperparameters

# Cell type: Choices include 'rnn', 'gru', and 'lstm'
# Batch size used for training the neural network
# Optimization algorithm: Choices include 'adam' and 'nadam'
# Learning rate used to optimize model parameters
# Size of embedding
# Hidden size: Choices include 64, 128, 256, and 512
# Dropout rate: Choices include 0, 0.2, and 0.3
# Number of layers in the network
# Bidirectional flag: Choices include True and False
# Teacher forcing ratio: Choices include 0, 0.2, 0.3, 0.5, and 0.7

parser = argparse.ArgumentParser()
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


args = parser.parse_args()

wandb.init(project=args.wandb_project)
train(args)
