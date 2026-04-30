package com.opendemo.java.patterns.decorator;

public class SMSNotifier extends NotifierDecorator {

    public SMSNotifier(Notifier notifier) {
        super(notifier);
    }

    public SMSNotifier() {
        super(null);
    }

    @Override
    public void send(String message) {
        if (wrappedNotifier != null) {
            wrappedNotifier.send(message);
        }
        System.out.println("[SMS] Sending: " + message);
    }

    @Override
    public String getChannel() {
        String base = wrappedNotifier != null ? wrappedNotifier.getChannel() + ", " : "";
        return base + "SMS";
    }
}
