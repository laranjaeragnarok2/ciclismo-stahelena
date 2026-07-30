#!/usr/bin/env bash
# Script mestre de extração de mídias de Ciclismo Santa Helena (Facebook e Instagram)
# Organiza fotos em pastas dedicadas respeitando os limites sem login.

BASE_DIR="/home/horyu/Projetos/ciclismo_santa_helena_midias"
PYTHON_BIN="/home/horyu/.venv_instaloader/bin/python"
GALLERY_DL="/home/horyu/.venv_instaloader/bin/gallery-dl"

echo "=========================================================="
echo "      EXTRAÇÃO DE MÍDIAS - CICLISMO SANTA HELENA"
echo "=========================================================="
echo "Pasta Principal: $BASE_DIR"
echo ""

mkdir -p "$BASE_DIR/facebook_fotos"
mkdir -p "$BASE_DIR/instagram_fotos"

# 1. Facebook Photos
echo "[1/2] Baixando fotos do Facebook (https://www.facebook.com/ciclismosantahelena/photos)..."
$GALLERY_DL --directory "$BASE_DIR/facebook_fotos" "https://www.facebook.com/ciclismosantahelena/photos"

echo ""
# 2. Instagram Photos (Apenas Fotos Únicas, sem vídeos e sem carrosséis)
echo "[2/2] Extraindo APENAS fotos únicas do Instagram sem login (respeitando limites e delays)..."
$PYTHON_BIN /home/horyu/Projetos/instagram_scraper/instagram_photos_only.py --output-dir "$BASE_DIR/instagram_fotos"

echo ""
echo "=========================================================="
echo " Processo finalizado!"
echo " Pasta das fotos do Facebook: $BASE_DIR/facebook_fotos"
echo " Pasta das fotos do Instagram: $BASE_DIR/instagram_fotos"
echo "=========================================================="
