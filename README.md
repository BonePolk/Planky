# Planky

![icon.png](https://raw.githubusercontent.com/BonePolk/Planky/refs/heads/master/icon.png)

<details>
<summary>🇬🇧 English</summary>


### Description
**Planky** is an easy-to-use and highly customizable tool for building your own **tcp/tls** server.

### Installation
```commandline
pip install Planky
```

### Usage

```python
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.plankyData import PlankyData
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

@server.on_message(ParsedMessage)
async def parsed_message(handler, event: MessageEvent):
    if event.message.content == b"hello": 
        await handler.send_data(PlankyData(payload=b"world"))
    else:
        await handler.send_data(PlankyData(payload=event.message.content))

if __name__ == "__main__":
    server.mainloop()
```

### Main features

- Simple usage
- TLS support
- Server side certificate validation support
- Custom parsers support
- Async support

### Documentation

- [ReadTheDocs](https://planky.readthedocs.io/en/latest/)

### Thanks

Nobody...

</details>

<details>
<summary>🇷🇺 Русский</summary>

### Описание
**Planky** — это простой и гибкий инструмент для создания собственного асинхронного **tcp/tls** сервера.

### Установка
```commandline
pip install Planky
```

### Использование

```python
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.plankyData import PlankyData
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

@server.on_message(ParsedMessage)
async def parsed_message(handler, event: MessageEvent):
    if event.message.content == b"hello": 
        await handler.send_data(PlankyData(payload=b"world"))
    else:
        await handler.send_data(PlankyData(payload=event.message.content))

if __name__ == "__main__":
    server.mainloop()
```

### Основные возможности

- Простое использование
- Поддержка tls
- Поддержка проверки сертификата на сервере
- Поддержка кастомных парсеров
- Поддержка асинхронности

### Документация

- [ReadTheDocs](https://planky.readthedocs.io/en/latest/)

### Благодарности

Пока нету

</details>