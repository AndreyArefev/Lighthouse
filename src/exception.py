from fastapi import FastAPI, HTTPException


class CategoryNotExists(HTTPException):
    """Вызывается когда категория не создана"""
    pass
