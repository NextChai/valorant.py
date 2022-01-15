# valorantpy
The async wrapper for the Valorant APi.

# Features
- [x] Memory optimized efficient wrapper for the valorant API.

# Please note
This library is undergoing heavy changes and is not recommended for use yet. There are many
limitations and that will be fixed in the future. Breaking changes **will** be pushed without warning and 
currently it's up to you to find a way to work around them. If you find any bugs feel free to contact me
`Chai#9762`.

# Code Example
```python

import aiohttp
from valorant import ValorantClient

async with aiohttp.ClientSession() as session:
    client = ValorantClient(
        'your-valorant-client', 
        session=session
    )
    account = await client.fetch_account_by_riot_id('Slix', 'yes')
    print(account)

```

