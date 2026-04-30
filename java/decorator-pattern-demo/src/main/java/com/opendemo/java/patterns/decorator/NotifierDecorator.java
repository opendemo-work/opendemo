package com.opendemo.java.patterns.decorator;

public abstract class NotifierDecorator implements Notifier {

    protected final Notifier wrappedNotifier;

    public NotifierDecorator(Notifier notifier) {
        this.wrappedNotifier = notifier;
    }

    @Override
    public void send(String message) {
        wrappedNotifier.send(message);
    }

    @Override
    public String getChannel() {
        return wrappedNotifier.getChannel();
    }
}
