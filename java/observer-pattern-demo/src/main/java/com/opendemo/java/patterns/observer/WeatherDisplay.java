package com.opendemo.java.patterns.observer;

public class WeatherDisplay implements Observer {

    private final String location;
    private float temperature;
    private float humidity;

    public WeatherDisplay(String location) {
        this.location = location;
    }

    @Override
    public void update(Object data) {
        if (data instanceof WeatherStation.WeatherData) {
            WeatherStation.WeatherData weatherData = (WeatherStation.WeatherData) data;
            this.temperature = weatherData.getTemperature();
            this.humidity = weatherData.getHumidity();
            System.out.println("WeatherDisplay [" + location + "]: Temp=" + temperature
                    + "°C, Humidity=" + humidity + "%");
        }
    }

    public String getLocation() {
        return location;
    }

    public float getTemperature() {
        return temperature;
    }

    public float getHumidity() {
        return humidity;
    }
}
