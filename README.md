# Тестовое задание для fastapi
Необходимо на fastapi создать сервис рассылки. 

Данный сервис будет являться частью микросервисной архитектуры, которая обеспечивает работу большого проекта в части 
уведомлений пользорвателей на email или в telegram.

## Спецификация

Сервис должен иметь одну точку входа:
`/api/notify/`

Тело запроса должно обязательно включать следующие параметры:
```python
{
  "message": strgin(1024),
  "recepient": string(150) | list[string(150)],
  "delay": int
}
```

- Параметр `message` содержит обычный текст, который будет отправлен в сообщении

- Параметр `recepient` может содержать одного получателя или список получателей. 
При этом необходимо определять для каждого получателя, предоставлен адрес для отправки на почту или в telegram.
В получателе telegram всегда только числа, почта оформлена по общей маске почтового адреса.

- Параметр `delay` отвечает за задержку отправки, где:

  `0` - отправлять без задержки, при получении запроса
  
  `1` - отправить с задержкой в 1 час
  
  `2` - отправить с задержкой в 1 день

## Дополнительно

При получении сообщение должно складываться в отдельную таблиу. 
А при рассылке необходимо записывать лог о попытке отправки в БД.
Сама отправка должна осуществляться с помощью очереди через celery.

Все доступы для отправки указываются внутри микросервиса. 

## Оформление
При реализации важно обращаться к рекомендациям по оформлению из данного гайда: 
https://github.com/zhanymkanov/fastapi-best-practices

Результат работы необходимо сдать ссылкой на github репозиторий