package com.opendemo.java.patterns.observer;

import java.util.ArrayList;
import java.util.List;

public class NewsPublisher implements Subject {

    private final List<Observer> subscribers = new ArrayList<>();
    private String latestNews;

    @Override
    public void attach(Observer observer) {
        if (!subscribers.contains(observer)) {
            subscribers.add(observer);
        }
    }

    @Override
    public void detach(Observer observer) {
        subscribers.remove(observer);
    }

    @Override
    public void notifyObservers() {
        for (Observer observer : subscribers) {
            observer.update(latestNews);
        }
    }

    public void publishNews(String news) {
        this.latestNews = news;
        System.out.println("NewsPublisher: Publishing news: " + news);
        notifyObservers();
    }

    public String getLatestNews() {
        return latestNews;
    }

    public int getSubscriberCount() {
        return subscribers.size();
    }
}
