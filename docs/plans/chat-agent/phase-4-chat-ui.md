# Phase 4: Chat UI (HTML + CSS, TDD)

## Goal

Add a chat agent section to the homepage HTML between Projects and Testimonials, with matching CSS styles. Follow TDD: write validation and E2E tests first, then implement the HTML and CSS to make them pass.

## Prerequisites

- Phase 1 complete (knowledge base exists for content cross-reference)
- Familiarity with the existing section structure in `index.html`

## Critical Files

- `index.html` — Insert new section (line 574-575 boundary)
- `WebContent/css/style.css` — Add chat styles (after line 476, Projects Footer section)
- `WebContent/css/mediaqueries.css` — Add responsive chat styles
- `tests/test_validation.py` — Add HTML structure tests
- `tests/test_chat.py` — New E2E test file

## Existing Patterns to Follow

### Section Pattern (from index.html)

Every section follows this pattern:

```html
<section id="section-name">
  <h2 class="section_text__p1">Section Title</h2>
  <!-- section content -->
</section>
```

### CSS Section Pattern (from style.css)

Sections use CSS custom properties defined in `:root`:

```css
--color-text-primary: #353535;
--color-text-secondary: rgb(85, 85, 85);
--color-bg-white: #fff;
--color-bg-light: #f9f9f9;
--color-bg-card-highlight: rgba(235, 241, 248, 0.4);
--color-accent-dark: rgb(53, 53, 53);
--color-border: rgb(53, 53, 53);
```

### Button Pattern (from style.css)

The site uses `.btn` and `.btn-color-1` classes:

```css
.btn {
  font-weight: 600;
  transition: all 300ms ease;
  padding: 1rem;
  width: 8rem;
  border-radius: 2rem;
  /* ... */
}

.btn-color-1 {
  border: rgb(53, 53, 53) 0.1rem solid;
  /* hover: white text on dark bg */
}
```

### Test Pattern (from tests/test_validation.py)

Validation tests use a `soup` fixture (BeautifulSoup on `index.html`) and are marked `@pytest.mark.validation`:

```python
@pytest.fixture(scope='module')
def soup():
    html = Path('index.html').read_text()
    return BeautifulSoup(html, 'html.parser')

@pytest.mark.validation
class TestHTMLValidation:
    def test_something(self, soup):
        ...
```

E2E tests use a `page` fixture (Playwright browser loaded with site) from `tests/conftest.py`:

```python
@pytest.fixture
def page(browser, server):
    page = browser.new_page()
    page.goto(server)
    yield page
    page.close()
```

---

## Step 1: Write Validation Tests (RED)

**Modify `tests/test_validation.py`** — Add a new test class after the existing `TestProjectsPageValidation` class (after line 165):

```python
@pytest.mark.validation
class TestChatSectionValidation:
    """Validate the chat agent section HTML structure."""

    def test_chat_section_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None, 'Missing <section id="chat-agent">'

    def test_chat_section_has_heading(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        h2 = section.find('h2')
        assert h2 is not None, 'Chat section missing <h2> heading'

    def test_chat_section_between_projects_and_testimonials(self, soup):
        sections = [s.get('id') for s in soup.find_all('section') if s.get('id')]
        assert 'chat-agent' in sections, 'chat-agent section not found'
        projects_idx = sections.index('projects')
        chat_idx = sections.index('chat-agent')
        testimonials_idx = sections.index('testimonials')
        assert projects_idx < chat_idx < testimonials_idx, (
            f'Section order wrong: projects={projects_idx}, chat={chat_idx}, testimonials={testimonials_idx}'
        )

    def test_chat_input_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        input_el = section.find('input', id='chat-input')
        assert input_el is not None, 'Missing chat input field'

    def test_chat_send_button_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        btn = section.find('button', id='chat-send')
        assert btn is not None, 'Missing chat send button'

    def test_chat_messages_container_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        messages = section.find('div', id='chat-messages')
        assert messages is not None, 'Missing chat messages container'

    def test_chat_input_has_aria_label(self, soup):
        input_el = soup.find('input', id='chat-input')
        assert input_el is not None
        assert input_el.get('aria-label'), 'Chat input missing aria-label'

    def test_chat_send_button_has_aria_label(self, soup):
        btn = soup.find('button', id='chat-send')
        assert btn is not None
        assert btn.get('aria-label'), 'Chat send button missing aria-label'
```

## Step 2: Write E2E Tests (RED)

**Create `tests/test_chat.py`**

```python
"""Chat agent section E2E tests — visibility and basic interaction."""

import pytest


@pytest.mark.e2e
class TestChatSectionE2E:
    def test_chat_section_visible(self, page):
        chat = page.locator('#chat-agent')
        assert chat.is_visible(), 'Chat section should be visible'

    def test_chat_input_is_focusable(self, page):
        page.click('#chat-input')
        focused = page.evaluate('document.activeElement.id')
        assert focused == 'chat-input'

    def test_chat_messages_area_exists(self, page):
        messages = page.locator('#chat-messages')
        assert messages.is_visible()

    def test_chat_has_welcome_message(self, page):
        first_msg = page.locator('#chat-messages .chat-message.assistant')
        assert first_msg.first.is_visible()
```

**Run tests — they should all FAIL (RED):**

```bash
uv run pytest tests/test_validation.py::TestChatSectionValidation tests/test_chat.py -v
```

---

