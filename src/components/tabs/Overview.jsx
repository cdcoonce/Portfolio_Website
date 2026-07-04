import { useState } from 'react';
import Button from '../Button.jsx';
import Tag from '../Tag.jsx';
import Cockpit from '../Cockpit.jsx';
import { metrics, projects } from '../../data/portfolio.js';
import { featuredProjects } from '../../lib/featured.js';
import { nextIndex, prevIndex } from '../../lib/carousel.js';

const isExternal = (href) => /^https?:\/\//.test(href || '');

/** Overview tab: at-a-glance metrics + a rotating featured-project spotlight. */
export default function Overview() {
  const featured = featuredProjects(projects);
  const [index, setIndex] = useState(0);
  const current = featured[index] ?? projects[0];
  const hasMultiple = featured.length > 1;
  const external = isExternal(current.href);

  return (
    <div className="overview">
      <div className="metrics">
        {metrics.map((m) => (
          <div className="metric" key={m.label}>
            <div className="metric__value">{m.value}</div>
            <div className="metric__label">{m.label}</div>
          </div>
        ))}
      </div>

      <div>
        <div className="featured-head">
          <div className="eyebrow">Featured project</div>
          {hasMultiple && (
            <div className="featured-nav">
              <div className="featured-nav__dots">
                {featured.map((p, i) => (
                  <button
                    key={p.title}
                    className={`dot${i === index ? ' dot--active' : ''}`}
                    aria-label={`Show ${p.title}`}
                    aria-current={i === index}
                    onClick={() => setIndex(i)}
                  />
                ))}
              </div>
              <div className="featured-nav__arrows">
                <button
                  className="arrow-btn"
                  aria-label="Previous featured project"
                  onClick={() => setIndex((i) => prevIndex(i, featured.length))}
                >
                  ❮
                </button>
                <button
                  className="arrow-btn"
                  aria-label="Next featured project"
                  onClick={() => setIndex((i) => nextIndex(i, featured.length))}
                >
                  ❯
                </button>
              </div>
            </div>
          )}
        </div>
        <div className="featured">
          {current.slug ? (
            <Cockpit slug={current.slug} className="featured__cockpit" />
          ) : (
            <img className="featured__img" src={current.image} alt={current.title} loading="lazy" />
          )}
          <div className="featured__body">
            <h3 className="featured__title">{current.title}</h3>
            <p className="featured__desc">{current.description}</p>
            <div className="featured__tags">
              {current.tags.slice(0, 2).map((t) => (
                <Tag key={t}>{t}</Tag>
              ))}
            </div>
            {current.links?.length ? (
              <div className="featured__cta-group">
                {current.links.map((link, i) => (
                  <Button
                    key={link.href}
                    size="sm"
                    href={link.href}
                    variant={i === 0 ? 'primary' : 'ghost'}
                    {...(isExternal(link.href)
                      ? { target: '_blank', rel: 'noopener noreferrer' }
                      : {})}
                  >
                    {link.label}
                  </Button>
                ))}
              </div>
            ) : (
              <Button
                size="sm"
                href={current.href}
                className="featured__cta"
                {...(external ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
              >
                {current.ctaLabel ?? 'View repository'}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
