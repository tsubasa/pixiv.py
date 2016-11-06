from __future__ import print_function

class Cursor(object):

    def __init__(self, method, *args, **kwargs):
        self.iterator = PageIterator(method, args, kwargs)

    def pages(self, limit=0):
        if limit > 0:
            self.iterator.limit = limit
        return self.iterator

    def items(self, limit=0):
        i = ItemIterator(self.iterator)
        i.limit = limit
        return i

class BaseIterator(object):

    def __init__(self, method, args, kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.limit = 0

    def __next__(self):
        return self.next()

    def next(self):
        raise NotImplementedError

    def prev(self):
        raise NotImplementedError

    def __iter__(self):
        return self

class PageIterator(BaseIterator):

    def __init__(self, method, args, kwargs):
        BaseIterator.__init__(self, method, args, kwargs)
        self.start_page = kwargs.pop('page', 0)
        self.current_page = self.start_page if self.start_page else 0
        self.next_page = self.start_page if self.start_page else 1

    def next(self):
        if self.limit > 0:
            if self.current_page > self.limit + self.start_page - 1:
                raise StopIteration

        items = self.method(pagination=True, page=self.next_page,
                            *self.args, **self.kwargs)
        if isinstance(items, tuple):
            items, cursors = items
        else:
            cursors = None
        if len(items) == 0:
            raise StopIteration
        if cursors and 'next' in cursors:
            self.next_page = int(cursors['next'])
        else:
            self.next_page += 1

        self.current_page += 1

        return items

class ItemIterator(BaseIterator):

    def __init__(self, page_iterator):
        self.page_iterator = page_iterator
        self.limit = 0
        self.current_page = None
        self.page_index = -1
        self.num_tweets = 0

    def next(self):
        if self.limit > 0:
            if self.num_tweets == self.limit:
                raise StopIteration
        if self.current_page is None or self.page_index == len(self.current_page) - 1:
            self.current_page = self.page_iterator.next()
            self.page_index = -1
        self.page_index += 1
        self.num_tweets += 1
        return self.current_page[self.page_index]

class AppCursor(object):

    def __init__(self, method, *args, **kwargs):
        self.iterator = AppPageIterator(method, args, kwargs)

    def pages(self, limit=0):
        if limit > 0:
            self.iterator.limit = limit
        return self.iterator

    def items(self, limit=0):
        i = ItemIterator(self.iterator)
        i.limit = limit
        return i

class AppPageIterator(BaseIterator):

    PER_PAGE = 30

    def __init__(self, method, args, kwargs):
        BaseIterator.__init__(self, method, args, kwargs)
        self.start_page = kwargs.pop('page', 0)
        self.current_page = self.start_page if self.start_page else 0
        self.next_offset = self.start_page * self.PER_PAGE if self.start_page else 0

    def next(self):
        if self.limit > 0:
            if self.current_page > self.limit + self.start_page - 1:
                raise StopIteration

        items = self.method(pagination=True, offset=self.next_offset,
                            *self.args, **self.kwargs)
        if isinstance(items, tuple):
            items, cursors = items
        else:
            cursors = None
        if len(items) == 0:
            raise StopIteration
        if cursors and 'offset' in cursors:
            self.next_offset = int(cursors['offset'])
        else:
            self.next_offset += self.PER_PAGE

        self.current_page += 1

        return items
