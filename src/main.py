import logging
import sys

from apps.library.router import operations_routing

logger = logging.getLogger("streamLogger")

def main() -> None:
    # Вызов python main.py дает подсказку
    if len(sys.argv) < 2:
        logger.info("Usage: python main.py <operation> [args]")
        sys.exit(1)

    operation = sys.argv[1]  # Ожидаем, что операция будет вторым аргументом

    # Явно объявляем операции из router для простоты восприятия
    create = operations_routing.get("add")
    get_all = operations_routing.get("view_all")
    delete = operations_routing.get("delete")
    change = operations_routing.get("change_status")
    search = operations_routing.get("search")

    # Обработка каждой команды от юзера
    if operation == "add":
        # Ожидаем, что будут переданы аргументы для добавления книги (title, author, year)
        if len(sys.argv) != 5:
            logger.warning("Usage: python script.py add <title> <author> <year>")
            sys.exit(1)
        title = sys.argv[2]
        author = sys.argv[3]
        year = int(sys.argv[4])

        create(title, author, year)
    elif operation == "view_all":
        logger.info(get_all())
    elif operation == "delete":
        if len(sys.argv) != 3:
            logger.warning("Usage: python script.py delete <id>")
            sys.exit(1)
        
        book_id = int(sys.argv[2])
        delete(book_id)
    elif operation == "change_status":
        if len(sys.argv) != 4:
            logger.warning("Usage: python script.py change_status <id> <status>")
            sys.exit(1)

        book_id = int(sys.argv[2])
        status = sys.argv[3]
        change(book_id, status)
    elif operation == "search": # Нужно явно указать поле и значение для поиска => python main.py search title "Some title" author Author
        kwargs = {}

        for i in range(2, len(sys.argv), 2):
            if i + 1 < len(sys.argv):
                kwargs[sys.argv[i]] = sys.argv[i + 1]

        books = search(**kwargs)
        logger.info(books)
    else:
        logger.warning(f"Unknown operation: {operation}")
        sys.exit(1)


if __name__ == "__main__":
    main()
