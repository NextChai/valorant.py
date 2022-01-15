# valorantpy
The async wrapper for the Valorant API.

# Features
- [x] Memory optimized efficient wrapper for the valorant API.
- [x] Complete API coverage.
- [x] Async/await support.
- [x] Support for an in depth cache system, allowing for the optimization of API calls.

# Please note
This library is undergoing heavy changes and is no where near production ready. There are many
limitations and that will be fixed in the future. Breaking changes **will** be pushed without warning and 
currently it's up to you to find a way to work around them. It is recommended to **NOT USE THIS LIBRARY UNTIL
IT IS STABLE AND HAS COMPLETE API COVERAGE.** If you find any bugs feel free to contact me
`Chai#9762`.

# Code Example
```python
import asyncio
import aiohttp
import valorant

async def main():
    session = aiohttp.ClientSession() 
    
    client = valorant.ValorantClient(token='', session=session)
    agents = await client.fetch_agents()
    agent = agents[0]
    
    new = await client.fetch_agent(agent.uuid)
    await session.close()
    
asyncio.run(main())
```

