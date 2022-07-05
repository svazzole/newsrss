import os
from typing import List, Optional

from gnews import GNews
from rich import print
from rich.console import Group, group
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Footer, Header, ScrollView


@group()
def get_news_titles(titles):
    for tits in titles:
        yield Title(title=tits)


class Title(Widget):
    mouse_over = Reactive(False)

    def __init__(
        self,
        title: str,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.title = title

    def render(self):
        news_title = self.title.split(" - ")[0]
        source = self.title.split(" - ")[1]
        new_title = f"{source} ||| {news_title}"
        title_text = Text(
            new_title,
        )
        title_text.stylize("bold magenta", 0, len(source) + 2)
        title_text.stylize("bold white", len(source) + 2, len(source) + 3)
        title_text.stylize("bold magenta", len(source) + 3, len(source) + 4)
        return Panel(title_text, style=("on blue" if self.mouse_over else ""))

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False


class NewsTitles(Widget):
    def __init__(
        self,
        titles: List[str],
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.titles = titles

    def render(self):
        return Panel(get_news_titles(self.titles), title="Latest News")


class NewsArticle(Widget):
    def __init__(
        self,
        article: str,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.article = article

    def render(self):
        page = Text(text=self.article, end="")
        return Panel(page, title="Article", expand=True, style="white on black")


class NewsRSSApp(App):
    """An example of a very simple Textual App"""

    async def on_load(self) -> None:
        """Sent before going in to application mode."""
        # Bind our basic keys
        await self.bind("q", "quit", "Quit")

        try:
            self.titles, self.article = [
                "Titulo uni - Sorcio 1",
                "Titulo dui - Sorcio 2",
            ], "Ciccio pasticcio"  # get_news()  #
        except Exception:
            self.titles = ["Some error occurred"]

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""
        news_titles = NewsTitles(titles=self.titles)
        x = os.get_terminal_size()[0]

        await self.view.dock(Header(tall=False), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(ScrollView(news_titles), edge="top", size=percent(50, x))
        await self.view.dock(
            ScrollView(NewsArticle(name=None, article=self.article)),
            edge="bottom",
            size=percent(50, x),
        )


def percent(percent, total):
    return int(percent * total / 100)


def get_news():
    google_news = GNews()

    italy_news = google_news.get_news("IT")

    titles, urls = [], []
    for news in italy_news:
        titles.append(news.get("title", "No title to display"))
        urls.append(news.get("url"))

    # print(titles)
    # print(urls)
    article = google_news.get_full_article(urls[0])
    print(article.text)
    return titles, article.text


if __name__ == "__main__":
    NewsRSSApp.run(title="News Reader", log="textual.log")
    # get_news()
