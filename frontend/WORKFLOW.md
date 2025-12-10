# Workflow в TestOps-Copilot

## Архитектура State Machine

Фронтенд использует state machine для управления пользовательским потоком работы с LLM сервисом.

## Типы чатов

1. **UI Testing** - Тестирование веб-интерфейсов
2. **API Testing** - Тестирование API на основе OpenAPI спецификации
3. **General** - Общий чат (не использует workflow)

## Workflow Steps (WorkflowStep)

```typescript
type WorkflowStep = 
  | 'idle'           // Начальное состояние
  | 'generate-ui'    // Генерация UI тест-плана
  | 'generate-api'   // Генерация API тест-плана
  | 'redact'         // Редактирование контента
  | 'generate-code'  // Генерация Python кода
  | 'optimize'       // Оптимизация тестов
  | 'review'         // Ревью кода
  | 'complete'       // Завершено
```

## Пользовательский Flow

### UI Testing Flow

```
1. Выбор режима "UI Testing"
   └─> WorkflowStep: idle

2. Пользователь описывает проект (URL, описание, модули)
   └─> POST /api/v1/ai/generate-ui-tests
   └─> WorkflowStep: generate-ui
   └─> Сохранение тест-плана в workflowData.testPlan

3. Редактирование плана (loop)
   ├─> Пользователь просит правки: "Добавь тест на кнопку X"
   │   └─> POST /api/v1/ai/redact-content
   │   └─> Обновление workflowData.testPlan
   │   └─> Возврат к шагу 3
   │
   └─> Пользователь утверждает: "готово" | "ок" | "генерируй код"
       └─> POST /api/v1/ai/generate-code-pytest
       └─> WorkflowStep: complete
       └─> Сохранение кода в workflowData.code
```

### API Testing Flow

```
1. Выбор режима "API Testing"
   └─> WorkflowStep: idle

2. Пользователь загружает OpenAPI спецификацию (JSON/YAML)
   └─> POST /api/v1/ai/generate-api-tests (multipart/form-data)
   └─> WorkflowStep: generate-api
   └─> Сохранение тест-плана в workflowData.testPlan

3. Редактирование плана (loop)
   ├─> Пользователь просит правки: "Убери тесты на /admin"
   │   └─> POST /api/v1/ai/redact-content
   │   └─> Обновление workflowData.testPlan
   │   └─> Возврат к шагу 3
   │
   └─> Пользователь утверждает: "готово"
       └─> POST /api/v1/ai/generate-code-pytest
       └─> WorkflowStep: complete
       └─> Сохранение кода в workflowData.code
```

## Индикатор Workflow

В верхней части `ChatArea` отображается индикатор текущего шага:

- 🎯 **Шаг 1**: Опишите проект для генерации тест-плана
- 📝 **Шаг 2**: Редактируйте план или напишите "готово" для генерации кода
- ⚙️ Генерация кода...
- ✅ Работа завершена! Можете создать новый чат

## API Endpoints

### Health Check
```http
GET /api/v1/ping
Response: 200 OK
```

### Generate UI Tests
```http
POST /api/v1/ai/generate-ui-tests
Content-Type: application/json

{
  "url": "https://example.com",
  "general_description": "Описание проекта",
  "modules": "Список модулей",
  "buttons_description": "Описание кнопок",
  "special_scenarios": "Специальные сценарии"
}

Response: { "message": "# Тест-план в Markdown" }
```

### Generate API Tests
```http
POST /api/v1/ai/generate-api-tests
Content-Type: multipart/form-data

file: openapi.json
general_description: "Описание API"
modules: "Модули для тестирования"

Response: { "message": "# Тест-план в Markdown" }
```

### Redact Content
```http
POST /api/v1/ai/redact-content
Content-Type: application/json

{
  "original_content": "Исходный тест-план",
  "edit_instructions": "Добавь тест на авторизацию"
}

Response: { "message": "# Обновлённый тест-план" }
```

### Generate Code Pytest
```http
POST /api/v1/ai/generate-code-pytest
Content-Type: application/json

{
  "url": "https://example.com",
  "general_description": "Описание",
  "approved_test_plan": "# Утверждённый тест-план"
}

Response: { "message": "```python\n# Generated code\n```" }
```

### Optimize Tests
```http
POST /api/v1/ai/optimize-tests
Content-Type: application/json

{
  "modules": "Модули",
  "test_cases": "Тест-кейсы для оптимизации"
}

Response: { "message": "# Оптимизированные тесты" }
```

### Review Code
```http
POST /api/v1/ai/review-code
Content-Type: application/json

{
  "code_snippet": "def test_example():\n    pass",
  "rules": "Стандарты TestOps"
}

Response: { "message": "# Результаты ревью" }
```

## Хранение State

Весь workflow state хранится в Pinia store (`appStore.ts`):

```typescript
interface ChatHistory {
  id: string
  title: string
  type: 'ui' | 'api' | 'general'
  messages: Message[]
  workflowStep: WorkflowStep
  workflowData: {
    testPlan?: string    // Сгенерированный/отредактированный план
    code?: string        // Финальный код
    lastStep?: WorkflowStep
  }
}
```

State сохраняется в `localStorage` под ключом `testops-chat-history`.

## Утверждение тест-плана

Функция `isApprovalMessage()` распознаёт следующие ключевые слова:
- готово
- ок
- да
- утверждаю
- одобряю
- генерируй код
- давай код
- кодом

## Обработка ошибок

Все API запросы обрабатываются через `safeFetch()` в `utils/api.ts`:
- Показывает уведомления Quasar при ошибках
- Обрабатывает network failures
- Парсит JSON ответы с `{message: "..."}`

## Визуальные подсказки

После каждого ответа бот добавляет подсказки:

```markdown
---
**Вы можете:**
- Попросить отредактировать план
- Написать "готово" для генерации кода
```

Или в состоянии `complete`:

```markdown
✅ **Код сгенерирован!** Можете начать новый чат для другого проекта.
```
