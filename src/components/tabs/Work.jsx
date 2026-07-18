import { useState } from 'react';
import ProjectCard from '../ProjectCard.jsx';
import Button from '../Button.jsx';
import { projects } from '../../data/portfolio.js';
import { WORK_FILTERS, filterProjects, countFor } from '../../lib/work-filter.js';

const gallery = projects.filter((p) => !p.hideFromGallery);

/** Work tab: category rail + search on the left, filtered project grid on the right. */
export default function Work() {
  const [filter, setFilter] = useState('all');
  const [query, setQuery] = useState('');

  const filtered = filterProjects(gallery, { filter, query });
  const countLabel =
    filtered.length === gallery.length
      ? `Showing all ${gallery.length} projects`
      : `Showing ${filtered.length} of ${gallery.length} projects`;

  const clear = () => {
    setFilter('all');
    setQuery('');
  };

  return (
    <div className="work" data-testid="work">
      <aside className="work-rail">
        <div className="work-search">
          <span className="work-search__icon" aria-hidden="true">
            ⌕
          </span>
          <input
            className="work-search__input"
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search work…"
            aria-label="Search work"
            data-testid="work-search"
          />
        </div>
        <div>
          <div className="work-rail__heading">Category</div>
          <div className="work-rail__list">
            {WORK_FILTERS.map((f) => {
              const active = f.key === filter;
              return (
                <button
                  key={f.key}
                  className={`rail-item${active ? ' rail-item--active' : ''}`}
                  aria-pressed={active}
                  onClick={() => setFilter(f.key)}
                  data-testid={`rail-${f.key}`}
                >
                  <span>{f.label}</span>
                  <span className="rail-item__count">{countFor(gallery, f.key)}</span>
                </button>
              );
            })}
          </div>
        </div>
      </aside>

      <div className="work-main">
        <div className="work-count" data-testid="work-count">
          {countLabel}
        </div>
        {filtered.length > 0 ? (
          <div className="work-grid" data-testid="work-grid">
            {filtered.map((p) => (
              <ProjectCard key={p.title} project={p} />
            ))}
          </div>
        ) : (
          <div className="work-empty" data-testid="work-empty">
            <div className="work-empty__title">No projects match your search</div>
            <div className="work-empty__hint">Try a different keyword or clear the filters.</div>
            <Button variant="ghost" size="sm" onClick={clear} data-testid="work-clear">
              Clear filters
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
