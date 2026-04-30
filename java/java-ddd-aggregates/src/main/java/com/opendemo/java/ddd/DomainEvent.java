package com.opendemo.java.ddd;

import java.util.Objects;

public abstract class DomainEvent {
    private final String eventId;
    private final long timestamp;

    protected DomainEvent(String eventId) {
        this.eventId = eventId;
        this.timestamp = System.currentTimeMillis();
    }

    public String getEventId() {
        return eventId;
    }

    public long getTimestamp() {
        return timestamp;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DomainEvent that = (DomainEvent) o;
        return Objects.equals(eventId, that.eventId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(eventId);
    }
}
