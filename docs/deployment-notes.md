# Deployment Notes

Gotchas and non-obvious fixes discovered while deploying BrightPath to Azure App Service. Add to this file as new issues come up — future-you (or a teammate deploying their own service) will hit the same thing.

## Container App Service shows "Issues Detected" / health check "Unknown" despite a successful image push

**Symptom:** You build and push your Docker image to Azure Container Registry, the App Service deployment appears to succeed, but the Azure Portal shows a health warning ("Issues Detected") and the site either doesn't load or is flaky.

**Root cause:** Azure App Service for Containers needs to know which port your container actually listens on so it can route incoming traffic to it. The **Container** tab in the Portal has a "Port" field when you create the App Service (e.g. we set it to `80` for our nginx-based frontend), but this field alone does **not** reliably configure routing after the fact — Azure can still default incorrectly.

**Fix:** Explicitly add a `WEBSITES_PORT` application setting matching your container's exposed port.

In the Azure Portal:
1. Go to your App Service
2. Left sidebar → **Environment variables** (not "Configuration → General settings" — that's a different tab and does not fix this)
3. Add a new application setting:
   - Name: `WEBSITES_PORT`
   - Value: `80` (or whatever port your container's `EXPOSE` directive uses)
4. Save and restart the App Service

Or via Azure CLI:
```bash
az webapp config appsettings set \
  --name <your-app-service-name> \
  --resource-group <your-resource-group> \
  --settings WEBSITES_PORT=80
```

**Where this showed up:** `brightpath-frontend` App Service, deploying the nginx-based `.frontend.Dockerfile` image (`EXPOSE 80`). Health check was "Unknown" until `WEBSITES_PORT=80` was added; resolved immediately after a restart.
