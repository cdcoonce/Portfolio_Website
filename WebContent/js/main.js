'use strict';

import { initFilter, getFilterFromURL } from './filter.js';
import { initCarousel } from './carousel.js';
import { initChat } from './chat.js';
import { projects, tags, TAG_LABELS, TAG_CATEGORIES } from './projects.js';
import { renderProjectCards, renderFilterButtons } from './renderer.js';

/**
 * Application entry point.
 * Initializes all interactive components after DOM is ready.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Copyright year (moved from inline script — Phase 1 Step 4)
  const yearSpan = document.getElementById('copyright-year');
  if (yearSpan) yearSpan.textContent = new Date().getFullYear();

  // Navigation — hamburger toggle
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen);
    });

    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Back to top button
  const backToTop = document.querySelector('.back-to-top');
  const testimonials = document.querySelector('#testimonials');

  if (backToTop) {
    window.addEventListener('scroll', () => {
      const testimonialsTop = testimonials ? testimonials.getBoundingClientRect().top : Infinity;
      backToTop.classList.toggle('visible', testimonialsTop <= window.innerHeight);
    });

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Scroll-down button
  const scrollDown = document.querySelector('.scroll-down');
  const profileSection = document.querySelector('#profile');

  if (scrollDown && profileSection) {
    window.addEventListener('scroll', () => {
      const profileBottom = profileSection.getBoundingClientRect().bottom;
      scrollDown.classList.toggle('hidden', profileBottom < 0);
    });

    scrollDown.addEventListener('click', () => {
      const skills = document.querySelector('#skills');
      const nav = document.querySelector('#main-nav');
      const navHeight = nav ? nav.offsetHeight : 0;
      window.scrollTo({ top: skills.offsetTop - navHeight, behavior: 'smooth' });
    });
  }

  // Render project cards from data module
  const grid = document.querySelector('.projects-grid');
  if (grid) {
    renderProjectCards(grid, projects);
  } else {
    console.warn('projects-grid container not found');
  }

  // Render filter buttons from derived tag registry
  const filterContainer = document.getElementById('filter-buttons');
  if (filterContainer) {
    renderFilterButtons(filterContainer, tags, TAG_CATEGORIES, { labels: TAG_LABELS });
  }

  // Page-aware initialization
  const page = document.body.dataset.page;
  const knownTags = new Set(tags);

  if (page === 'projects') {
    initFilter({
      maxVisible: null,
      defaultFilter: 'all',
      initialFilter: getFilterFromURL(),
      knownTags,
    });
  } else {
    initFilter({
      maxVisible: 4,
      defaultFilter: 'featured',
      knownTags,
    });
    initCarousel();
    initChat();
  }
});
