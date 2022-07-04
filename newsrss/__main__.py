import os
from typing import Optional

from gnews import GNews
from rich import print
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, Placeholder, ScrollView


class NewsTitles(Widget):
    def __init__(self, name: Optional[str] = None, titles=None) -> None:
        super().__init__(name=name)
        self.titles = titles

    def render(self):
        page = Text(end="")
        for title in self.titles:
            page.append_text(Text(title))
            page.append_text(Text("\n\n"))

        page.append_text(Text("<- Prev Page 0/0 Next ->"))
        return Panel(page, title="News", expand=False)


class NewsArticle(Widget):
    def __init__(self, name: Optional[str] = None, article=None) -> None:
        super().__init__(name=name)
        self.article = article

    def render(self):
        page = Text(text=self.article, end="")
        return Panel(page, title="Article", expand=False)


class NewsRSSApp(App):
    """An example of a very simple Textual App"""

    async def on_load(self) -> None:
        """Sent before going in to application mode."""
        # Bind our basic keys
        await self.bind("q", "quit", "Quit")

        try:
            self.titles, self.article = get_news()  # ["Titulo uni", "Titulo dui"]
        except Exception:
            self.titles = ["Some error occurred"]

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""
        news_titles = NewsTitles(titles=self.titles)
        x = os.get_terminal_size()[0]
        print(x)
        # await self.view.dock(Header(tall=False), edge="top")
        # await self.view.dock(Footer(), edge="bottom")
        # await self.view.dock(ScrollView(news_titles), edge="left")
        # await self.view.dock(Placeholder(name="Placeholder for text"), edge="right")

        await self.view.dock(Header(tall=False), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(ScrollView(news_titles), edge="left", size=percent(50, x))
        await self.view.dock(
            NewsArticle(name=None, article=self.article),
            edge="right",
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
