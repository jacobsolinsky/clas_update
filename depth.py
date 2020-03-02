#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:57:54 2020

@author: Lab
"""
import allen_constituency_parse
import allen_dependency_parse
from functools import lru_cache
from graphviz import Digraph


class ConstituencyTree:
    ID_NO = 0
    def __init__(self, node_type, children=None, word=None):
        self.id = ConstituencyTree.ID_NO
        ConstituencyTree.ID_NO += 1
        self.node_type = node_type
        self.children = children
        self.parent = None
        self.leaves = []
        self.is_leaf = False
        if self.children:
            for child in self.children:
                child.parent = self
                self.leaves += child.leaves
        else:
            self.leaves = [self]
            self.is_leaf = True
        self.word = word
        self.nodal_yngve = 0
        self.nodal_frazier = 0
    
    def __repr__(self):
        inner = self.word if self.word else ''.join(
                [f'<li>{child}</li>' for child in self.children]
                )
        return f'<ol>{self.node_type}: {inner}</ol>'
    
    def frazier_yngve_graph(self, dot = None, parent = None):
        final = True
        if not dot:
            self.calculate_yngve_score()
            self.calculate_frazier_score()
            dot = Digraph()
        else:
            final = False
        content = f'''{self.node_type}: {self.word}
            {self.yngve_score}|{self.frazier_score}''' \
            if self.is_leaf else f'''{self.node_type}
            {self.nodal_yngve}|{self.nodal_frazier}'''
        dot.node(str(self.id), content)
        if parent:
            dot.edge(str(self.id), str(parent))
        if not self.is_leaf:
            for child in self.children:
                child.frazier_yngve_graph(dot, self.id)
        if final:
            dot.render('frazier-yngve-plot.gv', view=True)
        
        
    
    def calculate_yngve_score(self):
        self.calculate_nodal_yngve()
        self.calculate_leaf_yngve()
    
    def calculate_nodal_yngve(self):
        if not self.is_leaf:
            for i, child in enumerate(self.children[::-1]):
                print(i)
                print(child)
                child.nodal_yngve = i
                child.calculate_nodal_yngve()
    
    def calculate_leaf_yngve(self):
        for leaf in self.leaves:
            leaf.yngve_score = leaf.nodal_yngve
            handle = leaf
            while handle.parent:
                leaf.yngve_score += handle.parent.nodal_yngve
                handle = handle.parent
                
    def calculate_frazier_score(self):
        self.calculate_nodal_frazier()
        self.calculate_leaf_frazier()
            
    def calculate_nodal_frazier(self):
        if not self.is_leaf:
            self.children[0].nodal_frazier = 1.5 if self.node_type == "S" else 1
            for child in self.children:
                child.calculate_nodal_frazier()
            
    def calculate_leaf_frazier(self):
        for leaf in self.leaves:
            leaf.frazier_score = leaf.nodal_frazier
            handle = leaf
            while handle.parent:
                if handle.parent.nodal_frazier == 0: break
                leaf.frazier_score += handle.parent.nodal_frazier
                handle = handle.parent
    
    def tally_parts_of_speech(self):
        self.total_words = len(self.leaves)
        self.noun_count, self.adj_count, self.adverb_count, \
            self.verb_count, self.det_count, self.conj_count, \
            self.prep_count, self.properN_count \
            = 0, 0, 0, 0, 0, 0, 0, 0
        type_dict = {'V': 'verb_count',
                     'JJ': 'adj_count',
                     'N': 'noun_count',
                     'RB': 'adverb_count',
                     'DT': 'det_count',
                     'PRP': 'personal_pronoun_count',
                     'CC': 'conj_count',
                     'IN': 'prep_count',
                     'NNP': 'properN_count',
        }
        for leaf in self.leaves:
            for k, v in type_dict.items():
                if leaf.node_type.startswith(k):
                    setattr(self, v, getattr(self, v) + 1)
    
    def calculate_clause_count(self, init=True, count=0):
        if self.node_type == 'S':
            count += 1
        if not self.is_leaf:
            for child in self.children:
                child.calculate_clause_count(False, count)
        if init:
            self.clause_count = count
    
    def calculate_mean_and_total(self):
        self.total_Ydepth = 0
        self.total_Fdepth = 0
        for leaf in self.leaves:
            yngve_total += leaf.yngve_score
            frazier_total +=leaf.frazier_score
        self.mean_Ydepth = self.total_Ydepth / len(self.leaves)
        self.mean_Fdepth = self.total_Fdepth / len(self.leaves)

        
    
    
    @staticmethod
    def constituency_parse(sentence, engine='allennlp'):
        return {'allennlp': ConstituencyTree.allen_constituency_parse}[
                engine
                ](sentence)
    
    @classmethod
    def allen_constituency_parse(cls, sentence):
        return ConstituencyTree.allen_constituency_process(
                    allen_constituency_parse.constituency_parse(sentence)[
                    'hierplane_tree'
                    ]['root']
                )
    
    @classmethod
    def allen_constituency_process(cls, parse_dict):
        node_type = parse_dict['nodeType']
        children = None
        if 'children' in parse_dict.keys():
            children = []
            for child in parse_dict['children']:
                children.append(cls.allen_constituency_process(child))
        else:
            return ConstituencyTree(node_type, children, parse_dict['word'])
        return ConstituencyTree(node_type, children)


    
    def calculate_yngve_depth(self, passdown = 0):
        passdown = passdown + self.yngve_depth
        if not self.children:
            self.total_yngve_depth = passdown + self.yngve_depth
        for i, child in enumerate(self.children[::-1]):
            child.yngve_depth = i
            child.calculate_yngve_depth(passdown)
    
    def calculate_frazier_depth(self):
        pass


class DependencyTree:
    def __init__(self):
        self.relations = []
        self.start_positions = []
    
    def __repr__(self):
        inner =  ''.join([
            f'''r.head: {r['head']} @ {r['head_pos']}, 
            relation_type: {r['relation_type']},
            tail: {r['tail']} @ {r['tail_pos']}'''
                for r in self.relations])
        return f'<ul>{inner}</ul>'
    
    def add(self, head, head_pos, relation_type, tail, tail_pos):
        self.relations.append({
                'head': head,
                'head_pos': head_pos,
                'relation_type': relation_type,
                'tail': tail,
                'tail_pos': tail_pos
                })
    
    @property
    @lru_cache(maxsize=1)
    def average_distance(self):
        i = 0
        for r in self.relations:
            i += abs(r['head_pos'] - r['tail_pos'])
        return i / len(self.relations)
    
    @staticmethod
    def dependency_parse(sentence, engine='allennlp'):
        return {'allennlp': DependencyTree.allen_dependency_parse}[
                engine
                ](sentence)
    
    @classmethod
    def allen_dependency_parse(cls, sentence):
        return DependencyTree.allen_dependency_process(
                    allen_dependency_parse.dependency_parse(sentence)[
                    'hierplane_tree'
                    ]['root']
                )
        
    def preprocess(self, parse_dict):
        self.start_positions.append(parse_dict['spans'][0]['start'])
        if 'children' in parse_dict.keys():
            for child in parse_dict['children']:
                self.preprocess(child)
    
    @classmethod
    def allen_dependency_process(cls, parse_dict, dependency_tree = None):
        if 'children' not in parse_dict.keys(): return
        if not dependency_tree:
            dependency_tree = DependencyTree()
            dependency_tree.preprocess(parse_dict)
            dependency_tree.start_positions.sort()
        head = parse_dict['word']
        head_pos = parse_dict['spans'][0]['start']
        head_pos = dependency_tree.start_positions.index(head_pos)
        for child in parse_dict['children']:
            relation_type = child['link']
            tail = child['word']
            tail_pos = child['spans'][0]['start']
            tail_pos = dependency_tree.start_positions.index(tail_pos)
            dependency_tree.add(head, head_pos, relation_type, tail, tail_pos)
            cls.allen_dependency_process(child, dependency_tree)
        return dependency_tree

def get_statistics(sentences):
    for i, sentence in sentences:
        