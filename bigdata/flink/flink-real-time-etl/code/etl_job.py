from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

# 定义 Kafka 源表
t_env.execute_sql('''
    CREATE TABLE user_events (
        user_id STRING,
        event_type STRING,
        event_time TIMESTAMP(3)
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'user-events',
        'properties.bootstrap.servers' = 'kafka:9092',
        'format' = 'json'
    )
''')

# 实时聚合
t_env.execute_sql('''
    CREATE TABLE event_stats (
        event_type STRING PRIMARY KEY NOT ENFORCED,
        event_count BIGINT
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:mysql://mysql:3306/demo',
        'table-name' = 'event_stats'
    )
''')

t_env.execute_sql('''
    INSERT INTO event_stats
    SELECT event_type, COUNT(*) as event_count
    FROM user_events
    GROUP BY event_type
''')
