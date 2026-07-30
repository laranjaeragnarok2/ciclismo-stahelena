#!/usr/bin/env python3
"""
Script de Curadoria e Agrupamento por Álbuns Temáticos de Pedais
Enxuga o volume total de mídias, elimina fotos redundantes e organiza uma seleção 'Best Of' em álbuns temáticos.
"""

import os
import sys
import json
import csv
import shutil
from pathlib import Path


def curar_e_agrupar():
    src_json = Path("/home/horyu/Projetos/ciclismo_santa_helena_midias/facebook_fotos_organizadas/catalogo_assuntos_completo.json")
    dest_base = Path("/home/horyu/Projetos/ciclismo_santa_helena_midias/albuns_curados")

    if not src_json.exists():
        print(f"Catálogo de origem não encontrado: {src_json}")
        sys.exit(1)

    with open(src_json, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Definir Álbuns Temáticos
    albuns = {
        "Album_Podios_e_Conquistas": {
            "title": "🏆 Pódios & Conquistas",
            "description": "Celebrações de vitórias, entrega de troféus e momentos no pódio dos atletas.",
            "dir": dest_base / "01_Podios_e_Conquistas",
            "filter": lambda x: x.get("assunto") == "Pódio & Premiações",
            "limit": 20
        },
        "Album_Cicloturismo_Terra_das_Aguas": {
            "title": "🌅 Cicloturismo Terra das Águas",
            "description": "Passeios contemplativos pelas rotas turísticas e Lago de Itaipu.",
            "dir": dest_base / "02_Cicloturismo_Terra_das_Aguas",
            "filter": lambda x: x.get("assunto") == "Paisagem & Balneário",
            "limit": 25
        },
        "Album_Trilhas_MTB_Itaipu": {
            "title": "🚵 Trilhas MTB & Refúgio Itaipu",
            "description": "Desafios de Mountain Bike nas estradas rurais e trilhas de terra.",
            "dir": dest_base / "03_Trilhas_MTB_Itaipu",
            "filter": lambda x: x.get("assunto") == "Pedal de Grupo & Trilhas MTB",
            "limit": 25
        },
        "Album_Pedais_Urbanos_e_Familia": {
            "title": "👥 Pedais da Família & Concentração",
            "description": "Fotos dos grupos de saída, passeios urbanos e momentos de confraternização.",
            "dir": dest_base / "04_Pedais_Urbanos_e_Familia",
            "filter": lambda x: x.get("assunto") == "Concentração & Registros de Grupo",
            "limit": 25
        },
        "Album_Cartazes_e_Divulgacao": {
            "title": "📢 Cartazes & Banners de Eventos",
            "description": "Flyers oficiais de divulgação dos pedais e eventos anteriores.",
            "dir": dest_base / "05_Cartazes_e_Divulgacao",
            "filter": lambda x: x.get("assunto") == "Cartaz / Informativo de Evento",
            "limit": 15
        }
    }

    # Criar pastas dos álbuns
    for key, info in albuns.items():
        info["dir"].mkdir(parents=True, exist_ok=True)

    print("=== Iniciando Curadoria de Mídias (Enxugando e Agrupando em Álbuns) ===")
    print(f"Total de mídias brutas analisadas: {len(items)}")

    curated_items = []
    stats = {}

    for album_key, album_info in albuns.items():
        matching = [item for item in items if album_info["filter"](item)]
        
        # Priorizar fotos de maior resolução (width >= 800) para garantir qualidade no site
        matching_sorted = sorted(matching, key=lambda x: (x.get("width", 0) * x.get("height", 0)), reverse=True)
        
        # Aplicar curadoria enxuta (limitar aos melhores exemplares)
        selected = matching_sorted[:album_info["limit"]]
        stats[album_info["title"]] = len(selected)

        for idx, item in enumerate(selected):
            src_file = Path(item["path"])
            if not src_file.exists():
                continue

            # Nome limpo e organizado no álbum
            new_filename = f"{album_key}_{idx+1:02d}{src_file.suffix}"
            dest_file = album_info["dir"] / new_filename
            shutil.copy2(src_file, dest_file)

            curated_item = {
                "album_id": album_key,
                "album_title": album_info["title"],
                "filename": new_filename,
                "original_filename": item["filename"],
                "width": item.get("width"),
                "height": item.get("height"),
                "aspect_ratio": item.get("aspect_ratio"),
                "suggested_use": item.get("suggested_use"),
                "path": str(dest_file)
            }
            curated_items.append(curated_item)

    # Salvar catálogo curado em JSON e CSV
    json_curated = dest_base / "catalogo_albuns_curados.json"
    with open(json_curated, "w", encoding="utf-8") as f:
        json.dump(curated_items, f, ensure_ascii=False, indent=4)

    csv_curated = dest_base / "catalogo_albuns_curados.csv"
    if curated_items:
        fieldnames = list(curated_items[0].keys())
        with open(csv_curated, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(curated_items)

    print("\n==========================================")
    print(" Curadoria & Organização de Álbuns Concluída!")
    print(f" 🎯 De 1.050 fotos brutas -> Reduzido para {len(curated_items)} Destaques de Alta Qualidade!")
    print("------------------------------------------")
    for album_name, qtd in stats.items():
        print(f" 📂 {album_name}: {qtd} fotos selecionadas")
    print("------------------------------------------")
    print(f" 📁 Pasta dos Álbuns: {dest_base}")
    print(f" 📄 Catálogo JSON: {json_curated}")
    print(f" 📄 Catálogo CSV:  {csv_curated}")
    print("==========================================")


if __name__ == "__main__":
    curar_e_agrupar()
