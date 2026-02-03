package main

import (
	"context"
	"log"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	"go.opentelemetry.io/otel/sdk/trace"
	"go.opentelemetry.io/otel/trace/noop"
	"google.golang.org/grpc/credentials/insecure"
)

// 初始化OpenTelemetry TracerProvider
func initTracer() (*trace.TracerProvider, error) {
	// 创建OTLP gRPC导出器，连接本地Jaeger
	exporter, err := otlptracegrpc.New(
		context.Background(),
		otlptracegrpc.WithInsecure(),
		otlptracegrpc.WithEndpoint("localhost:4317"),
	)
	if err != nil {
		return nil, err
	}

	// 设置资源信息（服务名等）
	res, err := resource.New(context.Background(),
		resource.WithAttributes(),
		resource.WithSchemaURL("https://opentelemetry.io/schemas/1.21.0"),
	)
	if err != nil {
		return nil, err
	}

	// 创建TracerProvider并设置批量处理
	tp := trace.NewTracerProvider(
		trace.WithBatcher(exporter),
		trace.WithResource(res),
	)

	// 设置全局TracerProvider
	otel.SetTracerProvider(tp)
	// 设置默认上下文传播器
	otel.SetTextMapPropagator(propagation.TraceContext{})

	return tp, nil
}

func main() {
	log.Println("INFO: Initializing OpenTelemetry...")
	tracerProvider, err := initTracer()
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err := tracerProvider.Shutdown(context.Background()); err != nil {
			log.Printf("Error shutting down tracer provider: %v", err)
		}
	}()

	// 获取Tracer
	tracer := otel.Tracer("otel-demo")

	// 创建父Span
	ctx, span := tracer.Start(context.Background(), "parent-span")
	log.Println("INFO: Starting parent span...")
	defer span.End()

	// 启动带上下文的工作协程
	log.Println("INFO: Launching background worker...")
	go doWork(ctx, tracer)

	// 模拟主流程工作
	time.Sleep(time.Second * 2)

	log.Println("Worker task completed.")
	log.Println("Press Enter to exit...")
	make(chan struct{})<-chan struct{}
}