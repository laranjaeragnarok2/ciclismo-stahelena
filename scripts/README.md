# Ferramenta de Extração Completa do Instagram

Este projeto foi preparado especificamente para extrair **todo o conteúdo** do perfil [@ciclismosantahelena](https://www.instagram.com/ciclismosantahelena/) (ou qualquer outro perfil público/privado que você tenha acesso).

## 🚀 O que este script extrai:
1. **Mídias completas**: Fotos em alta resolução, vídeos, reels e carrosséis.
2. **Legendas**: Arquivos de texto contendo o texto exato de cada publicação.
3. **Metadados em JSON e CSV**: Data UTC, curtidas, comentários, localização, URLs originais e caminhos dos arquivos baixados.
4. **Informações do Perfil**: Foto de perfil, bio, contadores de seguidores/seguindo e total de posts.

---

## 🛠️ Como Executar

O ambiente virtual Python foi criado e pré-configurado em `/home/horyu/.venv_instaloader`.

### 1. Extração Direta (Sem Login)
> *Nota: O Instagram limita requisições sem autenticação (erro HTTP 429). Se o Instagram solicitar login, use a opção 2.*

```bash
/home/horyu/.venv_instaloader/bin/python /home/horyu/Projetos/instagram_scraper/scraper.py
```

---

### 2. Extração Com Login (Recomendado para Perfis Grandes ou Evitar Bloqueios)
Para evitar que o Instagram bloqueie as requisições por IP não autenticado:

```bash
/home/horyu/.venv_instaloader/bin/python /home/horyu/Projetos/instagram_scraper/scraper.py --login SEU_USUARIO_INSTAGRAM
```
*O script solicitará sua senha de forma segura no terminal.*

---

### 3. Opções Avançadas

* **Baixar apenas um número específico de posts (ex: últimos 20 posts):**
  ```bash
  /home/horyu/.venv_instaloader/bin/python /home/horyu/Projetos/instagram_scraper/scraper.py --max-posts 20
  ```

* **Atualização rápida (baixa apenas posts novos):**
  ```bash
  /home/horyu/.venv_instaloader/bin/python /home/horyu/Projetos/instagram_scraper/scraper.py --fast-update
  ```

* **Definir pasta personalizada de destino:**
  ```bash
  /home/horyu/.venv_instaloader/bin/python /home/horyu/Projetos/instagram_scraper/scraper.py --output-dir /caminho/da/pasta
  ```

---

## 📁 Estrutura dos Arquivos Baixados

Após a execução, os arquivos serão salvos na pasta `downloads_ciclismosantahelena`:

* `perfil_info.json` (Dados do perfil)
* `relatorio_posts.json` (Resumo geral de todos os posts)
* `relatorio_posts.csv` (Planilha CSV pronta para Excel / Google Sheets)
* `[shortcode]/` (Subpasta para cada postagem contendo fotos, vídeo .mp4, legenda .txt e .json individual)
