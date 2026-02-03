module otel-demo

go 1.20

require (
	go.opentelemetry.io/otel v1.23.0
	go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc v1.23.0
	go.opentelemetry.io/otel/sdk v1.23.0
	google.golang.org/grpc v1.59.0
)

require (
	github.com/golang/protobuf v1.5.3
	github.com/google/uuid v1.3.0
	github.com/stretchr/testify v1.8.4
	go.opentelemetry.io/otel/exporters/otlp/internal/retry v1.23.0
	go.opentelemetry.io/otel/exporters/otlp/otlptrace v1.23.0
	go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp v1.23.0
	google.golang.org/genproto/googleapis/rpc v0.0.0-20231102141847-5db8af7c7948
)