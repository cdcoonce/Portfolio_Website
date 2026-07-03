import { useEffect, useRef, useState } from 'react';
import Button from '../Button.jsx';
import { presetGroups } from '../../data/portfolio.js';
import {
  getRemainingRequests,
  isRateLimited,
  recordRequest,
  renderAssistantMarkdown,
  sendMessage,
} from '../../lib/chat.js';

const GREETING = {
  role: 'assistant',
  content: "Hi! I'm Charles's AI assistant. Ask me about his projects, skills, or experience.",
};

/**
 * Ask AI tab: suggested-topic sidebar + chat panel wired to the live Lambda
 * assistant. Rate limiting mirrors the previous site (25 questions / hour).
 */
export default function AskAI() {
  const [messages, setMessages] = useState([GREETING]);
  const [draft, setDraft] = useState('');
  const [typing, setTyping] = useState(false);
  const [notice, setNotice] = useState('');
  const [locked, setLocked] = useState(false);
  const scrollRef = useRef(null);
  const busyRef = useRef(false);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, typing]);

  const refreshNotice = () => {
    const remaining = getRemainingRequests();
    if (remaining === 0) {
      setNotice('Rate limit reached. Please try again later.');
      setLocked(true);
    } else if (remaining <= 3) {
      setNotice(`${remaining} question${remaining === 1 ? '' : 's'} remaining this hour`);
    } else {
      setNotice('');
    }
  };

  useEffect(refreshNotice, []);

  const ask = async (text) => {
    const question = text.trim();
    if (!question || busyRef.current) return;
    if (isRateLimited()) {
      refreshNotice();
      return;
    }

    busyRef.current = true;
    setDraft('');
    setTyping(true);
    const history = [...messages, { role: 'user', content: question }];
    setMessages(history);

    try {
      recordRequest();
      const reply = await sendMessage(history);
      setMessages((m) => [...m, { role: 'assistant', content: reply }]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: 'assistant', content: 'Sorry, something went wrong. Please try again.' },
      ]);
    } finally {
      busyRef.current = false;
      setTyping(false);
      refreshNotice();
    }
  };

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      ask(draft);
    }
  };

  return (
    <div className="askai">
      <aside className="askai__sidebar">
        <div className="askai__sidebar-title">Suggested topics</div>
        {presetGroups.map((g) => (
          <div className="askai__group" key={g.category}>
            <div className="askai__group-name">{g.category}</div>
            <div className="askai__group-items">
              {g.items.map((label) => (
                <button
                  key={label}
                  className="askai__preset"
                  onClick={() => ask(label)}
                  disabled={locked}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </aside>

      <div className="askai__panel">
        <div className="askai__header">
          <div className="askai__mark" aria-hidden="true">
            ✦
          </div>
          <div>
            <div className="askai__name">Charles&rsquo;s AI assistant</div>
            <div className="askai__sub">Trained on my projects, skills &amp; experience</div>
          </div>
          <span className="askai__status">
            <span className="askai__status-dot" aria-hidden="true" />
            Online
          </span>
        </div>

        <div className="askai__messages" ref={scrollRef} aria-live="polite" role="log">
          {messages.map((m, i) => (
            <div className={`msg msg--${m.role}`} key={`${m.role}-${i}`}>
              {m.role === 'assistant' && (
                <div className="msg__avatar" aria-hidden="true">
                  ✦
                </div>
              )}
              {m.role === 'assistant' ? (
                <div
                  className="bubble bubble--assistant"
                  dangerouslySetInnerHTML={{ __html: renderAssistantMarkdown(m.content) }}
                />
              ) : (
                <div className="bubble bubble--user">{m.content}</div>
              )}
            </div>
          ))}
          {typing && (
            <div className="msg msg--assistant">
              <div className="msg__avatar" aria-hidden="true">
                ✦
              </div>
              <div className="bubble bubble--assistant typing" aria-label="Assistant is typing">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}
        </div>

        <div className="askai__composer">
          <div className="askai__input-row">
            <input
              className="askai__input"
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={onKeyDown}
              placeholder="Ask about Charles's projects, skills, or experience…"
              aria-label="Ask the assistant a question"
              maxLength={1000}
              autoComplete="off"
              disabled={locked}
            />
            <Button size="sm" onClick={() => ask(draft)} disabled={locked}>
              Send
            </Button>
          </div>
          <p className="askai__hint">
            {notice || 'Press Enter to send · answers from my live assistant.'}
          </p>
        </div>
      </div>
    </div>
  );
}
