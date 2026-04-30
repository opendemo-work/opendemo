package com.opendemo.java.ddd;

import java.util.*;

public abstract class AggregateRoot {
    private final List<DomainEvent> uncommittedEvents = new ArrayList<>();

    protected void registerEvent(DomainEvent event) {
        uncommittedEvents.add(event);
    }

    public List<DomainEvent> getUncommittedEvents() {
        return Collections.unmodifiableList(uncommittedEvents);
    }

    public void clearUncommittedEvents() {
        uncommittedEvents.clear();
    }
}
