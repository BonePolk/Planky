### `Version 0.1` Storage update

- Fix unexpected disconnect
- Removed unused tlsSetting class
- Removed "extra" from events.
- Replaced "extra" with "storage" for clients.
- Storage now supports storing custom data by key.
- Added support for storing expiring data in storage.
- Removed unused "extra" class
- Added a "ping_time" to client to store the timestamp of the last ping.
- "parse_extra" now don't return Extra class
- add default value for Storage.get
- Global storage for server

### `Version 0.0.1.2` First changelog patch

- Fix receiving data with several clients
- Now PlankyClient creating for next clients
- Clients stored in PlankyHandler.clients with specific id
- Now callbacks will receive client and event
- Events now contains extra instead of client_ip and client_port