from dataclasses import dataclass
from ssl import SSLContext


@dataclass
class TlsSettings:
    ssl: SSLContext
