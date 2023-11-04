import math

class PagingInfo:
    def __init__(self, pageSize, pageCurrent, pageCount):
        #số lượng sản phẩm 1 trang
        self.pageSize = pageSize
        #Trang hiện tại
        self.pageCurrent = pageCurrent
        #Tổng sản phẩm
        self.pageCount = pageCount
        #tổng số page
        self.totalPage = int(math.ceil(pageCount/pageSize))

class BooksPaging:
    def __init__(self, paging, books):
            self.paging = paging
            self.books = books