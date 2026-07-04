/** Small pill tag used for skills and project technologies. */
export default function Tag({ children, className = '' }) {
  return <span className={`tag ${className}`.trim()}>{children}</span>;
}
