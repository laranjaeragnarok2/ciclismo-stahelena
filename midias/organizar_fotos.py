#!/usr/bin/env python3
"""
Script de Classificação e Organização Automática das Mídias Raspadas
Classifica as fotos por dimensão, orientação (Landscape/Hero, Portrait/Mobile, Quadradas) e gera catálogo em JSON/CSV.
"""

import os
import sys
import json
import csv
import shutil
from pathlib import Path
from PIL import Image


def classificar_e_organizar():
    src_dir = Path("/home/horyu/Projetos/ciclismo_santa_helena_midias/facebook_fotos")
    dest_base = Path("/home/horyu/Projetos/ciclismo_santa_helena_midias/facebook_fotos_organizadas")

    if not src_dir.exists():
        print(f"Diretório de origem não encontrado: {src_dir}")
        sys.exit(1)

    # Subpastas de classificação
    hero_dir = dest_base / "01_banners_hero"
    mobile_dir = dest_base / "02_retratos_mobile"
    square_dir = dest_base / "03_quadradas_galeria"
    thumb_dir = dest_base / "04_pequenas_thumbnails"

    for d in [hero_dir, mobile_dir, square_dir, thumb_dir]:
        d.mkdir(parents=True, exist_ok=True)

    print("=== Iniciando Classificação e Organização de Mídias ===")
    print(f"Origem: {src_dir}")
    print(f"Destino: {dest_base}")

    files = [f for f in src_dir.glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
    print(f"Total de fotos encontradas: {len(files)}")

    catalog = []
    stats = {"hero": 0, "mobile": 0, "square": 0, "thumb": 0, "erro": 0}

    for img_path in files:
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                ratio = width / float(height) if height > 0 else 1.0

                # Regras de classificação
                if width < 600 or height < 600:
                    categoria = "thumb"
                    dest_folder = thumb_dir
                    uso_sugerido = "Thumbnail / Ícone"
                elif ratio >= 1.25 and width >= 1000:
                    categoria = "hero"
                    dest_folder = hero_dir
                    uso_sugerido = "Banner Hero / Carrossel Principal"
                elif ratio <= 0.85:
                    categoria = "mobile"
                    dest_folder = mobile_dir
                    uso_sugerido = "Card Vertical / Mobile Stories"
                else:
                    categoria = "square"
                    dest_folder = square_dir
                    uso_sugerido = "Galeria Grid / Eventos"

                dest_file = dest_folder / img_path.name
                shutil.copy2(img_path, dest_file)
                stats[categoria] += 1

                catalog.append({
                    "filename": img_path.name,
                    "width": width,
                    "height": height,
                    "aspect_ratio": round(ratio, 2),
                    "category": categoria,
                    "suggested_use": uso_sugerido,
                    "path": str(dest_file)
                })

        except Exception as e:
            stats["erro"] += 1
            print(f"Erro ao processar {img_path.name}: {e}")

    # Salvar Catálogo em JSON e CSV
    json_path = dest_base / "catalogo_midias_classificadas.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=4)

    csv_path = dest_base / "catalogo_midias_classificadas.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "width", "height", "aspect_ratio", "category", "suggested_use", "path"])
        writer.writeheader()
        writer.writerows(catalog)

    print("\n==========================================")
    print(" Classificação Concluída com Sucesso!")
    print(f" 🖼️ Banners Hero (Alta Resolução Widescreen): {stats['hero']}")
    print(f" 📱 Retratos Mobile (Verticais): {stats['mobile']}")
    print(f" 🟩 Quadradas / Padrão (Galeria Grid): {stats['square']}")
    print(f" 🔍 Thumbnails / Pequenas: {stats['thumb']}")
    print(f" 📁 Pasta Organizada: {dest_base}")
    print(f" 📄 Catálogo JSON: {json_path}")
    print(f" 📄 Catálogo CSV: {csv_path}")
    print("==========================================")


if __name__ == "__main__":
    classificar_e_organizar()
