package com.opendemo.java.patterns.templatemethod;

public abstract class AbstractGame {

    public final void play() {
        initialize();
        startPlay();
        endPlay();
    }

    protected abstract void initialize();

    protected abstract void startPlay();

    protected abstract void endPlay();
}
