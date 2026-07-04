import { useState } from 'react';
import Button from './Button.jsx';
import Overview from './tabs/Overview.jsx';
import Work from './tabs/Work.jsx';
import Experience from './tabs/Experience.jsx';
import Testimonials from './tabs/Testimonials.jsx';
import AskAI from './tabs/AskAI.jsx';
import Contact from './tabs/Contact.jsx';
import { navItems } from '../data/portfolio.js';

/** Root portfolio island: profile header, sticky tab bar, and tab routing. */
export default function Portfolio() {
  const [view, setView] = useState('overview');

  return (
    <div className="portfolio">
      <header className="profile">
        <div className="profile__avatar-ring">
          <img
            className="profile__avatar"
            src="/assets/headshot.jpeg"
            alt="Charles Coonce"
            width="156"
            height="156"
          />
        </div>
        <div className="profile__text">
          <p className="profile__hello">Hello, I&rsquo;m</p>
          <h1 className="profile__name">Charles Coonce</h1>
          <p className="profile__role">
            Analyst · Analytics Engineer · Solutions Architect @ Clearway Energy
          </p>
          <p className="profile__bio">
            I build scalable data pipelines, turn raw data into clear visual insights, and help teams
            make informed decisions.
          </p>
          <div className="profile__actions">
            <Button
              as="a"
              href="https://github.com/cdcoonce"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </Button>
            <Button
              as="a"
              href="/assets/CharlesCoonce_Resume.pdf"
              target="_blank"
              rel="noopener noreferrer"
              variant="ghost"
            >
              Resume
            </Button>
            <div className="profile__socials">
              <a href="mailto:CharlesCoonce@Gmail.com" aria-label="Email Charles Coonce">
                <img src="/assets/mailicon.png" alt="" width="28" height="28" />
              </a>
              <a
                href="https://www.linkedin.com/in/charlesdcoonce/"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Charles Coonce on LinkedIn"
              >
                <img src="/assets/linkedinicon.png" alt="" width="28" height="28" />
              </a>
            </div>
          </div>
        </div>
      </header>

      <nav className="tabbar" aria-label="Portfolio sections">
        {navItems.map((n) => (
          <button
            key={n.key}
            className={`tabbar__tab${view === n.key ? ' tabbar__tab--active' : ''}`}
            aria-current={view === n.key ? 'page' : undefined}
            onClick={() => setView(n.key)}
          >
            {n.label}
          </button>
        ))}
      </nav>

      <div className="tabpanel">
        {view === 'overview' && <Overview onSeeWork={() => setView('work')} />}
        {view === 'work' && <Work />}
        {view === 'experience' && <Experience />}
        {view === 'testimonials' && <Testimonials />}
        {view === 'ai' && <AskAI />}
        {view === 'contact' && <Contact />}
      </div>

      <footer className="site-footer">
        <p>Copyright © 2026 Charles Coonce. All Rights Reserved.</p>
      </footer>
    </div>
  );
}
