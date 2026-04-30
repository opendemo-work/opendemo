package com.opendemo.java.patterns.strategy;

import java.util.Arrays;

public class Sorter {

    private SortingStrategy sortingStrategy;

    public void setSortingStrategy(SortingStrategy sortingStrategy) {
        this.sortingStrategy = sortingStrategy;
    }

    public void sort(int[] array) {
        if (sortingStrategy == null) {
            System.out.println("No sorting strategy selected!");
            return;
        }
        System.out.println("Using: " + sortingStrategy.getName());
        System.out.println("Before: " + Arrays.toString(array));
        sortingStrategy.sort(array);
        System.out.println("After:  " + Arrays.toString(array));
    }
}
