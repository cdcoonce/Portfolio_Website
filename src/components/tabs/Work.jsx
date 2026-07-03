import ProjectCard from '../ProjectCard.jsx';
import { projects } from '../../data/portfolio.js';

/** Work tab: responsive grid of project cards. */
export default function Work() {
  return (
    <div className="work-grid">
      {projects.map((p) => (
        <ProjectCard key={p.title} project={p} />
      ))}
    </div>
  );
}
