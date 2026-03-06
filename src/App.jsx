import { useState } from "react";

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState("");

  const getWeather = async () => {
    setError("");
    setWeather(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/weather?city=${city}`
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.error);
      } else {
        setWeather(data);
      }
    } catch (err) {
      setError("Server not running");
    }
  };

  return (
    <div
      style={{
        width: "100%",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        boxSizing: "border-box",
      }}
    >
      <h1>Weather Search</h1>

      <input
        type="text"
        placeholder="Enter a city"
        value={city}
        onChange={(e) => setCity(e.target.value)}
      />

      <button onClick={getWeather}>Search</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {weather && (
        <div>
          <p>Temperature: {weather.temperature}°C</p>
          <p>Temperature: {Math.round(weather.temperature * 1.8 + 32)}°F</p>
          <p>Wind Speed: {weather.wind_speed} km/h</p>
          <p>Precipitation: {weather.precipitation} inches</p>
          <p>Relative Humidity: {weather.relative_humidity} %</p>
          <p>Wind Gusts: {weather.wind_gusts} knots</p>
          <p>Pressure MSL: {weather.pressure_msl} hPa</p>
          <p>Cloud Cover: {weather.cloud_cover} %</p>

        </div>
      )}
    </div>
  );
}

export default App;