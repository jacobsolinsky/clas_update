#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:55:40 2020

@author: Lab
"""

from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/biaffine-dependency-parser-ptb-2018.08.23.tar.gz")
def dependency_parse(sentence="If I bring 10 dollars tomorrow, can you buy me lunch?"):
    return predictor.predict(sentence)