# tcp_web_chat

Установка:
1) git clone https://github.com/dimadeck/tcp_web_chat
2) cd tcp_web_chat

Активация и настройка виртуального окружения:
3) python -m venv env
4) source env/bin/activate
5) pip install -r requirements.txt

Запуск сервера:
6) python main.py

Запуск клиента(-ов):
7) python main.py 127.0.0.1

Сервер v.0.1:
Консольное приложение
Принимает и обрабатывает подключения клиентов (main.py <ip>).

Подключены парсеры для обработки запросов по tcp(class DataParser) и web(class HttpParser) протоколам.
Проверки команд на валидность.
Связи подключение-пользователь хранятся в классе Connected.

Демонстрация работы сервера и команд login, msg, msgall, logout.
![alt text](github01.png)

Цикл работы:
После запуска, сервер ожидает входящие подключения. При появлении нового подключения запоминает его на новом потоке.
Ожидает входа пользователя командой login <username>. Присутствует проверка на дубликаты имен. Перед подключением можно
"прощупать" синтаксис команд сервера, так как проверка на валидность команд идет перед проверкой на подключение,
однако отправлять и получать сообщения чата незарегистрированный пользователь не может. После команды login <username>
пользователь считается зарегистрированным.

Команды:
login <username> Подключить нового пользователя. Все последующие команды могут быть выполнены только после этой.

msg <username> <text> Отправить сообщение <text> пользователю с именем <username>.

msgall <text> Отправить сообщение <text> всем подключенным пользователям.

logout Выйти из чата. Так же выход должен происходить автоматически при закрытии приложения.

whoami - узнать свое имя

userlist - узнать кто онлайн

debug - показать информацию о подключениях в терминале сервера(клиент НЕ видит ее)


TCP Клиент:
Минималистичное консольное Python приложение.
Подключается к серверу по протоколу TCP, передает команды, получает сообщения от сервера и других клиентов.


NOTE:
В server v.0.1. добавлен код(классы, механизмы, шаблоны html, и т.д.) для обработки web соединений, но нуждается
в дополнении и жесткой отладке, поэтому для комфорта проверки и работы чата закомментирован.