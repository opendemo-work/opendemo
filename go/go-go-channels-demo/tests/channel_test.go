package channels_test

import (
	"fmt"
	"strings"
	"testing"
	"time"

	"channels-demo/pkg/channels"
)

func TestBasicChannel(t *testing.T) {
	out := channels.BasicChannel()
	if len(out) == 0 {
		t.Fatal("BasicChannel 应返回非空输出")
	}
	joined := strings.Join(out, "\n")
	if !strings.Contains(joined, "工作协程开始处理任务") {
		t.Errorf("输出应包含 '工作协程开始处理任务'，实际为: %s", joined)
	}
	if !strings.Contains(joined, "主协程接收到结果: 处理完成!") {
		t.Errorf("输出应包含 '主协程接收到结果: 处理完成!'，实际为: %s", joined)
	}
}

func TestBufferedChannel(t *testing.T) {
	out := channels.BufferedChannel()
	joined := strings.Join(out, "\n")
	for _, expected := range []string{"生产者发送: 数据 1", "消费者接收到: 数据 1", "生产者完成，关闭通道", "消费者完成"} {
		if !strings.Contains(joined, expected) {
			t.Errorf("输出应包含 '%s'，实际为: %s", expected, joined)
		}
	}
}

func TestClosingChannel(t *testing.T) {
	out := channels.ClosingChannel()
	joined := strings.Join(out, "\n")
	for i := 1; i <= 3; i++ {
		expected := fmt.Sprintf("接收到数值: %d", i)
		if !strings.Contains(joined, expected) {
			t.Errorf("输出应包含 '%s'，实际为: %s", expected, joined)
		}
	}
	if !strings.Contains(joined, "channel 已关闭") {
		t.Errorf("输出应提示 channel 已关闭，实际为: %s", joined)
	}
}

func TestSelectChannelTimeout(t *testing.T) {
	out := channels.SelectChannel(50*time.Millisecond, 200*time.Millisecond)
	joined := strings.Join(out, "\n")
	if !strings.Contains(joined, "超时") {
		t.Errorf("任务慢于超时时应返回超时信息，实际为: %s", joined)
	}
}

func TestSelectChannelSuccess(t *testing.T) {
	out := channels.SelectChannel(200*time.Millisecond, 50*time.Millisecond)
	joined := strings.Join(out, "\n")
	if !strings.Contains(joined, "任务成功") {
		t.Errorf("任务快于超时时应返回成功信息，实际为: %s", joined)
	}
}
