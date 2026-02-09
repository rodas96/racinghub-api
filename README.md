# racinghub-api
Formula 1 api. Historical and up to date data
- 📚 **Interactive Docs**: https://racinghub.net/api/v1/docs
- 🐍 **Python Client**: https://pypi.org/project/racinghub-client/
- 📦 **npm Package**: https://www.npmjs.com/package/@racinghub/client

```bash
curl https://racinghub.net/api/v1/drivers/max-verstappen
```

```bash
pip install racinghub_client
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
