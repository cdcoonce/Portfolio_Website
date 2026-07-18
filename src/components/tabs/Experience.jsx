import Tag from '../Tag.jsx';
import { experience, skills } from '../../data/portfolio.js';

/** Experience tab: timeline of roles + categorized skill tags. */
export default function Experience() {
  return (
    <div className="experience" data-testid="experience">
      <div>
        <h3 className="col-heading">Experience</h3>
        <div className="timeline" data-testid="timeline">
          {experience.map((x) => (
            <div className="timeline__row" key={x.role} data-testid="timeline-row">
              <div className="timeline__period">{x.period}</div>
              <div className="timeline__entry">
                <span className="timeline__dot" aria-hidden="true" />
                <div className="timeline__role">{x.role}</div>
                <div className="timeline__org">{x.org}</div>
                <div className="timeline__note">{x.note}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="col-heading">Skills &amp; Tools</h3>
        <div className="skills" data-testid="skills">
          {skills.map((cat) => (
            <div className="skills__cat" key={cat.name} data-testid="skills-cat">
              <div className="skills__cat-name">{cat.name}</div>
              <div className="skills__tags">
                {cat.tags.map((t) => (
                  <Tag key={t}>{t}</Tag>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
