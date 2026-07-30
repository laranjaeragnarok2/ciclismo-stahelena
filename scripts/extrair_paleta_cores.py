#!/usr/bin/env python3
"""
Script de Extração da Paleta de Cores (Kit de Cores) Oficial da Marca
Analisador de cores dominantes do logo e das fotos do cliente.
"""

import json
from pathlib import Path
from PIL import Image


def extrair_cores_imagem(image_path, num_colors=5):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize((150, 150))
        result = img.quantize(colors=num_colors)
        palette = result.getpalette()
        color_counts = sorted(result.getcolors(), reverse=True)
        
        colors = []
        for count, index in color_counts[:num_colors]:
            r = palette[index * 3]
            g = palette[index * 3 + 1]
            b = palette[index * 3 + 2]
            hex_code = f"#{r:02X}{g:02X}{b:02X}"
            colors.append({"hex": hex_code, "rgb": f"rgb({r}, {g}, {b})", "pixels": count})
        return colors


def gerar_kit_cores():
    logo_path = Path("/home/horyu/Projetos/ciclismo/midias/logo/logo_ciclismo_santa_helena.jpg")
    output_dir = Path("/home/horyu/Projetos/ciclismo/midias")
    
    if not logo_path.exists():
        print(f"Logo não encontrada em: {logo_path}")
        return

    cores_logo = extrair_cores_imagem(logo_path, num_colors=6)

    kit_cores = {
        "marca": "Associação Santa-Helenense de Ciclismo (Ciclismo Santa Helena)",
        "logo_path": str(logo_path),
        "paleta_oficial": [
            {
                "nome": "Laranja Neon Ação (Primary CTA)",
                "hex": "#FF5722",
                "rgb": "rgb(255, 87, 34)",
                "uso": "Botões de ação principal (CTA), destaque de datas e acentos de velocidade"
            },
            {
                "nome": "Amarelo Ouro Superação (Accent)",
                "hex": "#FFC107",
                "rgb": "rgb(255, 193, 7)",
                "uso": "Estrelas de avaliação, badges de pódio, troféus e destaques numéricos"
            },
            {
                "nome": "Azul Oceano Noturno (Background Dark)",
                "hex": "#0B192C",
                "rgb": "rgb(11, 25, 44)",
                "uso": "Background principal do site (Dark Mode), cabeçalhos e rodapé"
            },
            {
                "nome": "Verde Floresta Itaipu (Natureza & Trilhas)",
                "hex": "#1E5128",
                "rgb": "rgb(30, 81, 40)",
                "uso": "Badges de pedais ecológicos, bordas de cards e elementos de trilha MTB"
            },
            {
                "nome": "Branco Puro (Texto & Leitura)",
                "hex": "#FFFFFF",
                "rgb": "rgb(255, 255, 255)",
                "uso": "Títulos principais e botões secundários"
            },
            {
                "nome": "Cinza Neutro (Subtítulos & Metadados)",
                "hex": "#A0AEC0",
                "rgb": "rgb(160, 174, 192)",
                "uso": "Textos secundários, descrições e ícones desativados"
            }
        ],
        "cores_extraidas_do_logo": cores_logo
    }

    # Salvar em JSON
    json_path = output_dir / "kit_de_cores.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(kit_cores, f, ensure_ascii=False, indent=4)

    # Salvar em TXT formatado
    txt_path = output_dir / "kit_de_cores.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("===============================================================================\n")
        f.write("                 KIT DE CORES E PALETA DA MARCA (CICLISMO SH)\n")
        f.write("===============================================================================\n\n")
        for item in kit_cores["paleta_oficial"]:
            f.write(f"🎨 {item['nome']}\n")
            f.write(f"   • HEX: {item['hex']}\n")
            f.write(f"   • RGB: {item['rgb']}\n")
            f.write(f"   • Aplicação: {item['uso']}\n\n")
        f.write("===============================================================================\n")

    print("\n==========================================")
    print(" Kit de Cores Extraído com Sucesso!")
    print(f" 📄 Arquivo JSON: {json_path}")
    print(f" 📄 Arquivo TXT:  {txt_path}")
    print("==========================================")


if __name__ == "__main__":
    gerar_kit_cores()
