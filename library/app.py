from repository.book import BookRep
from ui.console import ConsolePrinter
from service.state import StateManager, States


class App:
    @staticmethod
    def run():
        book_rep = BookRep()

        ConsolePrinter.clear()

        state_manager = StateManager(book_rep)
        state_manager.state_changed.add_listener(ConsolePrinter.draw_ui)
        state_manager.change_state(States.Main)

        while state_manager.is_work:
            state_manager.current_state.handle_input(state_manager)
