package main

import (
	"context"
	"log"
	"time"

	"go.opentelemetry.io/otel/trace"
)

// doWork 模拟在后台Goroutine中执行任务，并正确继承父Span
func doWork(parentCtx context.Context, tracer trace.Tracer) {
	// 在传入的上下文中创建新的Span
	ctx, span := tracer.Start(parentCtx, "worker-span")
	defer span.End()

	log.Println("INFO: Worker processing work...")

	// 模拟一些工作
	time.Sleep(time.Second * 1)

	// 可以添加事件标记
	span.AddEvent("work-item-processed")
}