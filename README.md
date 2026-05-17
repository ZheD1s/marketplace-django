# Marketplace API

REST API маркетплейса на Django REST Framework.

---

## 🚀 Возможности проекта

### 👤 Аутентификация
- JWT авторизация
- Получение access/refresh токенов
- Обновление access token

### 📦 Products
- Создание товаров
- Просмотр списка товаров
- Детальная информация о товаре
- Обновление товара
- Удаление товара
- Поиск товаров
- Фильтрация товаров

### 🛒 Cart
- Просмотр корзины
- Добавление товара в корзину
- Изменение количества товара
- Удаление товара из корзины
- Очистка корзины

### 📋 Orders
- Создание заказа из корзины
- Просмотр списка заказов
- Детальный просмотр заказа
- Изменение статуса заказа

### 🔒 Permissions
- Только владелец может изменять товар
- Только авторизованные пользователи работают с корзиной и заказами

---

## ⚙️ Технологии

- Python 3
- Django
- Django REST Framework
- JWT Authentication
- PostgreSQL
- drf-yasg (Swagger)

---

## 📚 Swagger документация

http://127.0.0.1:8000/swagger/

---

## 🔑 JWT Авторизация

### Получение токена

**POST**
/api/token/

### Body:

```json
{
    "email": "example@example.com",
    "password": "1234"
}
``` 
---
## 🛒 Основные endpoints

### Products
| Method | Endpoint            |
| ------ | ------------------- |
| GET    | /api/products/      |
| POST   | /api/products/      |
| GET    | /api/products/{id}/ |
| PATCH  | /api/products/{id}/ |
| DELETE | /api/products/{id}/ |

### Cart
| Method | Endpoint                   |
| ------ | -------------------------- |
| GET    | /api/products/cart/        |
| POST   | /api/products/cart/add/    |
| PATCH  | /api/products/cart/update/ |
| DELETE | /api/products/cart/remove/ |
| DELETE | /api/products/cart/clear/  |

### Orders
| Method | Endpoint                          |
| ------ | --------------------------------- |
| POST   | /api/products/orders/create/      |
| GET    | /api/products/orders/             |
| GET    | /api/products/orders/{id}/        |
| PATCH  | /api/products/orders/{id}/status/ |

## ▶️ Запуск проекта
1. Клонировать проект
git clone <repo_url>

2. Создать venv
python -m venv venv

3. Активировать venv
Windows: 
venv\Scripts\activate

4. Установить зависимости
pip install -r requirements.txt

5. Миграции
python manage.py migrate

6. Запуск сервера
python manage.py runserver

### 👨‍💻 Автор
Dias Zhetpisov