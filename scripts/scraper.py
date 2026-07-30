#!/usr/bin/env python3
"""
Script de Extração Completa do Instagram (@ciclismosantahelena)
Desenvolvido para baixar mídias (fotos, vídeos, reels), legendas, metadados e gerar relatórios em JSON e CSV.
"""

import sys
import os
import json
import csv
import argparse
from pathlib import Path

# Certifica-se de usar a biblioteca instaloader
try:
    import instaloader
except ImportError:
    print("ERRO: O pacote 'instaloader' não foi encontrado.")
    print("Por favor, instale usando: pip install instaloader")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extrai publicações, mídias e metadados de um perfil do Instagram."
    )
    parser.add_argument(
        "--username",
        type=str,
        default="ciclismosantahelena",
        help="Nome de usuário do perfil a ser extraído (padrão: ciclismosantahelena)",
    )
    parser.add_argument(
        "--login",
        type=str,
        default=None,
        help="Seu usuário do Instagram para realizar login e evitar limites de requisição (HTTP 429)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Diretório de destino para salvar os arquivos (padrão: ./downloads_<username>)",
    )
    parser.add_argument(
        "--max-posts",
        type=int,
        default=None,
        help="Número máximo de postagens para baixar (opcional)",
    )
    parser.add_argument(
        "--fast-update",
        action="store_true",
        help="Para a extração assim que encontrar uma postagem já baixada",
    )
    return parser.parse_args()


def extract_profile(target_username, login_user=None, output_dir=None, max_posts=None, fast_update=False):
    if not output_dir:
        output_dir = Path.cwd() / f"downloads_{target_username}"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Iniciando extração do perfil @{target_username} ===")
    print(f"Diretório de saída: {output_dir}")

    # Inicializar Instaloader com configurações recomendadas
    L = instaloader.Instaloader(
        dirname_pattern=str(output_dir / "{shortcode}"),
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=True,
        download_geotags=True,
        download_comments=False,
        save_metadata=True,
        compress_json=False,
    )

    if login_user:
        print(f"Fazendo login com @{login_user}...")
        try:
            L.interactive_login(login_user)
            print("Login efetuado com sucesso!")
        except Exception as e:
            print(f"Aviso ao realizar login: {e}")
            print("Tentando continuar sem login...")

    try:
        profile = instaloader.Profile.from_username(L.context, target_username)
    except Exception as e:
        print(f"\n[ERRO] Não foi possível carregar o perfil @{target_username}: {e}")
        print("\n=> DICA: O Instagram bloqueia acessos anônimos repetidos (HTTP 429).")
        print(f"=> Tente executar fornecendo seu login: python {sys.argv[0]} --login SEU_USUARIO")
        sys.exit(1)

    print("\n--- Informações do Perfil ---")
    print(f"Nome: {profile.full_name}")
    print(f"Bio: {profile.biography.replace('\n', ' ')}")
    print(f"Seguidores: {profile.followers}")
    print(f"Seguindo: {profile.followees}")
    print(f"Total de Publicações: {profile.mediacount}")

    # Salvar metadados do perfil
    profile_meta = {
        "username": profile.username,
        "full_name": profile.full_name,
        "biography": profile.biography,
        "followers": profile.followers,
        "followees": profile.followees,
        "mediacount": profile.mediacount,
        "profile_pic_url": profile.profile_pic_url,
        "is_private": profile.is_private,
        "is_verified": profile.is_verified,
    }
    with open(output_dir / "perfil_info.json", "w", encoding="utf-8") as f:
        json.dump(profile_meta, f, ensure_ascii=False, indent=4)

    # Baixar foto de perfil
    try:
        L.download_profilepic(profile)
    except Exception as e:
        print(f"Não foi possível baixar a foto de perfil: {e}")

    # Processar publicações
    posts_data = []
    count = 0

    print("\n--- Extraindo Publicações ---")
    posts_generator = profile.get_posts()

    for post in posts_generator:
        if max_posts and count >= max_posts:
            print(f"Limite máximo de {max_posts} postagens atingido.")
            break

        count += 1
        print(f"[{count}/{profile.mediacount}] Baixando post: {post.shortcode} ({post.date_utc.strftime('%Y-%m-%d %H:%M:%S')})")

        try:
            downloaded = L.download_post(post, target=output_dir / post.shortcode)
            
            post_info = {
                "shortcode": post.shortcode,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "date_utc": post.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "is_video": post.is_video,
                "typename": post.typename,
                "caption": post.caption if post.caption else "",
                "likes": post.likes,
                "comments": post.comments,
                "video_view_count": post.video_view_count if post.is_video else None,
                "location": post.location.name if post.location else None,
                "folder": str(output_dir / post.shortcode)
            }
            posts_data.append(post_info)

            if fast_update and not downloaded:
                print("Modo --fast-update ativado: post já existente encontrado. Parando extração.")
                break

        except Exception as e:
            print(f"Erro ao processar post {post.shortcode}: {e}")

    # Salvar relatório resumido dos posts em JSON e CSV
    json_summary = output_dir / "relatorio_posts.json"
    with open(json_summary, "w", encoding="utf-8") as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=4)

    csv_summary = output_dir / "relatorio_posts.csv"
    with open(csv_summary, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["shortcode", "url", "date_utc", "is_video", "typename", "caption", "likes", "comments", "location", "folder"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in posts_data:
            row = {k: p[k] for k in fieldnames if k in p}
            writer.writerow(row)

    print(f"\n==========================================")
    print(f" Extração concluída com sucesso!")
    print(f" Total de posts extraídos: {len(posts_data)}")
    print(f" Mídias salvas em: {output_dir}")
    print(f" Relatório JSON: {json_summary}")
    print(f" Relatório CSV:  {csv_summary}")
    print(f"==========================================")


if __name__ == "__main__":
    args = parse_args()
    extract_profile(
        target_username=args.username,
        login_user=args.login,
        output_dir=args.output_dir,
        max_posts=args.max_posts,
        fast_update=args.fast_update,
    )
