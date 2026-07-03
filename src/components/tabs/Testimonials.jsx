import { useState } from 'react';
import { testimonials } from '../../data/portfolio.js';
import { initials, nextIndex, prevIndex } from '../../lib/carousel.js';

/**
 * Testimonial avatar. Shows a locally-hosted headshot when `photo` is set,
 * otherwise the author's initials. When `linkedin` is set, the avatar becomes
 * a link to that profile.
 */
function Avatar({ person }) {
  const { author, photo, linkedin } = person;
  const inner = photo ? (
    <img className="testimonial-card__photo" src={photo} alt={author} />
  ) : (
    <span aria-hidden="true">{initials(author)}</span>
  );

  if (linkedin) {
    return (
      <a
        className="testimonial-card__avatar testimonial-card__avatar--link"
        href={linkedin}
        target="_blank"
        rel="noopener noreferrer"
        aria-label={`${author} on LinkedIn — opens in a new tab`}
      >
        {inner}
      </a>
    );
  }
  return <div className="testimonial-card__avatar">{inner}</div>;
}

/** Testimonials tab: single-quote carousel with segment dots + prev/next. */
export default function Testimonials() {
  const [index, setIndex] = useState(0);
  const current = testimonials[index];

  return (
    <div className="testimonials">
      <div className="testimonial-card">
        <div className="testimonial-card__mark" aria-hidden="true">
          &ldquo;
        </div>
        <blockquote className="testimonial-card__quote">{current.quote}</blockquote>
        <div className="testimonial-card__footer">
          <div className="testimonial-card__person">
            <Avatar person={current} />
            <div>
              <div className="testimonial-card__author">{current.author}</div>
              <div className="testimonial-card__meta">
                {current.job}, {current.company}
              </div>
            </div>
          </div>
          <div className="testimonial-card__controls">
            <div className="testimonial-card__dots">
              {testimonials.map((t, i) => (
                <button
                  key={t.author}
                  className={`dot${i === index ? ' dot--active' : ''}`}
                  aria-label={`Go to testimonial ${i + 1}`}
                  aria-current={i === index}
                  onClick={() => setIndex(i)}
                />
              ))}
            </div>
            <div className="testimonial-card__arrows">
              <button
                className="arrow-btn"
                aria-label="Previous testimonial"
                onClick={() => setIndex((i) => prevIndex(i, testimonials.length))}
              >
                ❮
              </button>
              <button
                className="arrow-btn"
                aria-label="Next testimonial"
                onClick={() => setIndex((i) => nextIndex(i, testimonials.length))}
              >
                ❯
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
