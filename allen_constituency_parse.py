#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 09:40:03 2020

@author: Lab
"""

from allennlp.models.archival import load_archive
from allennlp.service.predictors import Predictor

archive = load_archive(
            "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz"
        )

def constituency_parse(sentence):
    predictor = Predictor.from_archive(archive, 'constituency-parser')
    return predictor.predict(sentence)