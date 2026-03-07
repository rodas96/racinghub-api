# racinghub-api
Formula 1 api. Historical and up to date data
- 📚 **Interactive Docs**: https://racinghub.net/api/v1/docs
- 🐍 **Python Client**: https://pypi.org/project/racinghub-client/
- 📦 **npm Package**: https://www.npmjs.com/package/@racinghub/client

```bash
curl https://racinghub.net/api/v1/drivers/max-verstappen
```

```bash
pip install racinghub-client
```

```python
import pandas as pd

from racinghub_client import ApiClient, Configuration
from racinghub_client.api import DriversApi

client = ApiClient(configuration=Configuration(host="https://racinghub.net/api/v1"))
driver_api = DriversApi(client)

results = driver_api.get_driver_races_results("lewis-hamilton", limit=100)
df = pd.DataFrame([r.model_dump() for r in results.data])

df["positions_gained"] = df["grid_position"] - df["position"]
print(df[["race_date", "circuit_name", "positions_gained"]].head())
```

```bash
npm install @racinghub/client
```

```typescript
import { Configuration, DriversApi } from "@racinghub/client";

const config = new Configuration({ basePath: "https://racinghub.net/api/v1" });
const driversApi = new DriversApi(config);

const driver = await driversApi.getDriver({
  driverId: "max-verstappen",
});

const driver_results = await driversApi.getDriverRacesResults({
  driverId: "max-verstappen",
});
```

## MCP Support
All API endpoints are exposed as MCP tools at:
`https://racinghub.net/api/v1/mcp`

You can inspect the available tools using the MCP Inspector:
https://modelcontextprotocol.io/docs/tools/inspector

Example of an agent using it:
<img width="2048" height="954" alt="image" src="https://github.com/user-attachments/assets/0390554a-ea48-4410-8f4b-a5a5874ce0c5" />
<img width="2048" height="881" alt="image" src="https://github.com/user-attachments/assets/763e39ff-09c2-405d-be36-58c9e1e30037" />


## Developer Documentation
Comprehensive developer documentation is available in [`docs/dev/`](./docs/dev/) covering testing, configuration, deployment, and all project features.

### Quick Start for Developers
```bash
# Install development environment
make install

# Start services with Docker
docker compose up -d

# Run tests
make tests

# Auto-fix formatting
make chores
```

See the [developer documentation](./docs/dev/README.md) for complete guides and reference.
