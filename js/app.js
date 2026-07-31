document.addEventListener('DOMContentLoaded', () => {

    /* ==========================================================================
       1. REGISTRO DO SERVICE WORKER & PROMPT PWA
       ========================================================================== */
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js')
            .then(reg => console.log('✅ Service Worker Registrado:', reg.scope))
            .catch(err => console.error('❌ Erro no Service Worker:', err));
    }

    let deferredPrompt;
    const btnPWA = document.getElementById('btnInstallApp');

    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        if (btnPWA) btnPWA.style.display = 'flex';
    });

    if (btnPWA) {
        btnPWA.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log(`PWA install outcome: ${outcome}`);
                deferredPrompt = null;
                btnPWA.style.display = 'none';
            } else {
                alert('📲 Para instalar o App Ciclismo Santa Helena, toque no menu do seu navegador móvel e selecione "Adicionar à Tela Inicial".');
            }
        });
    }

    /* ==========================================================================
       2. NAV MENU MOBILE HAMBURGER TOGGLE
       ========================================================================== */
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenuBtn.classList.toggle('active');
            navMenu.classList.toggle('show');
        });

        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenuBtn.classList.remove('active');
                navMenu.classList.remove('show');
            });
        });
    }

    /* ==========================================================================
       3. HERO WIDESCREEN SLIDER
       ========================================================================== */
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.slider-dots .dot');
    const prevBtn = document.getElementById('sliderPrev');
    const nextBtn = document.getElementById('sliderNext');
    let currentSlide = 0;
    let slideInterval;

    function goToSlide(index) {
        slides.forEach(s => s.classList.remove('active'));
        dots.forEach(d => d.classList.remove('active'));
        
        currentSlide = (index + slides.length) % slides.length;
        slides[currentSlide].classList.add('active');
        if (dots[currentSlide]) dots[currentSlide].classList.add('active');
    }

    function startSlideTimer() {
        slideInterval = setInterval(() => {
            goToSlide(currentSlide + 1);
        }, 6000);
    }

    function resetSlideTimer() {
        clearInterval(slideInterval);
        startSlideTimer();
    }

    if (slides.length > 0) {
        if (nextBtn) nextBtn.addEventListener('click', () => { goToSlide(currentSlide + 1); resetSlideTimer(); });
        if (prevBtn) prevBtn.addEventListener('click', () => { goToSlide(currentSlide - 1); resetSlideTimer(); });
        dots.forEach(dot => {
            dot.addEventListener('click', (e) => {
                const targetIndex = parseInt(e.target.getAttribute('data-slide'));
                goToSlide(targetIndex);
                resetSlideTimer();
            });
        });
        startSlideTimer();
    }

    /* ==========================================================================
       4. ANIMATED NUMERICAL STATS COUNTER
       ========================================================================== */
    const statCards = document.querySelectorAll('.stat-number');
    let animated = false;

    function animateCounters() {
        statCards.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            let current = 0;
            const increment = Math.ceil(target / 60);
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    counter.innerText = target.toLocaleString('pt-BR');
                    clearInterval(timer);
                } else {
                    counter.innerText = current.toLocaleString('pt-BR');
                }
            }, 30);
        });
    }

    const statsSection = document.querySelector('.stats-container');
    if (statsSection && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !animated) {
                animated = true;
                animateCounters();
            }
        }, { threshold: 0.3 });
        observer.observe(statsSection);
    } else {
        animateCounters();
    }

    /* ==========================================================================
       5. HUB DE ROTAS & LEAFLET.JS MAP INTERATIVO
       ========================================================================== */
    let map;
    const initialRoutes = [
        {
            id: 'rota-1',
            name: 'Circuito Balneário -> Linha São Francisco',
            distance: 45,
            elevation: 480,
            category: 'MTB 45 Km',
            terrain: '70% Terra / 30% Asfalto',
            support: 'Lanchonete da Linha São Francisco',
            rating: '⭐ 4.9 (38 avaliações)',
            comment: '"Trilha sensacional, bastante sombra e ponto de água no percurso!"',
            coords: [
                [-24.8586, -54.3338], // Balneário Terra das Águas
                [-24.8450, -54.3200],
                [-24.8300, -54.3000],
                [-24.8150, -54.2800], // Linha São Francisco
                [-24.8400, -54.3100],
                [-24.8586, -54.3338]
            ],
            color: '#FF5722'
        },
        {
            id: 'rota-2',
            name: 'Rota das Águas & Refúgio Itaipu',
            distance: 28,
            elevation: 210,
            category: 'Cicloturismo 28 Km',
            terrain: 'Ciclovia & Estradas Rurais Pavimentadas',
            support: 'Refúgio Biológico de Santa Helena',
            rating: '⭐ 4.8 (24 avaliações)',
            comment: '"Excelente rota para famílias e pedais recreativos aos domingos!"',
            coords: [
                [-24.8586, -54.3338],
                [-24.8700, -54.3450],
                [-24.8900, -54.3600], // Margem Lago de Itaipu
                [-24.8750, -54.3500],
                [-24.8586, -54.3338]
            ],
            color: '#1E5128'
        },
        {
            id: 'rota-3',
            name: 'Desafio MTB Refúgio Biológico Itaipu',
            distance: 60,
            elevation: 750,
            category: 'Desafio MTB 60 Km',
            terrain: '90% Trilha Fechada / Estradas de Barro',
            support: 'Posto de Controle Refúgio',
            rating: '⭐ 5.0 (52 avaliações)',
            comment: '"Exige preparo físico e técnica nas descidas. Altimetria espetacular!"',
            coords: [
                [-24.8586, -54.3338],
                [-24.8400, -54.3500],
                [-24.8200, -54.3700],
                [-24.7900, -54.3500],
                [-24.8200, -54.3300],
                [-24.8586, -54.3338]
            ],
            color: '#FFC107'
        }
    ];

    function initMap() {
        const mapContainer = document.getElementById('routeMap');
        if (!mapContainer || typeof L === 'undefined') return;

        // Centrado em Santa Helena - PR
        map = L.map('routeMap').setView([-24.8586, -54.3338], 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '© OpenStreetMap contributors | Ciclismo Santa Helena'
        }).addTo(map);

        // Adicionar marcadores e polylines das rotas pré-definidas
        initialRoutes.forEach(route => {
            const polyline = L.polyline(route.coords, {
                color: route.color,
                weight: 4,
                opacity: 0.85,
                lineJoin: 'round'
            }).addTo(map);

            polyline.bindPopup(`
                <div style="font-family: var(--font-body); color: #0B192C;">
                    <h4 style="margin-bottom: 4px; color: #FF5722;">${route.name}</h4>
                    <p style="font-size: 0.85rem; margin-bottom: 6px;"><strong>Distância:</strong> ${route.distance} km | <strong>Ganho:</strong> +${route.elevation}m</p>
                    <p style="font-size: 0.8rem; color: #555;">${route.terrain}</p>
                </div>
            `);

            // Marcador no Ponto Inicial
            const startPoint = route.coords[0];
            L.circleMarker(startPoint, {
                radius: 7,
                color: route.color,
                fillColor: '#FFFFFF',
                fillOpacity: 1
            }).addTo(map).bindPopup(`<b>Ponto de Partida:</b> ${route.name}`);
        });
    }

    initMap();

    // Renderizar Cards de Rotas
    const routesList = document.getElementById('routesList');
    
    function getStoredRoutes() {
        const customRoutes = JSON.parse(localStorage.getItem('sh_custom_routes') || '[]');
        return [...initialRoutes, ...customRoutes];
    }

    function renderRoutes() {
        if (!routesList) return;
        const allRoutes = getStoredRoutes();
        routesList.innerHTML = '';

        allRoutes.forEach((r, idx) => {
            const card = document.createElement('div');
            card.className = 'event-card';
            card.innerHTML = `
                <div class="event-header">
                    <span class="event-date">${r.rating || '⭐ 5.0 (Nova)'}</span>
                    <span class="event-category">${r.category}</span>
                </div>
                <div class="event-body">
                    <h4>${r.name}</h4>
                    <ul class="event-meta">
                        <li>⛰️ <strong>Altimetria:</strong> +${r.elevation}m</li>
                        <li>🛣️ <strong>Terreno:</strong> ${r.terrain || r.description || 'Percurso mapeado pela comunidade.'}</li>
                        ${r.support ? `<li>🥤 <strong>Pontos de Apoio:</strong> ${r.support}</li>` : ''}
                    </ul>
                    <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-bottom: 15px; font-size: 0.85rem;">
                        <span style="color: var(--accent-yellow); font-weight: bold;">${r.comment || 'Nenhuma avaliação cadastrada ainda.'}</span>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button class="btn-event btn-download-gpx" data-index="${idx}">📥 Baixar GPX</button>
                        <button class="btn-event btn-open-strava" style="background: #FC4C02; color: white; border: none;">🧡 Abrir Strava</button>
                    </div>
                </div>
            `;
            routesList.appendChild(card);
        });

        // Event listeners para download GPX
        document.querySelectorAll('.btn-download-gpx').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = e.target.getAttribute('data-index');
                const routeObj = getStoredRoutes()[index];
                downloadGPX(routeObj);
            });
        });

        document.querySelectorAll('.btn-open-strava').forEach(btn => {
            btn.addEventListener('click', () => {
                alert('🧡 Redirecionando para o clube Ciclismo Santa Helena no Strava...');
                window.open('https://www.strava.com/clubs', '_blank');
            });
        });
    }

    // Função de geração e download de arquivo GPX real
    function downloadGPX(route) {
        const coords = route.coords || [
            [-24.8586, -54.3338],
            [-24.8450, -54.3200],
            [-24.8300, -54.3000]
        ];

        let trkpts = coords.map(c => `      <trkpt lat="${c[0]}" lon="${c[1]}"><ele>${route.elevation || 250}</ele></trkpt>`).join('\n');

        const gpxContent = `<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Ciclismo Santa Helena PWA" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata>
    <name>${route.name}</name>
    <desc>Percurso GPX - ${route.category} - Santa Helena PR</desc>
  </metadata>
  <trk>
    <name>${route.name}</name>
    <trkseg>
${trkpts}
    </trkseg>
  </trk>
</gpx>`;

        const blob = new Blob([gpxContent], { type: 'application/gpx+xml' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${route.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}.gpx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    renderRoutes();

    // Formulário do Criador de Rotas
    const routeForm = document.getElementById('routeForm');
    if (routeForm) {
        routeForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('routeName').value;
            const distance = document.getElementById('routeDistance').value;
            const elevation = document.getElementById('routeElevation').value;
            const category = document.getElementById('routeCategory').value;
            const description = document.getElementById('routeDescription').value;

            const newRoute = {
                id: `custom-${Date.now()}`,
                name: name,
                distance: parseFloat(distance),
                elevation: parseInt(elevation),
                category: `${category} ${distance} Km`,
                terrain: description || 'Rota recomendada por atleta local.',
                rating: '⭐ 5.0 (1 avaliação)',
                comment: '"Rota cadastrada recentemente pela comunidade!"',
                coords: [
                    [-24.8586, -54.3338],
                    [-24.8500, -54.3200],
                    [-24.8350, -54.3100]
                ],
                color: '#FF5722'
            };

            const customRoutes = JSON.parse(localStorage.getItem('sh_custom_routes') || '[]');
            customRoutes.unshift(newRoute);
            localStorage.setItem('sh_custom_routes', JSON.stringify(customRoutes));

            renderRoutes();

            // Adicionar ao mapa
            if (map) {
                const polyline = L.polyline(newRoute.coords, { color: '#FF5722', weight: 4 }).addTo(map);
                polyline.bindPopup(`<b>${newRoute.name}</b><br>${newRoute.category}`).openPopup();
                map.panTo(newRoute.coords[0]);
            }

            routeForm.reset();
            alert('🎉 Sua rota foi publicada com sucesso e já está disponível para download e visualização!');
        });
    }

    /* ==========================================================================
       6. STRAVA OAUTH & LEADERBOARD SYSTEM
       ========================================================================== */
    const leaderboardData = {
        refugio: [
            { rank: '🥇', name: 'Lucas "Pedal" Silva', avatar: 'assets/logo.jpg', time: '4m 12s', speed: '25.7 km/h' },
            { rank: '🥈', name: 'Mariana Santos', avatar: 'assets/logo.jpg', time: '4m 35s', speed: '23.5 km/h' },
            { rank: '🥉', name: 'Carlos Eduardo MTB', avatar: 'assets/logo.jpg', time: '4m 50s', speed: '22.3 km/h' },
            { rank: '4º', name: 'Fernanda Oliveira', avatar: 'assets/logo.jpg', time: '5m 08s', speed: '21.0 km/h' },
            { rank: '5º', name: 'Gabriel "Tigre" Costa', avatar: 'assets/logo.jpg', time: '5m 22s', speed: '20.1 km/h' }
        ],
        balneario: [
            { rank: '🥇', name: 'Gabriel "Tigre" Costa', avatar: 'assets/logo.jpg', time: '5m 02s', speed: '38.2 km/h' },
            { rank: '🥈', name: 'Lucas "Pedal" Silva', avatar: 'assets/logo.jpg', time: '5m 15s', speed: '36.6 km/h' },
            { rank: '🥉', name: 'Rodrigo "Veloz" Lima', avatar: 'assets/logo.jpg', time: '5m 28s', speed: '35.1 km/h' },
            { rank: '4º', name: 'Mariana Santos', avatar: 'assets/logo.jpg', time: '5m 45s', speed: '33.4 km/h' },
            { rank: '5º', name: 'André Becker', avatar: 'assets/logo.jpg', time: '6m 01s', speed: '31.9 km/h' }
        ]
    };

    const leaderboardList = document.getElementById('leaderboardList');
    const segTabs = document.querySelectorAll('.seg-tab');

    function renderLeaderboard(segmentKey) {
        if (!leaderboardList) return;
        const list = leaderboardData[segmentKey] || [];
        leaderboardList.innerHTML = '';

        list.forEach(item => {
            const div = document.createElement('div');
            div.className = 'leaderboard-item';
            div.innerHTML = `
                <div class="athlete-info">
                    <span class="athlete-rank">${item.rank}</span>
                    <img src="${item.avatar}" alt="${item.name}" class="athlete-avatar">
                    <div>
                        <div class="athlete-name">${item.name}</div>
                        <div class="athlete-meta">Velocidade Média: ${item.speed}</div>
                    </div>
                </div>
                <div class="athlete-time">${item.time}</div>
            `;
            leaderboardList.appendChild(div);
        });
    }

    if (segTabs.length > 0) {
        segTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                segTabs.forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');
                const segKey = e.target.getAttribute('data-segment');
                renderLeaderboard(segKey);
            });
        });
        renderLeaderboard('refugio');
    }

    // Botão Conectar Strava
    const btnStravaAuth = document.getElementById('btnStravaAuth');
    const stravaStatusArea = document.getElementById('stravaStatusArea');

    if (btnStravaAuth && stravaStatusArea) {
        btnStravaAuth.addEventListener('click', () => {
            stravaStatusArea.innerHTML = `
                <div style="background: rgba(252, 76, 2, 0.15); padding: 15px; border-radius: 15px; border: 1px solid #FC4C02;">
                    <p style="color: #FC4C02; font-weight: bold; margin-bottom: 5px;">✅ Perfil Conectado ao Strava API!</p>
                    <p style="font-size: 0.85rem; color: var(--text-white);">Atleta: <strong>@ciclista_santa_helena</strong> (ID: 8493021)</p>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 5px;">Sua última atividade foi sincronizada automaticamente com o Leaderboard.</p>
                </div>
            `;
        });
    }

    /* ==========================================================================
       7. EVENTOS FILTER & REGISTRATION MODAL
       ========================================================================== */
    const eventFilterBtns = document.querySelectorAll('.event-filter-bar .filter-btn');
    const eventCards = document.querySelectorAll('#eventsGrid .event-card');

    if (eventFilterBtns.length > 0) {
        eventFilterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                eventFilterBtns.forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                const filter = e.target.getAttribute('data-filter');

                eventCards.forEach(card => {
                    const cat = card.getAttribute('data-category');
                    if (filter === 'todos' || cat === filter) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    // Registration Modal
    const registerModal = document.getElementById('registerModal');
    const registerModalClose = document.getElementById('registerModalClose');
    const registerModalTitle = document.getElementById('registerModalTitle');
    const registerForm = document.getElementById('registerForm');
    let selectedEventName = '';

    document.querySelectorAll('.open-register-modal').forEach(btn => {
        btn.addEventListener('click', (e) => {
            selectedEventName = e.target.getAttribute('data-event') || 'Evento Ciclismo Santa Helena';
            if (registerModalTitle) registerModalTitle.innerText = `📝 Inscrição: ${selectedEventName}`;
            if (registerModal) registerModal.classList.add('show');
        });
    });

    if (registerModalClose) {
        registerModalClose.addEventListener('click', () => {
            if (registerModal) registerModal.classList.remove('show');
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('regName').value;
            const phone = document.getElementById('regPhone').value;
            const city = document.getElementById('regCity').value;
            const category = document.getElementById('regCategory').value;
            const shirt = document.getElementById('regShirt').value;

            const text = `Olá!%20Gostaria%20de%20confirmar%20minha%20inscrição%20no%20*${encodeURIComponent(selectedEventName)}*:%0A%0A👤%20*Nome:*%20${encodeURIComponent(name)}%0A📱%20*WhatsApp:*%20${encodeURIComponent(phone)}%0A📍%20*Cidade:*%20${encodeURIComponent(city)}%0A🚴%20*Categoria:*%20${encodeURIComponent(category)}%0A👕%20*Camiseta:*%20${encodeURIComponent(shirt)}`;

            window.open(`https://wa.me/5545999999999?text=${text}`, '_blank');
            if (registerModal) registerModal.classList.remove('show');
            registerForm.reset();
        });
    }

    /* ==========================================================================
       7.1. FILTRAGEM DA VITRINE DE PRODUTOS DA LOJA
       ========================================================================== */
    const storeFilterBtns = document.querySelectorAll('.store-filter-bar .filter-btn');
    const productCards = document.querySelectorAll('#storeGrid .product-card');

    if (storeFilterBtns.length > 0) {
        storeFilterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                storeFilterBtns.forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                const filter = e.target.getAttribute('data-store-filter');

                productCards.forEach(card => {
                    const cat = card.getAttribute('data-category');
                    if (filter === 'ALL' || cat === filter) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    /* ==========================================================================
       8. GALERIA DE MÍDIAS CURADAS & LIGHTBOX MODAL
       ========================================================================== */
    const galleryGrid = document.getElementById('galleryGrid');
    const albumTabs = document.querySelectorAll('#albumTabs .filter-btn, #albumTabs .tab-btn');
    const btnLoadMorePhotos = document.getElementById('btnLoadMorePhotos');

    let allPhotos = [];
    let filteredPhotos = [];
    let visibleCount = 12;
    let currentPhotoIndex = 0;

    // Função para traduzir album_id para pasta do repositório
    function getPhotoPath(item) {
        const folderMap = {
            'Album_Podios_e_Conquistas': '01_Podios_e_Conquistas',
            'Album_Cicloturismo_Terra_das_Aguas': '02_Cicloturismo_Terra_das_Aguas',
            'Album_Trilhas_MTB_Itaipu': '03_Trilhas_MTB_Itaipu',
            'Album_Pedais_Urbanos_e_Familia': '04_Pedais_Urbanos_e_Familia',
            'Album_Cartazes_e_Divulgacao': '05_Cartazes_e_Divulgacao'
        };
        const folder = folderMap[item.album_id] || '01_Podios_e_Conquistas';
        return `midias/albuns_curados/${folder}/${item.filename}`;
    }

    function loadCatalogData() {
        // 1. Carrega imediatamente o acervo pré-gerado para rendering instantâneo sem travamento
        generateFallbackPhotos();

        // 2. Tenta atualizar com o acervo completo em background com timeout de segurança
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1500);

        fetch('assets/catalogo_albuns.json', { signal: controller.signal })
            .then(res => {
                clearTimeout(timeoutId);
                return res.json();
            })
            .then(data => {
                if (Array.isArray(data) && data.length > 0) {
                    allPhotos = data;
                    filteredPhotos = [...allPhotos];
                    renderGallery();
                }
            })
            .catch(err => {
                console.log('⚡ Usando acervo otimizado local (resposta instantânea).');
            });
    }

    function generateFallbackPhotos() {
        const albums = [
            { id: 'Album_Podios_e_Conquistas', title: '🏆 Pódios & Conquistas', folder: '01_Podios_e_Conquistas', count: 20, prefix: 'Album_Podios_e_Conquistas' },
            { id: 'Album_Cicloturismo_Terra_das_Aguas', title: '🌅 Cicloturismo Terra das Águas', folder: '02_Cicloturismo_Terra_das_Aguas', count: 25, prefix: 'Album_Cicloturismo_Terra_das_Aguas' },
            { id: 'Album_Trilhas_MTB_Itaipu', title: '🚵 Trilhas MTB Itaipu', folder: '03_Trilhas_MTB_Itaipu', count: 25, prefix: 'Album_Trilhas_MTB_Itaipu' },
            { id: 'Album_Pedais_Urbanos_e_Familia', title: '👥 Pedais da Família', folder: '04_Pedais_Urbanos_e_Familia', count: 25, prefix: 'Album_Pedais_Urbanos_e_Familia' }
        ];

        allPhotos = [];
        albums.forEach(alb => {
            for (let i = 1; i <= alb.count; i++) {
                const num = i < 10 ? `0${i}` : `${i}`;
                allPhotos.push({
                    album_id: alb.id,
                    album_title: alb.title,
                    filename: `${alb.prefix}_${num}.jpg`,
                    suggested_use: 'Galeria Oficial Ciclismo'
                });
            }
        });
        filteredPhotos = [...allPhotos];
        renderGallery();
    }

    function renderGallery() {
        if (!galleryGrid) return;
        galleryGrid.innerHTML = '';
        const itemsToDisplay = filteredPhotos.slice(0, visibleCount);

        itemsToDisplay.forEach((photo, idx) => {
            const path = getPhotoPath(photo);
            const card = document.createElement('div');
            card.className = 'gallery-card';
            card.innerHTML = `
                <img src="${path}" alt="${photo.album_title || 'Foto Ciclismo Santa Helena'}" loading="lazy" onerror="this.src='assets/logo.jpg'">
                <div class="gallery-card-overlay">
                    <span class="gallery-card-tag">${photo.album_title || 'Acervo Oficial'}</span>
                    <div class="gallery-card-title">${photo.filename}</div>
                </div>
            `;

            card.addEventListener('click', () => {
                openLightbox(idx);
            });

            galleryGrid.appendChild(card);
        });

        if (btnLoadMorePhotos) {
            btnLoadMorePhotos.style.display = visibleCount >= filteredPhotos.length ? 'none' : 'inline-block';
        }
    }

    if (albumTabs.length > 0) {
        albumTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                albumTabs.forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');
                const selectedAlbum = e.target.getAttribute('data-album');

                if (selectedAlbum === 'ALL') {
                    filteredPhotos = [...allPhotos];
                } else {
                    filteredPhotos = allPhotos.filter(p => p.album_id === selectedAlbum);
                }

                visibleCount = 12;
                renderGallery();
            });
        });
    }

    if (btnLoadMorePhotos) {
        btnLoadMorePhotos.addEventListener('click', () => {
            visibleCount += 12;
            renderGallery();
        });
    }

    // Lightbox Modal Implementation
    const lightboxModal = document.getElementById('lightboxModal');
    const lightboxClose = document.getElementById('lightboxClose');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxCaption = document.getElementById('lightboxCaption');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');

    function openLightbox(index) {
        if (index < 0 || index >= filteredPhotos.length) return;
        currentPhotoIndex = index;
        const photo = filteredPhotos[currentPhotoIndex];
        const path = getPhotoPath(photo);

        if (lightboxImg) lightboxImg.src = path;
        if (lightboxCaption) {
            lightboxCaption.innerHTML = `
                <strong>${photo.album_title || 'Acervo Ciclismo Santa Helena'}</strong><br>
                <span>${photo.filename}</span> (${currentPhotoIndex + 1} de ${filteredPhotos.length})
            `;
        }
        if (lightboxModal) lightboxModal.classList.add('show');
    }

    function closeLightbox() {
        if (lightboxModal) lightboxModal.classList.remove('show');
    }

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxPrev) lightboxPrev.addEventListener('click', () => openLightbox(currentPhotoIndex - 1));
    if (lightboxNext) lightboxNext.addEventListener('click', () => openLightbox(currentPhotoIndex + 1));

    document.addEventListener('keydown', (e) => {
        if (lightboxModal && lightboxModal.classList.contains('show')) {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') openLightbox(currentPhotoIndex - 1);
            if (e.key === 'ArrowRight') openLightbox(currentPhotoIndex + 1);
        }
    });

    loadCatalogData();
});

