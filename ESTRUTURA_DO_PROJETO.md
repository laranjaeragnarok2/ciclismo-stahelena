# 📂 Estrutura do Projeto Ciclismo Santa Helena

Este arquivo descreve a organização unificada dos diretórios, mídias, códigos e documentação do projeto **Ciclismo Santa Helena**.

---

## 🌳 Árvore de Diretórios

```
/home/horyu/Projetos/ciclismo/
│
├── 📄 index.html                             # Portal Principal (Hero Slider, Eventos, Leaflet Map, Strava, Galeria)
├── 📄 manifest.json                          # PWA / Webview App Manifest
├── 📄 sw.js                                  # Service Worker (Suporte Offline PWA)
├── 📄 vercel.json                            # Configuração de Deploy Vercel (PWA Headers & Clean URLs)
├── 📄 PLANO_DE_DESENVOLVIMENTO_BLUEPRINT.md  # Arquitetura, Sprints e Especificações do Projeto
├── 📄 ESTRUTURA_DO_PROJETO.md                # Este documento de referência
├── 📄 README.md                              # Guia de início do projeto
│
├── 🎨 css/
│   └── style.css                          # Design System (Glassmorphism, Dark Mode, Responsive Tokens)
├── ⚡ js/
│   └── app.js                             # Lógica do Criador de Rotas, Leaflet.js, Strava API, PWA e Lightbox
├── 📦 assets/
│   ├── logo.jpg                           # Logo oficial em alta resolução
│   └── catalogo_albuns.json               # Catálogo JSON dos álbuns curados
│
├── 🖼️ midias/                                 # Mídias Raspadas, Organizadas e Curadas
│   ├── manual_da_marca.txt                    # Guia de Cores (HEX/RGB), Tipografia e Tom de Voz
│   ├── logo/
│   │   └── logo_ciclismo_santa_helena.jpg     # Logo emblemática oficial
│   └── albuns_curados/                        # 110 Fotos Selecionadas (Destaques para o Site)
│       ├── 01_Podios_e_Conquistas/
│       ├── 02_Cicloturismo_Terra_das_Aguas/
│       ├── 03_Trilhas_MTB_Itaipu/
│       ├── 04_Pedais_Urbanos_e_Familia/
│       └── 05_Cartazes_e_Divulgacao/
│
└── 🛠️ scripts/                               # Automações e Scrapers em Python
```

---

## 💡 Como utilizar este projeto no Antigravity IDE:

1. Abra a pasta `app/` no **Antigravity IDE** para trabalhar no código-fonte da aplicação.
2. Consulte o arquivo [`PLANO_DE_DESENVOLVIMENTO_BLUEPRINT.md`](file:///home/horyu/Projetos/ciclismo/PLANO_DE_DESENVOLVIMENTO_BLUEPRINT.md) para seguir a ordem das Sprints de desenvolvimento.
3. Utilize as mídias curadas contidas em `midias/albuns_curados/` e o catálogo em `app/assets/catalogo_albuns.json` para renderizar as galerias e banners no site.
