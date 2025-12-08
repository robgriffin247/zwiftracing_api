# Demo 1: Extract from ZwiftRacing.app endpoints

**Aim:** Create Python functions to extract data from each ZwiftRacing.app endpoint.

## Prerequisites

- Development environment
- ZwiftRacing.app API key in your environment


## Endpoints

### General

- Requests are made to the base URL ``https://api.zwiftracing.app/api/public/``
- Requests require an API key as a header ``HEADER = {"Authorization": os.getenv("ZRAPP_API_KEY")}``


### ``GET rider``

- Takes a single integer input of a riders Zwift ID
- Returns details of a single rider
- Payload returned as a dictionary of [current rider details](data/rider.json)
- When supplied with an epoch timestamp (in seconds), the ``race`` key [contains values](data/rider_epoch.json) at the given epoch (all other details are current)


### ``POST riders``

- Takes a Python list of integers of Zwift IDs
- Returns details of the given riders
- Payload returned as a [list of rider dictionaries](data/riders.json)
- When supplied with an epoch timestamp (in seconds), the ``race`` key [contains values](data/riders_epoch.json) at the given epoch (all other details are current)


### ``GET club``

- Takes a single integer input of a clubs ID
- Returns [club name, id and a list of rider dictionaries](data/club.json)
- Riders list is truncated to the first 1000 riders (sorted on Zwift ID)
    - Further riders can be obtained using a rider Zwift ID [to set a start point](data/club_from.json), e.g. in a club with riders ``[1, 2, 3, 4]``, setting the rider ID to ``3`` would return riders ``[3, 4]``


### ``GET result``

- Takes a single integer input of an event/race ID
- Returns event details and a list of riders sorted on position
- Payload returned as a [dictionary including the ``results`` &mdash; a list of rider details specific to the race (not as returned by the rider(s)/club endpoints)](data/results.json)


### ``GET zp result``

- Takes a single integer input of an event/race ID
- Returns a list of riders sorted on position from ZwiftPower
- Payload returned as a [list of dictionaries, each representing one rider](data/zp_results.json)



## Using the data

1. Get the data &mdash; I've called it ``event`` as it contains more than just results

    ```
    event = get_event(5188741)
    ```

1. If you save the data as json file, you can can load it to reduce load on the ZwiftRacing.app API    
    
    - Save

        ```
        id = 5188741
        event = get_event(id)
        with open(f"load/data/event_{id}.json", "w") as f:
            json.dump(event, f)
        ```

    - Load

        ```
        with open("extract/data/event_5188741.json", "r") as f:
            event = json.load(f)
        ```    

1. Explore the ``event`` dictionary object; &mdash; these are the keys

    ```
    for k in event.keys():
        print(k)
    ```

1. Get a value using ``get()``

    ```
    print(event.get("eventId"))
    ```

1. The the results data &mdash; a list of dictionaries, one per finisher/rider

    ```
    results = event.get("results")
    ```

1. Print the keys of the first rider

    ```
    for r in results[0].keys():
        print(r)
    ```