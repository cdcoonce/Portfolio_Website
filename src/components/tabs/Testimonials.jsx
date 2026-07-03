import { useState } from 'react';
import { testimonials } from '../../data/portfolio.js';
import { initials, nextIndex, prevIndex } from '../../lib/carousel.js';

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
            <div className="testimonial-card__avatar" aria-hidden="true">
              {initials(current.author)}
            </div>
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
