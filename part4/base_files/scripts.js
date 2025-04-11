document.addEventListener('DOMContentLoaded', () => {
    // Sélection des éléments DOM
    let placeCards = [];
    const tabLinks = document.querySelectorAll('.tab-link');
    const priceFilter = document.getElementById('price-filter');
    const placesList = document.getElementById('places-list');
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    const loginLink = document.getElementById('login-link');

    // Variables d'état
    let activeCategory = 'all';

    // Création du message "Aucun résultat"
    const noResultMsg = document.createElement('p');
    noResultMsg.id = 'no-results';
    noResultMsg.textContent = "Aucun lieu ne correspond aux filtres sélectionnés.";
    noResultMsg.style.display = 'none';
    noResultMsg.style.fontStyle = 'italic';
    placesList.appendChild(noResultMsg);

    // Fonction pour récupérer les cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Vérification de l'authentification et récupération des lieux
    function checkAuthentication() {
        const token = getCookie('token');
        const placeId = getPlaceIdFromURL();

        if (!token) {
            if (loginLink) loginLink.style.display = 'block';
        } else {
            if (loginLink) loginLink.style.display = 'none';

            if (placeId) {
                fetchPlaceDetails(token, placeId);
            } else {
                fetchPlaces(token);
            }
        }
    }

    // Récupération des lieux depuis l'API
    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://localhost:5500/places', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
            } else {
                console.error('Échec lors de la récupération des lieux :', response.statusText);
            }
        } catch (error) {
            console.error('Erreur lors de la récupération des lieux :', error);
        }
    }

    // Affichage des lieux dans la liste
    function displayPlaces(places) {
        places.sort((a, b) => a.price - b.price);

        placesList.innerHTML = ''; // Nettoyer la liste des lieux avant l'ajout

        places.forEach(place => {
            const placeElement = document.createElement('div');
            placeElement.classList.add('place-card');
            placeElement.dataset.price = place.price;
            placeElement.dataset.category = place.category;
            placeElement.dataset.id = place.id; // Ajout de l'ID du lieu
            placeElement.innerHTML = `
                <h3>${place.name}</h3>
                <p>${place.description}</p>
                <p>Prix : ${place.price} €</p>
                <p>Localisation : ${place.location}</p>
                <button class="details-button">Voir les détails</button>
            `;
            placesList.appendChild(placeElement);
        });

        placeCards = document.querySelectorAll('.place-card');

        // Appliquer les filtres initiaux
        applyFilters();

        // Activer les boutons
        activateDetailsButtons();
    }

    // Activer les boutons pour afficher les détails des lieux
    function activateDetailsButtons() {
        const detailsButtons = document.querySelectorAll('.details-button');

        detailsButtons.forEach(button => {
            button.addEventListener('click', () => {
                const placeId = button.closest('.place-card').dataset.id; // Récupérer l'ID du lieu
                window.location.href = `place.html?place_id=${placeId}`; // Redirection vers la page de détails
            });
        });
    }

    // Filtrer et trier les lieux
    const applyFilters = () => {
        const maxPrice = priceFilter.value;
        let anyVisible = false;

        tabLinks.forEach(link => {
            const cat = link.dataset.category || 'all';
            link.classList.toggle('active', cat === activeCategory);
        });

        placeCards.forEach(card => {
            const cardCategory = card.dataset.category;
            const matchesCategory = activeCategory === 'all' || activeCategory === cardCategory;
            const price = parseInt(card.dataset.price, 10);
            const matchesPrice = maxPrice === 'all' || price <= parseInt(maxPrice, 10);

            const shouldDisplay = matchesCategory && matchesPrice;
            card.style.display = shouldDisplay ? 'block' : 'none';
            if (shouldDisplay) anyVisible = true;
        });

        noResultMsg.style.display = anyVisible ? 'none' : 'block';
    };

    // Gestionnaires d'événements
    tabLinks.forEach(link => {
        link.addEventListener('click', () => {
            activeCategory = link.dataset.category || 'all';
            applyFilters();
        });
    });

    priceFilter.addEventListener('change', () => {
        applyFilters();
    });

    // Gestion du formulaire de connexion
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                showError('Veuillez remplir les champs email et mot de passe.');
                return;
            }

            try {
                const response = await fetch('http://localhost:5500/login', {
                    method: "POST",
                    headers: {
                        'Content-Type': "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; Secure; SameSite=Strict`;
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    showError(errorData.message || 'Échec de la connexion. Veuillez vérifier vos identifiants.');
                }
            } catch (error) {
                showError('Une erreur s\'est produite. Veuillez réessayer plus tard.');
                console.error(error);
            }
        });
    }

    // Fonction pour afficher les erreurs de connexion
    function showError(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.color = 'red';
        } else {
            alert(message);
        }
    }

    // Lancer la vérification et les actions nécessaires au chargement de la page
    checkAuthentication();
});

function activateDetailsButtons() {
    const detailsButtons = document.querySelectorAll('.details-button');

    detailsButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Récupérer l'ID du lieu depuis le parent .place-card
            const placeId = button.closest('.place-card').dataset.id;
            
            // Redirection vers la page de détails avec l'ID dans l'URL
            window.location.href = `place.html?place_id=${placeId}`;
        });
    });
}