const apiBaseUrl = "loveoffootball.io"; // Your Flask app's base URL
const apiEndpoint = "/proxy"; // Your Flask app's proxy route
const apiUrl =
  "http://api.sportradar.us/nfl/official/trial/v7/en/games/current_season/schedule.json";
const  apiKey = os.getenv('APIKEY')
const fullApiUrl = `${apiUrl}?api_key=${apiKey}`;

// Encode the full API URL
const encodedApiUrl = encodeURIComponent(fullApiUrl);
// Construct the proxy URL
const proxyUrl = `${apiBaseUrl}${apiEndpoint}?url=${encodedApiUrl}`;
//console.log('Proxy URL:', proxyUrl);

//fetch(fullApiUrl)
//    .then(response => response.json())
//    .then(data => {
//        console.log('API Data:', data);
//        // Handle the response data
//    })
//    .catch(error => {
//        console.error('Fetch Error:', error);
//    });

// Function to group games by day
function groupGamesByDay(games) {
  // Implement your grouping logic here
  // Return an object where keys are dates and values are arrays of games
}

// Function to render game days and games
function renderGameDays(gamesByDay) {
  const gameDaysContainer = document.querySelector(".game-days");

  for (const date in gamesByDay) {
    const games = gamesByDay[date];
    const gameDayContainer = document.createElement("div");
    gameDayContainer.classList.add("game-day");

    const dateHeader = document.createElement("h3");
    dateHeader.textContent = date;
    gameDayContainer.appendChild(dateHeader);

    for (const game of games) {
      const gameElement = document.createElement("div");
      gameElement.textContent = `${game.homeTeam} vs ${game.awayTeam}`;
      gameDayContainer.appendChild(gameElement);
    }

    gameDaysContainer.appendChild(gameDayContainer);
  }
}
