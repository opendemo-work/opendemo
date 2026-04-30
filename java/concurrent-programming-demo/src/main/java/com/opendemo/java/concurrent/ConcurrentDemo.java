package com.opendemo.java.concurrent;

public class ConcurrentDemo {

    public static void main(String[] args) throws Exception {
        System.out.println("=== Java并发编程演示 ===");
        System.out.println();

        ThreadCreationDemo.main(args);
        System.out.println();

        SynchronizedDemo.main(args);
        System.out.println();

        ConcurrentCollectionsDemo.main(args);
        System.out.println();

        ExecutorServiceDemo.main(args);
        System.out.println();

        AtomicVariableDemo.main(args);
        System.out.println();

        ProducerConsumerDemo.main(args);
    }
}
