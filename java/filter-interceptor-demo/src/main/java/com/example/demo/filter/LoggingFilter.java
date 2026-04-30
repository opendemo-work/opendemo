package com.example.demo.filter;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

public class LoggingFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) {
        System.out.println("[Filter] LoggingFilter 初始化");
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        long start = System.currentTimeMillis();

        System.out.println("[Filter] 请求开始: " + httpRequest.getMethod() + " " + httpRequest.getRequestURI());

        chain.doFilter(request, response);

        long duration = System.currentTimeMillis() - start;
        System.out.println("[Filter] 请求完成: " + httpRequest.getRequestURI() + " 耗时: " + duration + "ms");
    }

    @Override
    public void destroy() {
        System.out.println("[Filter] LoggingFilter 销毁");
    }
}
