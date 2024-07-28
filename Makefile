# Makefile для управления Celery

# Название вашего проекта
PROJECT_NAME = scrappy

# Команды для запуска
CELERY = celery -A celery_app


# Цели
.PHONY: all worker clean

all: worker

worker:
	@echo "Запуск worker..."
	$(CELERY) worker --beat --loglevel=info


clean:
	@echo "Остановка всех процессов..."
	# Здесь можно добавить команды для остановки процессов, если это необходимо


