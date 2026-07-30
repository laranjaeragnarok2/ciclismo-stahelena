# 🚴‍♂️ Associação Santa-Helenense de Ciclismo

> **Hub de Rotas GPX, Leaderboard Strava, Calendário de Eventos e App Oficial PWA** da Associação Santa-Helenense de Ciclismo (Santa Helena - PR).

---

## 🎯 Sobre o Projeto

O **Portal & App Ciclismo Santa Helena** é uma plataforma digital moderna e responsiva projetada para centralizar a vida esportiva e turística dos ciclistas da Região Oeste do Paraná (Balneário Terra das Águas, Refúgio Biológico da Itaipu e circuitos rurais).

Desenvolvido como uma **Progressive Web App (PWA)** de alta performance, o projeto funciona tanto no navegador desktop/mobile quanto instalado diretamente na tela inicial do smartphone com suporte offline.

---

## ✨ Principais Funcionalidades

- **🌄 Hero Slider Panorâmico Widescreen**: Carrossel responsivo com momentos marcantes dos passeios, pódios e trilhas locais.
- **📊 Estatísticas da Comunidade**: Contadores animados de quilometragem percorrida, ciclistas ativos, rotas mapeadas e mídias curadas.
- **🗺️ Hub de Rotas Interativo (Leaflet.js)**: Mapa interativo centrado em Santa Helena exibindo trajetos de MTB e Cicloturismo.
- **📥 Exportador de Arquivos GPX**: Gerador dinâmico de arquivos `.gpx` em tempo real para download direto em dispositivos GPS (Garmin, Wahoo, Bryton).
- **📝 Criador Comunitário de Percursos**: Formulário interativo para cadastro de rotas e armazenamento no `localStorage`.
- **🧡 Ranking Strava KOM / QOM**: Tabela de classificação por segmentos locais com rankings e velocidade média dos atletas.
- **📅 Calendário de Eventos & Inscrições**: Grade filtrável de eventos de cicloturismo e MTB com formulário de pré-inscrição integrado ao **WhatsApp**.
- **📸 Galeria de Mídias Curadas (110+ Fotos)**: Acervo fotográfico histórico organizado em 5 categorias (*Pódios*, *Cicloturismo*, *Trilhas MTB*, *Família*, *Cartazes*) com visualizador **Lightbox HD**.
- **📲 Suporte PWA Offline**: Service Worker e Manifesto Webview para experiência de app nativo no celular.

---

## 🎨 Identidade Visual & Design System

A interface utiliza um design moderno baseado em **Glassmorphism**, modo escuro e paleta inspirada na energia do esporte e na natureza de Santa Helena:

- **Laranja Energia (Primary)**: `#FF5722`
- **Amarelo Pódio (Accent)**: `#FFC107`
- **Azul Escuro (Background)**: `#0B192C`
- **Verde Floresta (Trilhas)**: `#1E5128`
- **Laranja Strava**: `#FC4C02`

### Tipografia
- **Títulos e Destaques**: `Outfit` (Google Fonts, Bold / Heavy)
- **Texto de Corpo**: `Inter` (Google Fonts, Regular / Medium)

---

## 📂 Estrutura de Arquivos

```
.
├── index.html             # Estrutura HTML5 semântica e acessível
├── vercel.json           # Configurações de cabeçalhos PWA e rotas
├── manifest.json         # Manifesto PWA do aplicativo
├── sw.js                 # Service Worker (Estratégia de Cache Offline)
├── css/
│   └── style.css         # Design System, Glassmorphism e Responsividade
├── js/
│   └── app.js            # Leaflet Map, Gerador GPX, Slider, Strava & Lightbox
├── assets/
│   ├── logo.jpg          # Emblemática Oficial do Clube
│   └── catalogo_albuns.json # Catálogo dos 5 álbuns curados
├── midias/               # Acervo de 110+ fotografias curadas
└── scripts/              # Automações em Python
```

---

## 📜 Licença & Direitos

© 2026 **Associação Santa-Helenense de Ciclismo**. Todos os direitos reservados.
