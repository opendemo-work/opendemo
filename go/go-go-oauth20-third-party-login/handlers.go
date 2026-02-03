package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/github"
)

// OAuth2 配置对象，用于与 GitHub 交互
var githubOauthConfig = &oauth2.Config{
	ClientID:     os.Getenv("GITHUB_CLIENT_ID"),
	ClientSecret: os.Getenv("GITHUB_CLIENT_SECRET"),
	RedirectURL:  "http://localhost:8080/callback",
	Scopes:       []string{"user:email"}, // 请求用户邮箱权限
	Endpoint:     github.Endpoint,        // 使用 GitHub 的 OAuth2 终端
}

// loginHandler 处理登录请求：重定向到 GitHub 授权页面
func loginHandler(w http.ResponseWriter, r *http.Request) {
	// 生成 OAuth2 授权 URL
	url := githubOauthConfig.AuthCodeURL("state-token", oauth2.AccessTypeOnline)
	// 重定向用户到 GitHub 进行授权
	http.Redirect(w, r, url, http.StatusTemporaryRedirect)
}

// GitHub 用户信息结构体
type GitHubUser struct {
	Login     string `json:"login"`
	ID        int64  `json:"id"`
	AvatarURL string `json:"avatar_url"`
	Name      string `json:"name"`
	Email     string `json:"email"`
}

// callbackHandler 处理 GitHub 回调
func callbackHandler(w http.ResponseWriter, r *http.Request) {
	// 获取返回的授权码
	code := r.URL.Query().Get("code")
	if code == "" {
		http.Error(w, "授权码缺失", http.StatusBadRequest)
		return
	}

	// 使用授权码向 GitHub 申请访问令牌
	token, err := githubOauthConfig.Exchange(r.Context(), code)
	if err != nil {
		http.Error(w, fmt.Sprintf("无法获取访问令牌: %v", err), http.StatusInternalServerError)
		return
	}

	// 构建请求获取用户信息
	client := githubOauthConfig.Client(r.Context(), token)
	resp, err := client.Get("https://api.github.com/user")
	if err != nil {
		http.Error(w, fmt.Sprintf("无法获取用户信息: %v", err), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// 解析 JSON 响应
	var ghUser GitHubUser
	if err := json.NewDecoder(resp.Body).Decode(&ghUser); err != nil {
		http.Error(w, "解析用户信息失败", http.StatusInternalServerError)
		return
	}

	// 返回欢迎信息给用户
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	fmt.Fprintf(w, "欢迎你，%s！\n", ghUser.Login)
	if ghUser.Email != "" {
		fmt.Fprintf(w, "邮箱: %s\n", ghUser.Email)
	} else {
		fmt.Fprintf(w, "邮箱: 未公开\n")
	}
	fmt.Fprintf(w, "头像: %s\n", ghUser.AvatarURL)

	log.Printf("用户 %s 成功登录", ghUser.Login)
}
