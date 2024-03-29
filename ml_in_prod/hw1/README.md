# Машинное обучение в продакшене. ДЗ 1

[Условия](./hw1.md)

[Ссылка на датасет](https://www.kaggle.com/datasets/cherngs/heart-disease-cleveland-uci)

### Установка необходимых библиотек:

```
pip3 install -r requirements.txt
```

### Генерация EDA отчёта (сохраняется в `reports`)
```
python3 -m visualize
```

### Обучение модели с дефолтным конфигом:
```
python3 -m src.train_pipeline
```

### Обучение модели с выбранным конфигом:
```
python3 -m src.train_pipeline +train_pipelines=forest_train_pipeline
```

### Инференс модели
```
python3 -m src.predict_pipeline
```

### Структура проекта
```
└─ ml_project
   ├─ README.md
   ├─ __init__.py
   ├─ configs
   │  ├─ default_predict_pipeline.yaml
   │  ├─ default_train_pipeline.yaml
   │  ├─ features
   │  │  └─ default.yaml
   │  ├─ model
   │  │  ├─ logistic_regression.yaml
   │  │  └─ random_forest.yaml
   │  ├─ preprocessing
   │  │  ├─ identity_transformer.yaml
   │  │  └─ one_hot_transformer.yaml
   │  ├─ split
   │  │  └─ default.yaml
   │  └─ train_pipelines
   │     ├─ forest_train_pipeline.yaml
   │     └─ lr_train_pipeline.yaml
   ├─ data
   │  └─ raw
   │     └─ heart_cleveland_upload.csv
   ├─ reports
   │  └─ EDA_pandas_profiling.html
   ├─ requirements.txt
   ├─ src
   │  ├─ __init__.py
   │  ├─ data
   │  │  ├─ __init__.py
   │  │  ├─ features_params.py
   │  │  ├─ make_dataset.py
   │  │  └─ split_params.py
   │  ├─ models
   │  │  ├─ __init__.py
   │  │  ├─ model_params.py
   │  │  ├─ predict_model.py
   │  │  └─ train_model.py
   │  ├─ predict_pipeline.py
   │  ├─ predict_pipeline_params.py
   │  ├─ preprocessing
   │  │  ├─ __init__.py
   │  │  ├─ preprocessing_params.py
   │  │  └─ transformers.py
   │  ├─ train_pipeline.py
   │  ├─ train_pipeline_params.py
   │  └─ utils.py
   └─ visualize.py
```

### Архитектурные и тактические решения:

- Созданы конфигурации для обучения логистической регрессии и случайного леса.
- Созданы тождественный и OneHot трансформеры.
- Созданы функции для генерации синтетических данных, но не были написаны тесты (не успел по времени, TDD-фанаты меня убьют). Данные генерируются равномерно в диапазоне между минимальным и максимальным значением данной фичи. Стратегия генерации разная для категориальных, непрерывных и дискретных величин.
- Отчет по анализу данных генерируется автоматически, используя `pandas-profiling`.
- Для конфигурирования использовалась `hydra`.
- Для сущностей из конфигов были написаны датаклассы (содержатся в файлах вида `*_params.py`).
- Не подключал хранилище для данных (данные хранятся в самом проекте в `data/raw`).
- Вывод логов, данных гидры, pickle-файлов моделей и json-файлов с метриками осуществляется в папку `artifacts`.


### Самооценка

0. В описании к пулл реквесту описаны основные "архитектурные" и тактические решения, которые сделаны в вашей работе. (1/1)
1. В пулл-реквесте проведена самооценка (1/1)
2. Выполнено EDA с использованием скрипта. (2	/2)
3. Написана функция/класс для тренировки модели, вызов оформлен как утилита командной строки, записана в readme инструкция по запуску (3/3)
4. Написана функция/класс predict (вызов оформлен как утилита командной строки), которая примет на вход артефакт/ы от обучения, тестовую выборку (без меток) и запишет предикт по заданному пути, инструкция по вызову записана в readme (3/3)
5. Проект имеет модульную структуру. (2/2)
6. Использованы логгеры (2/2)
7. Написаны тесты на отдельные модули и на прогон обучения и predict. (0/3)
8. Для тестов генерируются синтетические данные, приближенные к реальным. (2/2)
9. Обучение модели конфигурируется с помощью конфигов yaml. (3/3) 
10. Используются датаклассы для сущностей из конфига, а не голые dict (2/2)
11. Напишите кастомный трансформер и протестируйте его (2/3) (трансформеры написаны, а тестов нет)
12. В проекте зафиксированы все зависимости (1/1)
13. Настроен CI для прогона тестов, линтера на основе github actions (3/3).

Дополнительные баллы:
- Используйте hydra для конфигурирования (3/3)
- Mlflow не использовал (0/6)

