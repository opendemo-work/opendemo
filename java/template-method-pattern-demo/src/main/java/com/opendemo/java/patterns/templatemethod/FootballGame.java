package com.opendemo.java.patterns.templatemethod;

public class FootballGame extends AbstractGame {

    @Override
    protected void initialize() {
        System.out.println("FootballGame: Setting up football field...");
        System.out.println("FootballGame: Teams warming up, referee ready");
    }

    @Override
    protected void startPlay() {
        System.out.println("FootballGame: Kickoff! Two halves of 45 minutes");
        System.out.println("FootballGame: Players passing and shooting");
    }

    @Override
    protected void endPlay() {
        System.out.println("FootballGame: Full time! Final whistle blown");
        System.out.println("FootballGame: Announcing match result");
    }
}
