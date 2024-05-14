"""
    Some handy functions for pytorch model training ...
"""
import os
import pickle

import torch

# Checkpoints
device = torch.device('cpu')

import random
import numpy as np

def save_checkpoint(model, model_dir):
    # Save the entire model to a file
    torch.save(model, model_dir)

def resume_checkpoint(model, model_dir, device_id):
    # Load the entire model from a file
    model = torch.load(model_dir, map_location=lambda storage, loc: storage.cuda(device=device_id))
    return model

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f)

def seed_it(seed):
    random.seed(seed)
    os.environ["PYTHONSEED"] = str(seed)
    np.random.seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.enabled = True
    torch.manual_seed(seed)

def use_cuda(enabled, device_id=0):
    if enabled and torch.cuda.is_available():
        torch.cuda.set_device(device_id)
    else:
        print("Warning: CUDA is not available, using CPU instead.")

def use_optimizer(network, params):
    if params['optimizer'] == 'sgd':
        optimizer = torch.optim.SGD(network.parameters(),
                                    lr=params['sgd_lr'],
                                    momentum=params['sgd_momentum'],
                                    weight_decay=params['l2_regularization'])
    elif params['optimizer'] == 'adam':
        optimizer = torch.optim.Adam(network.parameters(),
                                     lr=params['adam_lr'],
                                     weight_decay=params['l2_regularization'])
    return optimizer
