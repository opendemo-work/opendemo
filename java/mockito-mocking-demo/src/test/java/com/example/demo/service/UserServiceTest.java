package com.example.demo.service;

import com.example.demo.model.User;
import com.example.demo.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * UserService测试类
 * 
 * 演示Mockito的各种特性
 */
@ExtendWith(MockitoExtension.class)  // 启用Mockito扩展
@DisplayName("用户服务测试")
public class UserServiceTest {
    
    @Mock  // 创建Mock对象
    private UserRepository userRepository;
    
    @Mock
    private NotificationService notificationService;
    
    @InjectMocks  // 自动注入Mock对象到被测类
    private UserService userService;
    
    private User testUser;
    
    @BeforeEach
    void setUp() {
        testUser = new User(1L, "john", "john@example.com", 25);
    }
    
    // ========== 基础Mock测试 ==========
    
    @Test
    @DisplayName("根据ID获取用户 - 用户存在")
    void testGetUserById_UserExists() {
        // given - 配置Mock行为
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        
        // when
        Optional<User> result = userService.getUserById(1L);
        
        // then - 验证结果
        assertThat(result).isPresent();
        assertThat(result.get().getUsername()).isEqualTo("john");
        
        // 验证Mock方法被调用
        verify(userRepository).findById(1L);
    }
    
    @Test
    @DisplayName("根据ID获取用户 - 用户不存在")
    void testGetUserById_UserNotExists() {
        // given
        when(userRepository.findById(999L)).thenReturn(Optional.empty());
        
        // when
        Optional<User> result = userService.getUserById(999L);
        
        // then
        assertThat(result).isEmpty();
        verify(userRepository).findById(999L);
    }
    
    @Test
    @DisplayName("获取所有用户")
    void testGetAllUsers() {
        // given
        User user2 = new User(2L, "jane", "jane@example.com", 30);
        when(userRepository.findAll()).thenReturn(Arrays.asList(testUser, user2));
        
        // when
        List<User> result = userService.getAllUsers();
        
        // then
        assertThat(result).hasSize(2);
        assertThat(result).extracting(User::getUsername)
                         .containsExactly("john", "jane");
    }
    
    // ========== 参数匹配器测试 ==========
    
    @Test
    @DisplayName("注册用户 - 成功")
    void testRegisterUser_Success() {
        // given
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(testUser);
        when(notificationService.sendWelcomeEmail(any(User.class))).thenReturn(true);
        
        // when
        User result = userService.registerUser(testUser);
        
        // then
        assertThat(result).isNotNull();
        assertThat(result.getUsername()).isEqualTo("john");
        
        // 验证交互
        verify(userRepository).existsByEmail("john@example.com");
        verify(userRepository).save(any(User.class));
        verify(notificationService).sendWelcomeEmail(any(User.class));
    }
    
    @Test
    @DisplayName("注册用户 - 邮箱已存在")
    void testRegisterUser_EmailExists() {
        // given
        when(userRepository.existsByEmail(anyString())).thenReturn(true);
        
        // when & then
        assertThatThrownBy(() -> userService.registerUser(testUser))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("邮箱已存在");
        
        // 验证save和sendWelcomeEmail没有被调用
        verify(userRepository, never()).save(any());
        verify(notificationService, never()).sendWelcomeEmail(any());
    }
    
    @Test
    @DisplayName("注册用户 - 年龄小于18岁")
    void testRegisterUser_AgeUnder18() {
        // given
        User youngUser = new User(2L, "young", "young@example.com", 16);
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        
        // when & then
        assertThatThrownBy(() -> userService.registerUser(youngUser))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("年龄必须大于等于18岁");
    }
    
    // ========== 参数捕获器测试 ==========
    
    @Test
    @DisplayName("注册用户 - 验证保存的用户")
    void testRegisterUser_VerifySavedUser() {
        // given
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(testUser);
        when(notificationService.sendWelcomeEmail(any(User.class))).thenReturn(true);
        
        // when
        userService.registerUser(testUser);
        
        // then - 使用ArgumentCaptor捕获参数
        ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);
        verify(userRepository).save(userCaptor.capture());
        
        User capturedUser = userCaptor.getValue();
        assertThat(capturedUser.getUsername()).isEqualTo("john");
        assertThat(capturedUser.getEmail()).isEqualTo("john@example.com");
    }
    
    // ========== 调用次数验证 ==========
    
    @Test
    @DisplayName("删除用户")
    void testDeleteUser() {
        // when
        userService.deleteUser(1L);
        
        // then - 验证方法被调用一次
        verify(userRepository, times(1)).deleteById(1L);
    }
    
    @Test
    @DisplayName("多次调用验证")
    void testMultipleCalls() {
        // given
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        
        // when
        userService.getUserById(1L);
        userService.getUserById(1L);
        userService.getUserById(1L);
        
        // then - 验证方法被调用3次
        verify(userRepository, times(3)).findById(1L);
    }
    
    // ========== 异常模拟测试 ==========
    
    @Test
    @DisplayName("更新用户 - 用户不存在")
    void testUpdateUser_UserNotFound() {
        // given
        when(userRepository.findById(anyLong())).thenReturn(Optional.empty());
        
        // when & then
        assertThatThrownBy(() -> userService.updateUser(999L, testUser))
                .isInstanceOf(RuntimeException.class)
                .hasMessage("用户不存在: 999");
    }
    
    // ========== 连续调用测试 ==========
    
    @Test
    @DisplayName("连续调用返回不同值")
    void testConsecutiveCalls() {
        // given - 第一次返回testUser，之后返回空
        when(userRepository.findById(1L))
                .thenReturn(Optional.of(testUser))
                .thenReturn(Optional.empty());
        
        // when & then
        assertThat(userService.getUserById(1L)).isPresent();
        assertThat(userService.getUserById(1L)).isEmpty();
    }
    
    // ========== Spy测试 ==========
    
    @Test
    @DisplayName("使用Spy部分Mock")
    void testWithSpy() {
        // Spy对象会调用真实方法，除非被stub
        UserService spyService = spy(userService);
        
        // when
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        spyService.getUserById(1L);
        
        // then - 验证真实方法被调用
        verify(spyService).getUserById(1L);
    }
}
