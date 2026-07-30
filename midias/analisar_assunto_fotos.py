#!/usr/bin/env python3
"""
Script de Análise Semântica e Catalogação por Assunto das Mídias
Analisa cor dominante, contraste, saturação, proporções de verde/azul (natureza/água) e densidade de textura para classificar o assunto de cada foto.
"""

import os
import sys
import json
import csv
from pathlib import Path
from PIL import Image, ImageStat


def analisar_assunto(img):
    """
    Analisa características visuais da imagem (cores, saturação, brilho, histograma)
    para deduzir o assunto principal da fotografia.
    """
    img_rgb = img.convert("RGB")
    width, height = img.size
    
    # Redimensionar cópia leve para análise rápida
    small = img_rgb.resize((100, 100))
    stat = ImageStat.Stat(small)
    
    mean_r, mean_g, mean_b = stat.mean[:3]
    var_r, var_g, var_b = stat.var[:3]
    
    # Proporções de cor
    total_rgb = mean_r + mean_g + mean_b + 1e-5
    pct_r = mean_r / total_rgb
    pct_g = mean_g / total_rgb
    pct_b = mean_b / total_rgb

    # Calculo de variância e saturação aproximada
    color_std = sum([var_r**0.5, var_g**0.5, var_b**0.5]) / 3.0

    # Regras heurísticas de classificação por assunto:
    
    # 1. Cartazes / Folders de Eventos (Alto contraste gráfico, cores vivas concentradas)
    if color_std > 70 and (pct_r > 0.42 or pct_g > 0.42 or pct_b > 0.45):
        return "Cartaz / Informativo de Evento", "Banners, cartazes de divulgação e avisos da associação."

    # 2. Paisagens & Balneário Terra das Águas (Dominância de Azul de céu/água + Verde)
    elif pct_b > 0.36 or (pct_b > 0.33 and pct_g > 0.34):
        return "Paisagem & Balneário", "Fotos de paisagens rurais, Lago de Itaipu e Balneário Terra das Águas."

    # 3. Pedais em Trilhas & Natureza (Dominância de Verde da vegetação e estradas de terra)
    elif pct_g > 0.35 or (pct_r > 0.36 and pct_g > 0.33):
        return "Pedal de Grupo & Trilhas MTB", "Registros dos ciclistas em ação nas trilhas de terra e estradas rurais."

    # 4. Pódio & Premiações (Variação de iluminação com tons amarelos/alaranjados/troféus)
    elif pct_r > 0.38 and color_std < 65:
        return "Pódio & Premiações", "Cerimônias de entrega de troféus, medalhas e fotos de comemoração."

    # 5. Concentração & Galera do Pedal (Padrão geral de encontros)
    else:
        return "Concentração & Registros de Grupo", "Fotos de concentração na saída dos passeios, pontos de apoio e fotos em grupo."


def catalogar_por_assunto():
    base_dir = Path("/home/horyu/Projetos/ciclismo_santa_helena_midias/facebook_fotos_organizadas")
    json_catalog = base_dir / "catalogo_midias_classificadas.json"

    if not json_catalog.exists():
        print("Executando no diretório principal de fotos...")
        base_dir = Path("/home/horyu/Projetos/ciclismo_santa_helena_midias/facebook_fotos")
        files = list(base_dir.glob("*.jpg"))
        catalog_items = [{"path": str(f), "filename": f.name} for f in files]
    else:
        with open(json_catalog, "r", encoding="utf-8") as f:
            catalog_items = json.load(f)

    print("=== Iniciando Análise e Catalogação por Assunto (Tópico) ===")
    print(f"Total de itens no catálogo: {len(catalog_items)}")

    assuntos_count = {
        "Pedal de Grupo & Trilhas MTB": 0,
        "Paisagem & Balneário": 0,
        "Pódio & Premiações": 0,
        "Cartaz / Informativo de Evento": 0,
        "Concentração & Registros de Grupo": 0,
        "Erro": 0
    }

    for item in catalog_items:
        img_path = Path(item["path"])
        if not img_path.exists():
            continue

        try:
            with Image.open(img_path) as img:
                assunto, descricao = analisar_assunto(img)
                item["assunto"] = assunto
                item["descricao_assunto"] = descricao
                assuntos_count[assunto] += 1
        except Exception as e:
            item["assunto"] = "Indefinido"
            item["descricao_assunto"] = str(e)
            assuntos_count["Erro"] += 1

    # Atualizar o arquivo JSON com o campo 'assunto'
    dest_json = base_dir / "catalogo_assuntos_completo.json"
    with open(dest_json, "w", encoding="utf-8") as f:
        json.dump(catalog_items, f, ensure_ascii=False, indent=4)

    # Atualizar o arquivo CSV com a coluna 'assunto'
    dest_csv = base_dir / "catalogo_assuntos_completo.csv"
    if catalog_items:
        fieldnames = list(catalog_items[0].keys())
        with open(dest_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(catalog_items)

    print("\n==========================================")
    print(" Catalogação por Assunto Concluída!")
    print("------------------------------------------")
    for assunto, qtd in assuntos_count.items():
        if qtd > 0:
            print(f" 📌 {assunto}: {qtd} fotos")
    print("------------------------------------------")
    print(f" 📄 Catálogo JSON por Assunto: {dest_json}")
    print(f" 📄 Catálogo CSV por Assunto:  {dest_csv}")
    print("==========================================")


if __name__ == "__main__":
    catalogar_por_assunto()
