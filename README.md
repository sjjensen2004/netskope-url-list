# What does this thing do?

This takes the URL list from [https://urlhaus.abuse.ch/downloads/csv_online/], parses it, and uploads the URL list to your Netskope Tenant. 

## What do I need to use this?

Docker and Docker Compose installed on your host and a Netskope tenant. 

## How do I use this?

First, modify ./env/tenant.env with your Netskope Tenanat information. 

- NETSKOPE_TOKEN: This is the token you generated in settings/tools/Rest API v2/New Token (Make sure the Scope is set and that you have R/W access to URL lists)
- TENANT_URL: This is your tenant endpoint. Something [https://<your-tenant>.goskope.com]

Now run  `docker-compose up`

**DISCLAIMER**
This is a quick and dirty script and is likely to have errors. It's meant for learning purpose only <@>:)