# import asyncio
import datetime
import edgedb

# client = edgedb.create_client(dsn="edgedb://edgedb@localhost:5656")

client = edgedb.create_client()

client.query(
    """
    INSERT User {
        name := <str>$name,
    }
    """,
    name="Bob",
)

user_count = client.query(
    "SELECT count(User {name} FILTER .name = <str>$name)", name="Bob"
)
user_set = client.query("SELECT User {name} FILTER .name = <str>$name", name="Bob")
# *user_set* now contains
# Set{Object{name := 'Bob', dob := datetime.date(1984, 3, 1)}}
print(user_count)
print(user_set)

client.query(
    """
    DELETE User {name := <str>$name}
""",
    name="Bob",
)
client.close()
