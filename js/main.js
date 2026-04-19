document.addEventListener('DOMContentLoaded', () => {

    // navbar ndryshon ngjyre kur scrollon
    const navbar = document.getElementById('main-navbar');

    navbar.classList.add('navbar-dark-initial');

    const handleScroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
            navbar.classList.remove('navbar-dark-initial');
        } else {
            navbar.classList.remove('scrolled');
            navbar.classList.add('navbar-dark-initial');
        }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll();

    // scroll i bute kur klikohet nje link
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');

            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // mbyll menune ne mobile nese eshte hapur
                const offcanvasElement = document.getElementById('offcanvasNavbar');
                if (offcanvasElement && offcanvasElement.classList.contains('show')) {
                    const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement) || new bootstrap.Offcanvas(offcanvasElement);
                    bsOffcanvas.hide();
                }
            }
        });
    });

    // animacion kur elementet shfaqen ne ekran
    const reveals = document.querySelectorAll('.reveal-up');

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const elementVisible = 100;

        reveals.forEach((reveal) => {
            const elementTop = reveal.getBoundingClientRect().top;
            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll();

    // link aktiv ne navbar ndryshon sipas seksionit ku je
    const sections = document.querySelectorAll('header, section');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    const observerOptions = {
        root: null,
        rootMargin: '-30% 0px -50% 0px',
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => link.classList.remove('active'));

                const targetId = entry.target.getAttribute('id');
                const activeLink = document.querySelector(`.navbar-nav .nav-link[href="#${targetId}"]`);

                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));

   

    // harta me leaflet
    const mapElement = document.getElementById('albaniaMap');
    if (mapElement) {
        const map = L.map('albaniaMap').setView([41.1533, 20.1683], 7);

        // stili i hartes nga carto
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        // te dhenat e vendeve ne harte
        const mapPins = [
            { category: 'hiking', coords: [42.3986, 19.7758], title: 'Theth', desc: 'World-class hiking in the Accursed Mountains.' },
            { category: 'hiking', coords: [42.4419, 19.8911], title: 'Valbona', desc: 'Stunning alpine valleys and trails.' },
            { category: 'history', coords: [40.7086, 19.9436], title: 'Berat', desc: 'The city of a thousand windows (UNESCO).' },
            { category: 'history', coords: [40.0758, 20.1388], title: 'Gjirokastër', desc: 'The city of stone with an ancient castle.' },
            { category: 'beaches', coords: [39.7583, 20.0019], title: 'Ksamil', desc: 'Crystal clear waters and sandy beaches.' },
            { category: 'food', coords: [40.2358, 20.3516], title: 'Përmet', desc: 'Famous for thermal baths, slow food, and wine.' },
            { category: 'food', coords: [40.4682, 19.4938], title: 'Vlorë', desc: 'Fresh seafood and coastal wine tours.' },
            { category: 'history', coords: [41.3275, 19.8187], title: 'Tirana', desc: 'Vibrant capital full of history and museums.' },
            { category: 'beaches', coords: [40.159832, 19.599130], title: 'Palase', desc: 'A beautiful coastal village on the Albanian Riviera, known for its crystal-clear Ionian waters, peaceful beaches, and stunning scenery where mountains meet the sea.' },
            { category: 'beaches', coords: [40.1418, 19.6792], title: 'Gjipe', desc: 'A hidden gem between towering cliffs, Gjipe Beach stuns with crystal-clear waters and a breathtaking canyon setting, it offers a peaceful and scenic escape.' }
        ];

        let markers = [];

        const renderMarkers = (category) => {
            // fshij pikat e vjetra
            markers.forEach(marker => map.removeLayer(marker));
            markers = [];

            const filteredPins = category === 'all'
                ? mapPins
                : mapPins.filter(pin => pin.category === category);

            filteredPins.forEach(pin => {
                // ngjyra e pikes sipas kategorise
                let pinColor = '#00A859';
                if (pin.category === 'beaches') pinColor = '#0d6efd';
                if (pin.category === 'history') pinColor = '#fd7e14';
                if (pin.category === 'food') pinColor = '#dc3545';

                const customIcon = L.divIcon({
                    className: 'custom-map-marker',
                    html: `<div style="background-color: ${pinColor}; width: 16px; height: 16px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
                    iconSize: [20, 20],
                    iconAnchor: [10, 10],
                    popupAnchor: [0, -10]
                });

                const marker = L.marker(pin.coords, { icon: customIcon }).addTo(map);
                marker.bindPopup(`<h6>${pin.title}</h6><p class="small">${pin.desc}</p>`);
                markers.push(marker);
            });

            // zoom ne vendet e filtruara
            if (markers.length > 0 && category !== 'all') {
                const group = new L.featureGroup(markers);
                map.fitBounds(group.getBounds().pad(0.5));
            } else if (category === 'all') {
                map.setView([41.1533, 20.1683], 7);
            }
        };

        renderMarkers('all');

        // butonat e filtrimit te hartes
        const activityBtns = document.querySelectorAll('.activity-btn');
        activityBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                activityBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const category = btn.getAttribute('data-category');
                renderMarkers(category);
            });
        });

        // filtrat e guidave
        const filterBtns = document.querySelectorAll('[data-filter]');
        const guideCards = document.querySelectorAll('[data-guide]');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                filterBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const filter = this.dataset.filter;

                guideCards.forEach(card => {
                    const categories = card.dataset.guide;
                    if (filter === 'all' || categories.includes(filter)) {
                        card.style.display = '';
                        card.style.animation = 'fadeIn 0.3s ease';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });

        // fix per harten kur nuk shfaqet sic duhet
        setTimeout(() => { map.invalidateSize(); }, 500);
    }
});