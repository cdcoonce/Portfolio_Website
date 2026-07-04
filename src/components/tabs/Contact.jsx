import { contactMethods } from '../../data/portfolio.js';

const isExternal = (href) => /^https?:\/\//.test(href || '');

/** Contact tab: low-key ways to reach out — card grid, no job-seeking framing. */
export default function Contact() {
  return (
    <div className="contact">
      <div className="contact__intro">
        <h2 className="contact__title">Get in touch</h2>
        <p className="contact__lead">
          Have a question about my work, a project you&rsquo;d like to talk through, or just want to
          connect? My inbox is open.
        </p>
      </div>
      <div className="contact__grid">
        {contactMethods.map((c) => (
          <a
            key={c.label}
            className="contact-card"
            href={c.href}
            {...(isExternal(c.href) ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
          >
            <div>
              <div className="contact-card__label">{c.label}</div>
              <div className="contact-card__value">{c.value}</div>
            </div>
            <span className="contact-card__arrow" aria-hidden="true">
              →
            </span>
          </a>
        ))}
      </div>
      <p className="contact__note">I typically respond within a day or two.</p>
    </div>
  );
}
