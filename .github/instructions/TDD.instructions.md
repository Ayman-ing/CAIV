---
name: TDD-Workflow
description: "Use when: Working on new features, bug fixes, or refactoring. Enforce Test-Driven Development approach: Write tests first before implementation."
applyTo: ["**/*.py", "**/*.ts", "**/*.vue"]
---

# Test-Driven Development (TDD) Workflow

## Core Principle
**Write tests FIRST, then implement code to pass those tests.**

## Workflow Steps

### 1. RED Phase - Write Failing Tests
- Start with the failing test
- Define what the code SHOULD do
- Test should fail initially (this is expected!)
- **Tools**: Use `test_` prefix for test files/functions
- **Location**: Place tests in `tests/` folder with matching structure

### 2. GREEN Phase - Implement Minimal Code
- Write the minimal code to make tests pass
- Don't over-engineer - just make it work
- Focus on passing the test, not on perfection
- **Check**: Run tests to verify they pass

### 3. REFACTOR Phase - Improve Code Quality
- Once tests pass, refactor for clarity/efficiency
- Tests act as safety net - refactor without fear
- Keep tests passing throughout
- **Avoid**: Changing functionality during refactor

## For This Project (CAIV)

### Backend (FastAPI/Python)
```
feature/
├── router.py          # API endpoints
├── schemas.py         # Pydantic models
├── service.py         # Business logic
├── repository.py      # Data access
├── models.py          # ORM models
└── tests/
    ├── test_router.py         # API tests (RED first!)
    ├── test_service.py        # Service tests
    └── test_repository.py     # Repository tests
```

**Test Pattern**:
```python
# 1. Write test first (RED)
def test_create_language_prevents_duplicates():
    # Setup, Execute, Assert
    pass

# 2. Implement to pass test (GREEN)
def create_language(profile_id, language):
    # Implementation here
    pass

# 3. Refactor if needed (REFACTOR)
```

### Frontend (Vue/TypeScript)
```
components/
├── profile/
│   ├── LanguageSection.vue
│   └── __tests__/
│       └── LanguageSection.spec.ts  # Tests BEFORE changes!
```

**Test Pattern**:
```typescript
// 1. Write test first
describe('LanguageSection', () => {
  it('should prevent duplicate languages', async () => {
    // Setup, Act, Assert
  })
})

// 2. Update component to pass test
// 3. Refactor component
```

## Commands to Always Use

### Backend
```bash
# Watch tests while developing
pytest tests/ -v --tb=short -x

# Run specific test
pytest tests/test_endpoints.py::TestLanguageCRUD::test_05_duplicate_prevention -v

# Coverage report
pytest tests/ --cov=features/profiles --cov-report=term-missing
```

### Frontend
```bash
# Run Vue tests
npm run test

# Watch mode
npm run test:watch
```

## TDD Benefits for CAIV
- ✅ Catches bugs early (before they reach production)
- ✅ Documents expected behavior (tests are living documentation)
- ✅ Safer refactoring (tests catch regressions instantly)
- ✅ Better design (tests expose design issues early)
- ✅ Confidence in deployments (high test coverage = high confidence)

## Common Mistakes to Avoid
❌ Writing tests AFTER implementation (defeats TDD purpose)
❌ Testing implementation details instead of behavior
❌ Writing vague test names ("test_works()")
❌ Skipping refactor phase (just leave working code as-is)
❌ Making tests too tightly coupled to implementation

## Required Test Coverage Levels
- **Critical features** (authentication, data validation, duplicate prevention): 100%
- **Business logic** (profile services, resume generation): 90%+
- **API endpoints**: 100% happy path + error cases
- **UI components**: 80%+ (focus on user interactions)

---
**Status**: Active for all CAIV development
**Applied to**: Backend (`*.py`), Frontend (`*.ts`, `*.vue`)
**Last Updated**: March 22, 2026
