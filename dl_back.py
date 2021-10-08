import pandas as pd
import numpy as np

import re

from tqdm import tqdm

import torch
from torch.utils.data import Dataset, DataLoader
import os

class GetDataset(Dataset):
    def __init__(self, df, train_data=True):
        self.df = df
        self.train_data = train_data
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        text = self.df.loc[index, 'selftext']
        
        encoded_dict = tokenizer.encode_plus(
            text,
            add_special_tokens = True,      
            max_length = 256,    # 512       
            pad_to_max_length = True,
            return_attention_mask = True,  
            return_tensors = 'pt'  
        )
        
        padded_token_list = encoded_dict['input_ids'][0]
        att_mask = encoded_dict['attention_mask'][0]
        
        if self.train_data:
            label = torch.tensor(self.df.loc[index, 'label'])
            return padded_token_list, att_mask, label
        
        return padded_token_list, att_mask

def create_prediction(data_df, model_path=''):
    if model_path.endswith('.pt'):
        model.load(model_path)
        model.eval()
        
        test_data = GetDataset(data_df, train_data=False)


        test_loader = DataLoader(test_data, 
                               batch_size=1,
                               shuffle=False,)
                               
        for i, batch in enumerate(test_loader):
            ind_batch = batch[0].to(device)
            mask_batch = batch[1].to(device)
            outputs = model(ind_batch,  attention_mask=mask_batch)
            
            pred = outputs[0]
            pred = pred.detach().cpu().numpy()
            
            target = labels_batch.to('cpu').numpy()
            
            target_list.extend(target)
            
            if i == 0:
                stacked_preds = pred
            else:
                stacked_preds = np.vstack([stacked_preds, pred])
                
        preds = np.argmax(stacked_preds, axis=1)
        return preds
    else:
        return 'Model weigths are empty! Try again!'
        
    


    
    
        
