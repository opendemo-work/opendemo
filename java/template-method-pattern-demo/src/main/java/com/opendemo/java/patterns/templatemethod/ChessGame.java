package com.opendemo.java.patterns.templatemethod;

public class ChessGame extends AbstractGame {

    @Override
    protected void initialize() {
        System.out.println("ChessGame: Setting up chess board...");
        System.out.println("ChessGame: Placing pieces in starting positions");
    }

    @Override
    protected void startPlay() {
        System.out.println("ChessGame: Players take turns moving pieces");
        System.out.println("ChessGame: White moves first, then Black");
    }

    @Override
    protected void endPlay() {
        System.out.println("ChessGame: Game Over - Checkmate!");
        System.out.println("ChessGame: Recording game result");
    }
}
