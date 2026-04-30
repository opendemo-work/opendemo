package com.opendemo.java.patterns.observer;

public class NewsSubscriber implements Observer {

    private final String name;
    private String lastReceivedNews;

    public NewsSubscriber(String name) {
        this.name = name;
    }

    @Override
    public void update(Object data) {
        this.lastReceivedNews = (String) data;
        System.out.println("NewsSubscriber [" + name + "]: Received news: " + data);
    }

    public String getName() {
        return name;
    }

    public String getLastReceivedNews() {
        return lastReceivedNews;
    }
}
