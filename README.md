# ddog-alexa-skill

This is a simple example of utilizing alexa voice commands to query the Datadog Api for specific metrics.


Currently there are only a few query's that are supported: CPU `system.mem.total`, Memory `system.mem.total` disk `system.disk.total` : 

I also leveraged the [.rollup() function](https://docs.datadoghq.com/monitors/guide/monitor-arithmetic-and-sparse-metrics/#rollup) for the api to give me a single value.

> Alexa, ask Datadog what is my CPU:

will result in a response along the lines of:

> Your average CPU right now is 4%

![gif](https://p-WjFZ4qYb.b3.n0.cdn.getcloudapp.com/items/ApurK2pm/Screen+Recording+2020-02-10+at+04.54+PM.gif?v=d2286954f5d85deb882998caaabbb7cc)

# Datadog Webhook integration

I created a endpoint that also utilized Datadogs Webhook [integration](https://docs.datadoghq.com/integrations/webhooks/#overview)

```

# Additional Configuration

You'll also need to supply your Datadog API and app keys in order for the queries to work properly. You can set these in `config.py`:

```language-python
  DD_API_KEY: 'TODO',
  DD_APP_KEY: 'TODO'
```