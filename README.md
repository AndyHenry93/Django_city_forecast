# Real-Time Weather Application

This Django application provides real-time weather data for the top 250 cities in the United States, allowing users to view weather conditions based on their specific search criteria.

## Key Features

### 1. **Custom Weather Search**
- Users can input specific weather conditions (e.g., temperature, humidity, wind speed) to filter and display relevant data.

### 2. **Top 250 US Cities**
- Covers the top 250 most populous cities across the U.S., providing localized weather updates.

### 3. **Data Integration**
- Utilizes the OpenWeather API for fetching real-time weather data.
- Leverages the Google API Suite to connect to an Excel sheet for storing and managing weather-related information.

### 4. **Docker Implementation**
- Application is containerized using Docker, ensuring consistent and scalable deployment across different environments.

### 5. **Celery for Asynchronous Tasks**
- Handles time-consuming tasks asynchronously using Celery, optimizing performance by offloading heavy processes like data fetching and processing.

### 6. **Caching for Optimization**
- Implements caching to store frequently accessed data, reducing load times and minimizing repeated API calls.

## Technologies Used

- **Backend**: Django
- **APIs**: OpenWeather API, Google API Suite
- **Task Queue**: Celery
- **Caching**: Django caching framework (e.g., Memcached or Redis)
- **Containerization**: Docker
- **Asynchronous Task Broker**: RabbitMQ or Redis

## How to Run the Application

### Prerequisites
- Docker installed on your machine
- API keys for OpenWeather and Google API Suite
- Redis or RabbitMQ for Celery task management

### Steps

1. **Clone the Repository**:
    ```bash
    https://github.com/AndyHenry93/Django_city_forecast.git
    cd django-weather-app
    ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory and add your API keys and other configurations.
   
3. **Build and Run Docker Containers**:
    ```bash
    docker-compose up --build
    ```

4. **Run Celery Workers**:
    In a separate terminal, start the Celery worker:
    ```bash
    docker-compose exec web celery -A weather_app worker --loglevel=info
    ```

5. **Access the Application**:
   - Open your browser and navigate to `http://localhost:8000`.
  
# Docker Repository

Feel free to pull the Git repository and review the code.  
The Docker container can be found here: [andyhenry93/django-forecast-project](https://hub.docker.com/r/andyhenry93/django-forecast-project)

## Command to Pull Docker Repository
```bash
docker pull andyhenry93/django-forecast-project
```

## Command to Run Container
  ```bash
  docker run -p 8000:8000 andyhenry93/django-forecast-project
  ```

## Call Server
```bash
127.0.0.1:8000
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

By combining fast, efficient technologies like Docker, Celery, caching, and API integrations, this application delivers an optimal, responsive user experience for accessing real-time weather information.
