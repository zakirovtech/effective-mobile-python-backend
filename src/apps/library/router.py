from apps.library.controllers import BookController

book_controller = BookController()

operations_routing = {
    "add": book_controller.create,
    "delete": book_controller.delete,
    "search": book_controller.search,
    "view_all": book_controller.get_all,
    "change_status": book_controller.change_status
}
