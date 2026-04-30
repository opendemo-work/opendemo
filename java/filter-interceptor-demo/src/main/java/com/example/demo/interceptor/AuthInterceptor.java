package com.example.demo.interceptor;

import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Component
public class AuthInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String uri = request.getRequestURI();
        System.out.println("[Interceptor] preHandle: " + uri + " handler=" + handler.getClass().getSimpleName());
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) {
        System.out.println("[Interceptor] postHandle: " + request.getRequestURI() + " status=" + response.getStatus());
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        if (ex != null) {
            System.out.println("[Interceptor] afterCompletion (异常): " + request.getRequestURI() + " exception=" + ex.getMessage());
        } else {
            System.out.println("[Interceptor] afterCompletion (正常): " + request.getRequestURI());
        }
    }
}
