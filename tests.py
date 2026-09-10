import pytest


class TestBooksCollector:


    @pytest.mark.parametrize("name", [
        "Первая",
        "Вторая книга с названием из ровно 40 сим",
        "Книга №3",
    ])
    def test_add_new_book_valid_name_added(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.get_books_genre()


    @pytest.mark.parametrize("name", ["", "Вторая книга с названием из больше 40 символов"])
    def test_add_new_book_invalid_name_not_added(self, collector, name):
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()


    def test_add_new_book_duplicate_not_added_twice(self, collector):
        collector.add_new_book("Повтор")
        collector.add_new_book("Повтор")
        assert list(collector.get_books_genre().keys()).count("Повтор") == 1


    def test_add_new_book_has_no_genre(self, collector):
        collector.add_new_book("БезЖанра")
        assert collector.get_book_genre("БезЖанра") == ""


    @pytest.mark.parametrize("genre", ["Фантастика", "Мультфильмы", "Комедии"])
    def test_set_book_genre_valid_genre_set(self, collector, genre):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)
        assert collector.get_book_genre("Книга") == genre


    @pytest.mark.parametrize("name,genre", [
        ("НетКниги", "Фантастика"),
        ("Книга", "Антиутопия"),
    ])
    def test_set_book_genre_invalid_not_set(self, collector, name, genre):
        collector.add_new_book("Книга")
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre("Книга") == ""


    def test_get_books_with_specific_genre_returns_only_matching(self, collector):
        collector.add_new_book("Книга6")
        collector.add_new_book("Книга7")
        collector.add_new_book("Книга8")
        collector.set_book_genre("Книга6", "Фантастика")
        collector.set_book_genre("Книга7", "Детективы")
        collector.set_book_genre("Книга8", "Фантастика")
        assert set(collector.get_books_with_specific_genre("Фантастика")) == {"Книга6", "Книга8"}


    @pytest.mark.parametrize("genre,expected", [
        ("Мультфильмы", True),
        ("Комедии", True),
        ("Ужасы", False),
        ("Детективы", False),
    ])
    def test_get_books_for_children(self, collector, genre, expected):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)
        assert ("Книга" in collector.get_books_for_children()) == expected


    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book("Избранное")
        collector.add_book_in_favorites("Избранное")
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Избранное"]


    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book("Избранное")
        collector.add_book_in_favorites("Избранное")
        assert "Избранное" in collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites("Избранное")
        favorites = collector.get_list_of_favorites_books()
        assert favorites == []


    def test_add_book_in_favorites_duplicate_and_missing_book(self, collector):
        collector.add_new_book("КнигаЕсть")
        collector.add_book_in_favorites("КнигаЕсть")
        collector.add_book_in_favorites("КнигаЕсть")
        collector.add_book_in_favorites("НетКниги")
        assert collector.get_list_of_favorites_books().count("КнигаЕсть") == 1
        assert "НетКниги" not in collector.get_list_of_favorites_books()
