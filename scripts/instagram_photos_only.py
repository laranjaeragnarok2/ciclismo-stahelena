#!/usr/bin/env python3
"""
Script de Extração de Fotos Únicas do Instagram (@ciclismosantahelena)
- Ignora Vídeos, Reels e Carrosséis (apenas fotos simples 'GraphImage').
- Respeita limites de requisição sem login (delay configurável e retry em caso de HTTP 429).
- Salva fotos, legendas e relatório CSV/JSON.
"""

import sys
import os
import time
import json
import csv
import random
import argparse
from pathlib import Path

try:
    import instaloader
    from instaloader.exceptions import TooManyRequestsException, ConnectionException
except ImportError:
    print("ERRO: instaloader não instalado.")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Extrai APENAS fotos únicas do Instagram sem login.")
    parser.add_argument("--username", type=str, default="ciclismosantahelena", help="Perfil do Instagram")
    parser.add_argument("--output-dir", type=str, default="/home/horyu/Projetos/ciclismo_santa_helena_midias/instagram_fotos", help="Diretório de destino")
    parser.add_argument("--delay-min", type=float, default=5.0, help="Tempo mínimo de espera entre posts (segundos)")
    parser.add_argument("--delay-max", type=float, default=10.0, help="Tempo máximo de espera entre posts (segundos)")
    parser.add_argument("--max-photos", type=int, default=None, help="Limite máximo de fotos a baixar (opcional)")
    return parser.parse_args()


def extract_photos_only():
    args = parse_args()
    target_dir = Path(args.output_dir)
    photos_dir = target_dir / "fotos"
    photos_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Iniciando extração de FOTOS ÚNICAS do Instagram (@{args.username}) ===")
    print(f"Diretório de saída: {target_dir}")
    print(f"Filtro: APENAS fotos únicas (Vídeos e Carrosséis serão ignorados)")
    print(f"Delay entre requisições: {args.delay_min}s a {args.delay_max}s")

    L = instaloader.Instaloader(
        dirname_pattern=str(photos_dir),
        download_pictures=True,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern="",  # Não criar múltiplos .txt adicionais soltos por default
    )

    try:
        profile = instaloader.Profile.from_username(L.context, args.username)
    except Exception as e:
        print(f"\n[ERRO] Falha ao acessar perfil @{args.username}: {e}")
        print("Dica: O Instagram pode ter aplicado limitação temporária no IP. Aguarde alguns minutos antes de tentar novamente.")
        sys.exit(1)

    print(f"\nTotal de posts no perfil: {profile.mediacount}")
    
    posts_summary = []
    saved_photos_count = 0

    try:
        for post in profile.get_posts():
            if args.max_photos and saved_photos_count >= args.max_photos:
                print(f"\nLimite de {args.max_photos} fotos atingido.")
                break

            # 1. FILTRAR APENAS FOTOS ÚNICAS (GraphImage)
            if post.is_video:
                print(f"[PULADO - VÍDEO] Post {post.shortcode}")
                continue

            if post.typename != "GraphImage":
                print(f"[PULADO - CARROSSEL/OUTRO] Post {post.shortcode} (Tipo: {post.typename})")
                continue

            # Verificar se a foto já foi baixada
            img_filename = f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.jpg"
            txt_filename = f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.txt"
            img_path = photos_dir / img_filename
            txt_path = photos_dir / txt_filename

            print(f"\n[FOTO {saved_photos_count + 1}] Processando {post.shortcode} ({post.date_utc.strftime('%Y-%m-%d')})...")

            try:
                # Baixar foto e salvar legenda
                L.download_post(post, target=photos_dir)
                
                saved_photos_count += 1

                info = {
                    "shortcode": post.shortcode,
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "date_utc": post.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    "caption": post.caption if post.caption else "",
                    "likes": post.likes,
                    "image_file": img_filename,
                }
                posts_summary.append(info)

                # Salvar relatório parcial para não perder nada
                with open(target_dir / "relatorio_fotos.json", "w", encoding="utf-8") as f:
                    json.dump(posts_summary, f, ensure_ascii=False, indent=4)

                # 2. DELAY RESPEITANDO LIMITES DO INSTAGRAM
                sleep_time = random.uniform(args.delay_min, args.delay_max)
                print(f"-> Foto salva com sucesso. Pausa de segurança: {sleep_time:.1f}s...")
                time.sleep(sleep_time)

            except TooManyRequestsException:
                print("\n⚠️ [AVISO HTTP 429] Instagram solicitou pausa por limite de requisições!")
                print("Aguardando 120 segundos para liberar o limite do IP...")
                time.sleep(120)
            except Exception as e:
                print(f"Erro ao baixar post {post.shortcode}: {e}")

    except TooManyRequestsException:
        print("\n⚠️ [HTTP 429] Limite de requisições atingido. O progresso até aqui foi salvo!")
    except Exception as e:
        print(f"\nInterrupção ou erro na execução: {e}")

    # Salvar relatório final em CSV
    csv_file = target_dir / "relatorio_fotos.csv"
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["shortcode", "url", "date_utc", "caption", "likes", "image_file"])
        writer.writeheader()
        writer.writerows(posts_summary)

    print("\n==========================================")
    print(f" Extração do Instagram Concluída!")
    print(f" Total de Fotos Únicas Baixadas: {saved_photos_count}")
    print(f" Pasta das Fotos: {photos_dir}")
    print(f" Relatório CSV: {csv_file}")
    print("==========================================")


if __name__ == "__main__":
    extract_photos_only()
