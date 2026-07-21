"""
entrenar_vocabulario_pytorch.py (CON REANUDACIÓN)
Word2Vec con PyTorch - Guarda y reanuda entrenamiento
"""

import os
import re
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from collections import Counter
import numpy as np

# ⚡ CONFIGURACIÓN
CORPUS_DIR = "data/corpus"
MODEL_PATH = "data/vocabulario_pytorch.pt"
VOCAB_PATH = "data/vocabulario_pytorch.json"
EMBEDDING_DIM = 150
WINDOW_SIZE = 4
MIN_COUNT = 5
BATCH_SIZE = 1024
EPOCHS = 8
LEARNING_RATE = 0.001


def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\sáéíóúüñ]', ' ', texto)
    texto = re.sub(r'\d+', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


def cargar_textos():
    archivos = [f for f in os.listdir(CORPUS_DIR) if f.endswith('.txt')]
    if not archivos:
        print("❌ No hay archivos .txt en data/corpus/")
        return []
    
    todas_palabras = []
    print(f"\n📚 Cargando {len(archivos)} archivos...")
    for archivo in archivos:
        ruta = os.path.join(CORPUS_DIR, archivo)
        print(f"   📄 {archivo}")
        with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
            texto = f.read()
        texto_limpio = limpiar_texto(texto)
        todas_palabras.extend(texto_limpio.split())
    
    print(f"   ✅ {len(todas_palabras)} palabras cargadas")
    return todas_palabras


def crear_vocabulario(palabras):
    contador = Counter(palabras)
    palabras_filtradas = [p for p in palabras if contador[p] >= MIN_COUNT]
    vocabulario = sorted(set(palabras_filtradas))
    palabra_a_idx = {p: i for i, p in enumerate(vocabulario)}
    idx_a_palabra = {i: p for p, i in palabra_a_idx.items()}
    
    print(f"   📖 Vocabulario: {len(vocabulario)} palabras")
    return vocabulario, palabra_a_idx, idx_a_palabra


def generar_pares(palabras, palabra_a_idx):
    """Genera pares - versión rápida (1 de cada 3)"""
    pares = []
    total = len(palabras)
    contador = 0
    
    print(f"   🔗 Generando pares (modo rápido)...")
    for i, palabra in enumerate(palabras):
        if i % 200000 == 0:
            print(f"      {i}/{total} ({(i/total)*100:.0f}%)")
        
        if palabra not in palabra_a_idx:
            continue
        
        centro = palabra_a_idx[palabra]
        inicio = max(0, i - WINDOW_SIZE)
        fin = min(total, i + WINDOW_SIZE + 1)
        
        for j in range(inicio, fin):
            if i != j and palabras[j] in palabra_a_idx:
                contador += 1
                if contador % 3 == 0:
                    contexto = palabra_a_idx[palabras[j]]
                    pares.append((centro, contexto))
    
    print(f"   ✅ {len(pares)} pares generados")
    return pares


class Word2VecDataset(Dataset):
    def __init__(self, pares):
        self.centros = torch.tensor([p[0] for p in pares], dtype=torch.long)
        self.contextos = torch.tensor([p[1] for p in pares], dtype=torch.long)
    
    def __len__(self):
        return len(self.centros)
    
    def __getitem__(self, idx):
        return self.centros[idx], self.contextos[idx]
