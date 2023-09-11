document.addEventListener('DOMContentLoaded', function () {
    const dataFromScriptDiv = document.getElementById('receive-from-script');
    const dataForm = document.getElementById('data-form');
    const dataInput = document.getElementById('data-input');

    let refreshInterval = 5000; // Interval par défaut : 5 secondes
    let refreshTimer; // Variable pour stocker l'ID du timer de rafraîchissement
    let isRefreshing = true; // Indicateur pour savoir si le rafraîchissement est actif

    // Fonction pour actualiser les données depuis le script
    function fetchDataFromScript() {
        if (isRefreshing) {
            // Ne fetch les données que si le rafraîchissement est actif
            fetch('http://127.0.0.1:5002/send-data-to-web')
                .then(response => response.json())
                .then(data => {
                    console.log('Data received from the script:', data.data,);
                    // Display received data on the HTML page
                    dataFromScriptDiv.textContent = data.data || 'No data received from the script yet.';
                })
                .catch(error => {
                    console.error('Error fetching data from the script:', error);
                });
        }
    }

    // Fonction pour démarrer le rafraîchissement avec l'intervalle actuel
    function startRefresh() {
        if (!isRefreshing) {
            isRefreshing = true;
            fetchDataFromScript();
            refreshTimer = setInterval(fetchDataFromScript, refreshInterval);
        }
        // Change the color of the "Start Refresh" button
        document.getElementById('start-refresh').style.backgroundColor = 'green';
        document.getElementById('stop-refresh').style.backgroundColor = ''; // Reset color of "Stop Refresh" button
    }

    // Fonction pour arrêter le rafraîchissement
    function stopRefresh() {
        isRefreshing = false;
        clearInterval(refreshTimer);
        // Change the color of the "Stop Refresh" button
        document.getElementById('stop-refresh').style.backgroundColor = 'red';
        document.getElementById('start-refresh').style.backgroundColor = ''; // Reset color of "Start Refresh" button
    }

    // Fonction pour définir le nouvel intervalle de rafraîchissement
    function setRefreshInterval(intervalInSeconds) {
        refreshInterval = intervalInSeconds * 1000; // Convertir en millisecondes
        stopRefresh(); // Arrêter le rafraîchissement actuel
        startRefresh(); // Démarrer le rafraîchissement avec le nouvel intervalle
        // Change the color of the selected interval button
        document.getElementById(`refresh-${intervalInSeconds}`).style.backgroundColor = 'blue';
        // Reset color of other interval buttons
        const intervals = [5, 30, 60];
        intervals.filter(interval => interval !== intervalInSeconds).forEach(interval => {
            document.getElementById(`refresh-${interval}`).style.backgroundColor = '';
        });
    }

    // Gérer le clic sur les boutons
    dataForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        const data = dataInput.value; // Get data from the text input

        // Make a POST request to Flask API to send the data
        fetch('http://127.0.0.1:5001/receive-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: data }) // Send data in JSON format
        })
            .then(response => response.json())
            .then(result => {
                console.log('Response from Flask API:', result);
                dataInput.value = ''; // Clear the text input after sending
            })
            .catch(error => {
                console.error('Error sending data to Flask API:', error);
            });
    });

    // Gérer les boutons de contrôle du rafraîchissement
    document.getElementById('start-refresh').addEventListener('click', startRefresh);
    document.getElementById('stop-refresh').addEventListener('click', stopRefresh);

    // Gérer les boutons pour définir l'intervalle de rafraîchissement
    document.getElementById('refresh-5').addEventListener('click', () => setRefreshInterval(5));
    document.getElementById('refresh-30').addEventListener('click', () => setRefreshInterval(30));
    document.getElementById('refresh-60').addEventListener('click', () => setRefreshInterval(60));

    // Démarrer le rafraîchissement au chargement de la page
    startRefresh();
});