## Step 3: Implement HTML (GREEN)

**Modify `index.html`** — Insert the chat section between line 574 (`</section>` closing projects) and line 575 (`<section id="testimonials">`).

The exact insertion point is after the closing `</section>` tag of the projects section and before the opening `<section id="testimonials">` tag.

Insert this HTML block:

```html
<section id="chat-agent">
  <div class="chat-container">
    <h2 class="section_text__p1">Ask Me Anything</h2>
    <p class="chat-subtitle">
      Have a question about my projects, skills, or experience? Ask my AI assistant.
    </p>
    <div id="chat-messages" class="chat-messages" aria-live="polite" role="log">
      <div class="chat-message assistant">
        <p>Hi! I'm Charles's AI assistant. Ask me about his projects, skills, or experience.</p>
      </div>
    </div>
    <div class="chat-input-row">
      <input
        type="text"
        id="chat-input"
        class="chat-input"
        placeholder="e.g., What projects use Python?"
        aria-label="Type your question"
        maxlength="1000"
        autocomplete="off"
      />
      <button id="chat-send" class="btn btn-color-1 chat-send" aria-label="Send message">
        Send
      </button>
    </div>
    <p id="chat-rate-limit" class="chat-rate-limit" hidden></p>
  </div>
</section>
```

**Also add a nav link** — In the `<ul class="nav-links">` (lines 41-47), add after the Projects link (line 44):

Current:

```html
<li><a href="#projects">Projects</a></li>
<li><a href="#testimonials">Testimonials</a></li>
```

Change to:

```html
<li><a href="#projects">Projects</a></li>
<li><a href="#chat-agent">Ask AI</a></li>
<li><a href="#testimonials">Testimonials</a></li>
```

---

## Step 4: Implement CSS

**Modify `WebContent/css/style.css`** — Add after the Projects Footer section (after the `.view-all-link` rule block, around line 476) and before the Testimonials Section comment (line 478):

```css
/* === Chat Agent Section === */

#chat-agent {
  padding: 2rem;
  background-color: var(--color-bg-white);
  max-width: 800px;
  margin: 2rem auto;
}

.chat-container {
  max-width: 700px;
  margin: 0 auto;
}

.chat-container h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary);
}

.chat-subtitle {
  margin-bottom: 1rem;
  font-size: 0.95rem;
  color: var(--color-text-secondary);
}

.chat-messages {
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 1rem;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  background-color: var(--color-bg-light);
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chat-message {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  max-width: 85%;
  line-height: 1.5;
}

.chat-message p {
  margin: 0;
}

.chat-message.user {
  background-color: var(--color-accent-dark);
  color: var(--color-bg-white);
  align-self: flex-end;
  border-bottom-right-radius: 2px;
}

.chat-message.user p {
  color: var(--color-bg-white);
}

.chat-message.assistant {
  background-color: var(--color-bg-card-highlight);
  align-self: flex-start;
  border-bottom-left-radius: 2px;
}

.chat-input-row {
  display: flex;
  gap: 0.5rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 2rem;
  font-family: inherit;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 300ms ease;
}

.chat-input:focus {
  border-color: var(--color-accent-black);
}

.chat-send {
  width: auto;
  padding: 0.75rem 1.5rem;
  white-space: nowrap;
}

.chat-rate-limit {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #c0392b;
  text-align: center;
}

/* Loading animation for waiting state */

.chat-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chat-loading-dots {
  display: inline-flex;
  gap: 4px;
}

.chat-loading-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--color-text-secondary);
  animation: chat-bounce 1.4s infinite ease-in-out both;
}

.chat-loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.chat-loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

.chat-loading-dots span:nth-child(3) {
  animation-delay: 0s;
}

@keyframes chat-bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
```

**Modify `WebContent/css/mediaqueries.css`** — Add responsive rules.

Inside the `@media (max-width: 700px)` block (after the Testimonials rules, before the closing `}`), add:

```css
/* === Chat Agent === */

.chat-container h2 {
  text-align: center;
}

.chat-subtitle {
  text-align: center;
}

.chat-message {
  max-width: 95%;
}
```

---

## Step 5: Run Tests Again (GREEN)

```bash
# Validation tests
uv run pytest tests/test_validation.py::TestChatSectionValidation -v

# E2E tests (requires Playwright)
uv run pytest tests/test_chat.py -v

# Also run ALL existing tests to ensure nothing broke
uv run pytest tests/ -m "not slow" -v
```

All tests should pass, including existing tests (the new section shouldn't break the 17 project card count, semantic structure tests, etc.).

## Step 6: Visual Verification

```bash
npm run serve
# Open http://localhost:8000 in browser
```

Verify:

1. Chat section appears between Projects and Testimonials
2. "Ask AI" appears in the navigation
3. The welcome message is displayed in the chat area
4. The input field and Send button are visible and styled consistently
5. On mobile (resize to < 700px): heading and subtitle are centered, messages take full width
6. The loading animation dots bounce correctly (test by temporarily adding the HTML)

## Output

After this phase:

- `index.html` has the `#chat-agent` section and nav link
- `WebContent/css/style.css` has chat section styles
- `WebContent/css/mediaqueries.css` has responsive chat styles
- `tests/test_validation.py` has `TestChatSectionValidation` (8 tests passing)
- `tests/test_chat.py` has `TestChatSectionE2E` (4 tests passing)
- Ready for Phase 5 (chat.js module)
