package com.opendemo.java.patterns.decorator;

public class EmailNotifier extends NotifierDecorator {

    public EmailNotifier(Notifier notifier) {
        super(notifier);
    }

    public EmailNotifier() {
        super(null);
    }

    @Override
    public void send(String message) {
        if (wrappedNotifier != null) {
            wrappedNotifier.send(message);
        }
        System.out.println("[Email] Sending: " + message);
    }

    @Override
    public String getChannel() {
        String base = wrappedNotifier != null ? wrappedNotifier.getChannel() + ", " : "";
        return base + "Email";
    }
}
