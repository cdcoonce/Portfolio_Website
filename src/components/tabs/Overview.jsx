import Button from '../Button.jsx';
import Tag from '../Tag.jsx';
import { metrics, projects } from '../../data/portfolio.js';

/** Overview tab: at-a-glance metrics + a featured project spotlight. */
export default function Overview({ onSeeWork }) {
  const featured = projects[0];
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
        <div className="eyebrow">Featured project</div>
        <div className="featured">
          <img
            className="featured__img"
            src={featured.image}
            alt={featured.title}
            loading="lazy"
          />
          <div className="featured__body">
            <h3 className="featured__title">{featured.title}</h3>
            <p className="featured__desc">{featured.description}</p>
            <div className="featured__tags">
              {featured.tags.slice(0, 2).map((t) => (
                <Tag key={t}>{t}</Tag>
              ))}
            </div>
            <Button size="sm" onClick={onSeeWork} className="featured__cta">
              See all work
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
