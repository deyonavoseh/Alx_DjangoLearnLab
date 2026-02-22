from django.db import models


class Author(models.Model):
    """
    Represents a book author.
    One author can have many books (one-to-many relationship).
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book.
    Linked to Author via ForeignKey — one author, many books.
    related_name='books' allows reverse lookup: author.books.all()
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
