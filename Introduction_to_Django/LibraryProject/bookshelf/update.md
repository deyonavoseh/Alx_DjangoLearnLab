# Update Operation
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(Book.objects.get(id=book.id))
# Output: Nineteen Eighty-Four by George Orwell (1949)
```
