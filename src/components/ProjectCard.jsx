import Tag from './Tag.jsx';
import Cockpit from './Cockpit.jsx';

/** Project card: image header, date, title, description, tag row. Links out. */
export default function ProjectCard({ project }) {
  const { title, date, description, image, imageContain, slug, tags, href } = project;
  return (
    <a
      className="project-card"
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={`${title} — opens in a new tab`}
    >
      <div className="project-card__media">
        {slug ? (
          <Cockpit slug={slug} className="project-card__cockpit" />
        ) : (
          <img
            className={`project-card__img${imageContain ? ' project-card__img--contain' : ''}`}
            src={image}
            alt={title}
            loading="lazy"
          />
        )}
      </div>
      <div className="project-card__body">
        <span className="project-card__date">{date}</span>
        <h3 className="project-card__title">{title}</h3>
        <p className="project-card__desc">{description}</p>
        <div className="project-card__tags">
          {tags.map((t) => (
            <Tag key={t}>{t}</Tag>
          ))}
        </div>
      </div>
    </a>
  );
}
