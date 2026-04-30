package com.opendemo.java.generics;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class GenericBox<T> {
    private static final Logger logger = LoggerFactory.getLogger(GenericBox.class);

    private T content;

    public GenericBox() {
    }

    public GenericBox(T content) {
        this.content = content;
    }

    public void set(T content) {
        this.content = content;
        logger.info("设置内容: {}", content);
    }

    public T get() {
        logger.info("获取内容: {}", content);
        return content;
    }

    public boolean isEmpty() {
        return content == null;
    }

    public String getType() {
        if (content == null) {
            return "null";
        }
        return content.getClass().getSimpleName();
    }

    @Override
    public String toString() {
        return "GenericBox{" + content + " (" + getType() + ")}";
    }
}
