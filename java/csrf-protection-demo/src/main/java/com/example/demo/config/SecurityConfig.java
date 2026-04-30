package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/", "/home", "/css/**").permitAll()
                .antMatchers("/transfer/**").authenticated()
                .anyRequest().authenticated()
            .and()
            .formLogin()
                .defaultSuccessUrl("/home")
                .permitAll()
            .and()
            .logout()
                .logoutSuccessUrl("/")
                .permitAll()
            .and()
            .csrf()
                .csrfTokenRepository(cookieCsrfTokenRepository())
                .and()
            .headers()
                .xssProtection()
                .and()
                .contentSecurityPolicy("default-src 'self'");
        return http.build();
    }

    @Bean
    public CookieCsrfTokenRepository cookieCsrfTokenRepository() {
        CookieCsrfTokenRepository repository = new CookieCsrfTokenRepository();
        repository.setCookieHttpOnly(false);
        repository.setCookieName("XSRF-TOKEN");
        repository.setHeaderName("X-XSRF-TOKEN");
        return repository;
    }

    @Bean
    public UserDetailsService userDetailsService() {
        return new InMemoryUserDetailsManager(
            User.withUsername("alice")
                .password("{noop}password123")
                .roles("USER")
                .build(),
            User.withUsername("bob")
                .password("{noop}admin456")
                .roles("USER", "ADMIN")
                .build()
        );
    }
}
