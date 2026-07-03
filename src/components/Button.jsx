/**
 * Pill button — the signature control shape.
 * variant: 'primary' (dark fill) | 'ghost' (outline). size: 'md' | 'sm'.
 * Renders as <a> when `href` is provided, otherwise <button>.
 */
export default function Button({
  as,
  href,
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  ...rest
}) {
  const classes = [
    'btn',
    `btn--${variant}`,
    size === 'sm' ? 'btn--sm' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  const Tag = as || (href ? 'a' : 'button');
  const tagProps = Tag === 'a' ? { href } : { type: rest.type || 'button' };

  return (
    <Tag className={classes} {...tagProps} {...rest}>
      {children}
    </Tag>
  );
}
