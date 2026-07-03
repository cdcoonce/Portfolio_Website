import Button from '../Button.jsx';

/** Contact tab: short prompt + primary/secondary reach-out buttons. */
export default function Contact() {
  return (
    <div className="contact">
      <p className="contact__lead">
        Interested in working together or have a question? Reach out below and I&rsquo;ll get
        back to you.
      </p>
      <div className="contact__actions">
        <Button as="a" href="mailto:CharlesCoonce@Gmail.com">
          Email Me
        </Button>
        <Button
          as="a"
          href="https://www.linkedin.com/in/charlesdcoonce/"
          target="_blank"
          rel="noopener noreferrer"
          variant="ghost"
        >
          LinkedIn
        </Button>
        <Button
          as="a"
          href="https://github.com/cdcoonce"
          target="_blank"
          rel="noopener noreferrer"
          variant="ghost"
        >
          GitHub
        </Button>
      </div>
    </div>
  );
}
