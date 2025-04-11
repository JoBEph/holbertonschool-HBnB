document.addEventListener('DOMContentLoaded', () => {
    // Select DOM elements
    let placeCards = [];
    const tabLinks = document.querySelectorAll('.tab-link');
    const priceFilter = document.getElementById('price-filter');
    const placesList = document.getElementById('places-list');
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    const loginLink = document.getElementById('login-link');

    // State variables
    let activeCategory = 'all';

    // Create "No results" message
    const noResultMsg = document.createElement('p');
    noResultMsg.id = 'no-results';
    noResultMsg.textContent = "No places match the selected filters.";
    noResultMsg.style.display = 'none';
    noResultMsg.style.fontStyle = 'italic';
    placesList.appendChild(noResultMsg);

    // Function to get a cookie value
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Check authentication and fetch places
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

    // Fetch places from API
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
                console.error('Failed to fetch places:', response.statusText);
            }
        } catch (error) {
            console.error('Error while fetching places:', error);
        }
    }

    // Display places in the list
    function displayPlaces(places) {
        places.sort((a, b) => a.price - b.price);

        placesList.innerHTML = ''; // Clear existing list

        places.forEach(place => {
            const placeElement = document.createElement('div');
            placeElement.classList.add('place-card');
            placeElement.dataset.price = place.price;
            placeElement.dataset.category = place.category;
            placeElement.dataset.id = place.id;
            placeElement.innerHTML = `
                <h3>${place.name}</h3>
                <p>${place.description}</p>
                <p>Price: ${place.price} €</p>
                <p>Location: ${place.location}</p>
                <button class="details-button">View Details</button>
            `;
            placesList.appendChild(placeElement);
        });

        placeCards = document.querySelectorAll('.place-card');

        // Apply initial filters
        applyFilters();

        // Enable detail buttons
        activateDetailsButtons();
    }

    // Enable buttons to view place details
    function activateDetailsButtons() {
        const detailsButtons = document.querySelectorAll('.details-button');

        detailsButtons.forEach(button => {
            button.addEventListener('click', () => {
                const placeId = button.closest('.place-card').dataset.id;
                window.location.href = `place.html?place_id=${placeId}`;
            });
        });
    }

    // Apply category and price filters
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

    // Tab link filter events
    tabLinks.forEach(link => {
        link.addEventListener('click', () => {
            activeCategory = link.dataset.category || 'all';
            applyFilters();
        });
    });

    priceFilter.addEventListener('change', () => {
        applyFilters();
    });

    // Login form handler
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                showError('Please fill in both email and password fields.');
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
                    showError(errorData.message || 'Login failed. Please check your credentials.');
                }
            } catch (error) {
                showError('An error occurred. Please try again later.');
                console.error(error);
            }
        });
    }

    // Show login error message
    function showError(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.color = 'red';
        } else {
            alert(message);
        }
    }

    // Initialize logic on page load
    checkAuthentication();
});

// Enable "View Details" button events
function activateDetailsButtons() {
    const detailsButtons = document.querySelectorAll('.details-button');

    detailsButtons.forEach(button => {
        button.addEventListener('click', () => {
            const placeId = button.closest('.place-card').dataset.id;
            window.location.href = `place.html?place_id=${placeId}`;
        });
    });
}

// Extract place ID from URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

// Check token for review page
const token = getCookie('token');
if (!token) {
    window.location.href = 'index.html'; // Redirect if not authenticated
    return;
}

const reviewForm = document.getElementById('review-form');
if (reviewForm) {
    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const reviewText = document.getElementById('review').value.trim();
        const rating = document.querySelector('input[name="rating"]:checked')?.value;

        if (!reviewText || !rating) {
            alert("Please write a review and select a rating.");
            return;
        }

        try {
            const response = await fetch('http://localhost:5001/api/v1/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    place_id: placeId,
                    text: reviewText,
                    rating: parseInt(rating, 10)
                })
            });

            if (response.ok) {
                alert("Review submitted successfully!");
                reviewForm.reset();
            } else {
                const errorData = await response.json();
                alert("Error: " + (errorData.error || "Unable to submit the review."));
            }

        } catch (error) {
            console.error('Error submitting review:', error);
            alert("An error occurred. Please try again.");
        }
    });
}
