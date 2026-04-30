package com.opendemo.java.patterns.observer;

import java.util.ArrayList;
import java.util.List;

public class WeatherStation implements Subject {

    private final List<Observer> displays = new ArrayList<>();
    private float temperature;
    private float humidity;
    private float pressure;

    @Override
    public void attach(Observer observer) {
        if (!displays.contains(observer)) {
            displays.add(observer);
        }
    }

    @Override
    public void detach(Observer observer) {
        displays.remove(observer);
    }

    @Override
    public void notifyObservers() {
        WeatherData weatherData = new WeatherData(temperature, humidity, pressure);
        for (Observer observer : displays) {
            observer.update(weatherData);
        }
    }

    public void setMeasurements(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        System.out.println("WeatherStation: Measurements updated - Temp: " + temperature
                + "°C, Humidity: " + humidity + "%, Pressure: " + pressure + " hPa");
        notifyObservers();
    }

    public static class WeatherData {
        private final float temperature;
        private final float humidity;
        private final float pressure;

        public WeatherData(float temperature, float humidity, float pressure) {
            this.temperature = temperature;
            this.humidity = humidity;
            this.pressure = pressure;
        }

        public float getTemperature() { return temperature; }
        public float getHumidity() { return humidity; }
        public float getPressure() { return pressure; }
    }
}
