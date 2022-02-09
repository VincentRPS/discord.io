from typing import TypeVar, Union

T = TypeVar('T', covariant=True)
Snowflakeish = int
SnowflakeishList = list[Snowflakeish]
SnowflakeishOr = Union[T, Snowflakeish]
