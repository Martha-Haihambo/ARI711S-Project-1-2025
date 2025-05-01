# Part 2 Traffic Sign Recognition  

This AI model is a traffic sign classifier. It recognizes and classifies images of traffic signs into one of 43 categories using deep learning.

# Project Structure

-gtsrb
-straffic.py

# Experimentation Results
- Accuracy: 98.38%  

# Learning Curves
- The model was trained for 10 epochs. Learning curves was not plotted in this version.

# Hyperparameters
- Epochs:10  
- Batch Size: 64  
- Optimizer: Adam  
- Loss: Categorical Crossentropy  
- Dropout Rate: 0.5

# What Worked 
- Using a small image size kept training fast without losing accuracy.
- Adding a dropout layer helped avoid overfitting.
- The model generalizes well with minimal tuning.

# What didnt Worked 
- Increasing depth or complexity did not significantly improve accuracy.
- Training for more epochs led to overfitting beyond 10 epochs.

# Finale Module
- This version uses a clean and optimized CNN model with high test accuracy.



# Requirements 
-python 3.10
-tensor flow 2.19.0
-pip 21.2.3 
 
 # Authors 
Donevan Stuurman 222077336 
Martha Haihambo 223003344

# Copyright 
Copyright (c) 2025, Donevan Stuurman and Martha Haihambo.