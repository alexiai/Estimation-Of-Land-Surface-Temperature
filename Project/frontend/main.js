// Inițializează harta
console.log("Inițializare hartă...");
const map = L.map('map').setView([46.77, 23.59], 13); // Centrat pe Cluj-Napoca

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

console.log("Hartă inițializată.");
let polygon = null;
// Funcție care creează sau actualizează poligonul
function updatePolygon() {
    console.log("Actualizare poligon...");
    const coordinates = [];

    for (let i = 1; i <= 4; i++) {
        const lat = parseFloat(document.getElementById(`lat${i}`).value);
        const lng = parseFloat(document.getElementById(`long${i}`).value);
        if (!isNaN(lat) && !isNaN(lng)) {
            coordinates.push([lat, lng]);
        }
    }
    console.log("Coordonate colectate pentru poligon:", coordinates);
    // Dacă avem toate cele 4 coordonate, desenăm poligonul
    if (coordinates.length === 4) {
        if (polygon) {
            map.removeLayer(polygon); // Șterge poligonul vechi dacă există
        }

        polygon = L.polygon(coordinates, {
            color: 'orange',       // Culoarea conturului
            fillColor: 'orange',   // Culoarea de umplere
            fillOpacity: 0.5,      // Transparența interiorului
            dashArray: '5, 5'      // Hașurare: linii punctate
        }).addTo(map);
        console.log("Poligon desenat.");
    }
}

let activeMarkerIndex = null; // Indexul coordonatei curente selectate pentru modificare
let markers = [null, null, null, null]; // Markerii de pe hartă, inițializați cu null

// Funcție pentru selectarea unei coordonate
function selectCoordinate(index) {
    console.log("Coordonată selectată:", index);
    activeMarkerIndex = index;
}

// Funcție care adaugă sau actualizează un marker pe hartă
function updateMarker(index, lat, lng) {
    console.log(`Actualizare marker la indexul ${index}:`, { lat, lng });
    if (markers[index]) {
        map.removeLayer(markers[index]); // Șterge markerul vechi dacă există
    }
    markers[index] = L.marker([lat, lng]).addTo(map); // Adaugă un marker nou
    map.setView([lat, lng], 13); // Centrează harta pe noul marker
}

// Funcție care verifică și actualizează coordonatele introduse manual
function handleManualInput(index) {
    console.log("Input manual detectat pentru coordonata:", index);
    const latInput = document.getElementById(`lat${index + 1}`);
    const longInput = document.getElementById(`long${index + 1}`);
    const lat = parseFloat(latInput.value);
    const lng = parseFloat(longInput.value);
    console.log("Valori input manual:", { lat, lng });
    if (!isNaN(lat) && !isNaN(lng)) {
        updateMarker(index, lat, lng); // Actualizează markerul pe hartă
        updatePolygon();
    } else if (latInput.value === '' || longInput.value === '') {
        if (markers[index]) {
            map.removeLayer(markers[index]); // Șterge markerul dacă inputul este gol
            markers[index] = null;
        }
        updatePolygon();
    }
}

// Adaugă event listeners pentru inputurile manuale
console.log("Adăugare event listeners pentru inputuri...");
for (let i = 1; i <= 4; i++) {
    document.getElementById(`lat${i}`).addEventListener('input', () => handleManualInput(i - 1));
    document.getElementById(`long${i}`).addEventListener('input', () => handleManualInput(i - 1));
}
console.log("Event listeners pentru inputuri adăugate.");
// Event listener pentru clic pe hartă
map.on('click', (e) => {
    console.log("Harta a fost clicată:", e.latlng);
    if (activeMarkerIndex !== null) {
        const latInput = document.getElementById(`lat${activeMarkerIndex + 1}`);
        const longInput = document.getElementById(`long${activeMarkerIndex + 1}`);

        // Actualizează valorile inputurilor
        latInput.value = e.latlng.lat.toFixed(6);
        longInput.value = e.latlng.lng.toFixed(6);

        // Actualizează markerul pe hartă
        updateMarker(activeMarkerIndex, e.latlng.lat, e.latlng.lng);
        updatePolygon();
    }
});

// Adaugă event listeners pentru pictogramele de pin și stilizează cursorul
for (let i = 1; i <= 4; i++) {
    const pinElement = document.getElementById(`pin${i}`);
    pinElement.style.cursor = 'pointer'; // Schimbă cursorul la pointer
    pinElement.addEventListener('click', () => {
        selectCoordinate(i - 1);
        const latInput = document.getElementById(`lat${i}`);
        const longInput = document.getElementById(`long${i}`);
        const lat = parseFloat(latInput.value);
        const lng = parseFloat(longInput.value);
        if (!isNaN(lat) && !isNaN(lng)) {
            map.setView([lat, lng], 13); // Centrează harta pe coordonatele existente
        }
    });
}

const form = document.getElementById('lst-form');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const lat1 = parseFloat(document.getElementById('lat1').value);
    const long1 = parseFloat(document.getElementById('long1').value);
    const lat2 = parseFloat(document.getElementById('lat2').value);
    const long2 = parseFloat(document.getElementById('long2').value);
    const lat3 = parseFloat(document.getElementById('lat3').value);
    const long3 = parseFloat(document.getElementById('long3').value);
    const lat4 = parseFloat(document.getElementById('lat4').value);
    const long4 = parseFloat(document.getElementById('long4').value);

    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const cloudPercentage = parseFloat(document.getElementById('cloud-percentage').value);

    const requestData = {
        coordinates: [
            [lat1, long1],
            [lat2, long2],
            [lat3, long3],
            [lat4, long4]
        ],
        startDate: startDate,
        endDate: endDate,
        cloudPercentage: cloudPercentage
    };

    console.log("Trimitem cererea către backend cu datele:", requestData);

    try {
        const response = await fetch('http://localhost:5000/run-lst', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (response.ok) {
            const result = await response.json();
            resultDiv.innerHTML = `<h3>Result:</h3><pre>${JSON.stringify(result, null, 2)}</pre>`;

        } else {
            const error = await response.json();
            resultDiv.innerHTML = `<h3>Error:</h3><p>${error.error}</p>`;

        }
    } catch (error) {
        resultDiv.innerHTML = `<h3>Error:</h3><p>${error.error}</p>`;

    }
});
