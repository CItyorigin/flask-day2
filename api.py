from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import BookSchema

# ✅ url_prefix를 "/"로 설정
blp = Blueprint("Books", "books", url_prefix="/", description="책 관련 API")

books = []
book_id_counter = 1

@blp.route("/")
class BookListResource(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        """모든 책 목록 반환"""
        return books

    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, new_data):
        """새 책 추가"""
        global book_id_counter
        new_data["id"] = book_id_counter
        book_id_counter += 1
        books.append(new_data)
        return new_data

@blp.route("/<int:book_id>")
class BookResource(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        """특정 책 조회"""
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            abort(404, message="책을 찾을 수 없습니다.")
        return book

    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, updated_data, book_id):
        """책 정보 업데이트"""
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            abort(404, message="책을 찾을 수 없습니다.")
        book.update(updated_data)
        book["id"] = book_id
        return book

    def delete(self, book_id):
        """책 삭제"""
        global books
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            abort(404, message="책을 찾을 수 없습니다.")
        books = [b for b in books if b["id"] != book_id]
        return {"message": "삭제되었습니다."}, 200
