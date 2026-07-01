import requests

query = '''
SELECT event_type, COUNT(*) as cnt, SUM(amount) as total
FROM demo.events
GROUP BY event_type
ORDER BY total DESC
'''

resp = requests.post('http://localhost:8123', data=query)
print(resp.text)
