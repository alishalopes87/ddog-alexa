from datadog import initialize, api
from config import DD_API_KEY, DD_APP_KEY
import time


def query_ddog_cpu():
	options = {
	    'api_key': 'DD_API_KEY',
	    'app_key': 'DD_APP_KEY'
	}

	initialize(**options)

	now = int(time.time())

	query = 'system.cpu.system{*}.rollup(avg)'
	result = api.Metric.query(start=now - 3600, end=now, query=query)
	metric = max(result['series'][0]["pointlist"])
	return str(round(metric[1])) + " percent"


output = query_ddog_cpu()
print(output)