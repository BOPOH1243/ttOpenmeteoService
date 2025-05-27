const input = document.getElementById('city-input');
const suggestions = document.getElementById('suggestions');
const forecast = document.getElementById('forecast');

// Проверяем, есть ли сохранённый город в localStorage
const savedCity = JSON.parse(localStorage.getItem('lastCity'));
if (savedCity) {
  input.value = savedCity.name;
  fetchWeather(savedCity.latitude, savedCity.longitude, savedCity.name);
}

let debounceTimer;

input.addEventListener('input', () => {
  const query = input.value.trim();
  if (query.length < 3) {
    suggestions.innerHTML = '';
    return;
  }

  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=5&language=ru&format=json`)
      .then(response => response.json())
      .then(data => {
        suggestions.innerHTML = '';
        if (data.results) {
          data.results.forEach(place => {
            const li = document.createElement('li');
            li.textContent = `${place.name}, ${place.country}`;
            li.dataset.lat = place.latitude;
            li.dataset.lon = place.longitude;
            suggestions.appendChild(li);
          });
        }
      })
      .catch(error => {
        console.error('Ошибка при получении подсказок:', error);
      });
  }, 300);
});

suggestions.addEventListener('click', (event) => {
  if (event.target.tagName === 'LI') {
    const lat = event.target.dataset.lat;
    const lon = event.target.dataset.lon;
    const cityName = event.target.textContent;
    input.value = cityName;
    suggestions.innerHTML = '';
    fetchWeather(lat, lon, cityName);
  }
});

function fetchWeather(lat, lon, cityName) {
  fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m`)
    .then(response => response.json())
    .then(data => {
      const current = data.current;
      forecast.innerHTML = `
        <h2>Текущая погода в ${cityName}</h2>
        <p><strong>Температура:</strong> ${current.temperature_2m} °C</p>
        <p><strong>Скорость ветра:</strong> ${current.wind_speed_10m} км/ч</p>
      `;
      localStorage.setItem('lastCity', JSON.stringify({
        name: cityName,
        latitude: lat,
        longitude: lon
      }));
      fetch('/notify_backend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city_name: cityName })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Ошибка при отправке данных на /notify_backend');
          }
          return response.json();
        })
        .then(data => {
          console.log('Уведомление успешно отправлено:', data);
        })
        .catch(error => {
          console.error('Ошибка при отправке уведомления:', error);
        });
    })
    .catch(error => {
      console.error('Ошибка при получении прогноза погоды:', error);
      forecast.innerHTML = '<p>Не удалось загрузить данные о погоде.</p>';
    });
}

