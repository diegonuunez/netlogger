from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header

from .connection_table import ConnectionTable
from .connection_parser import ConnectionParser

COLUMNS = ("Remote IP", "Port", "Status", "Process", "Service", "Domain")


class CLI(App):
    TITLE = "NetLogger"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]
    REFRESH_INTERVAL = 2.0

    def __init__(self) -> None:
        super().__init__()
        self.table = ConnectionTable(ConnectionParser())

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(zebra_stripes=True, cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        grid = self.query_one(DataTable)
        grid.add_columns(*COLUMNS)
        self.action_refresh()
        self.set_interval(self.REFRESH_INTERVAL, self.action_refresh)

    def action_refresh(self) -> None:
        self.table.refresh()
        self._render()

    def _render(self) -> None:
        grid = self.query_one(DataTable)
        grid.clear()
        fresh = {id(c) for c in self.table.new()}
        for c in self.table.all():
            style = "bold green" if id(c) in fresh else ""
            if c.status == "ESTABLISHED":
                grid.add_row(
                    Text(c.remote_ip, style=style),
                    Text(str(c.remote_port or ""), style=style),
                    Text(c.status, style=style),
                    Text(c.process, style=style),
                    Text(c.service, style=style),
                    Text(c.domain, style=style),
                )
        self.sub_title = f"{len(self.table.all())} conexiones"


def main() -> None:
    CLI().run()


if __name__ == "__main__":
    main()
