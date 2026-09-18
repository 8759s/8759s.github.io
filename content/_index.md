---
# Leave the homepage title empty to use the site title
title: ""
date: 2022-10-24
type: landing
description: "Web security researcher at Palo Alto Networks. PhD from University of Toronto. Research in phishing detection, browser security, and AI-powered vulnerability management."

design:
  # Default section spacing
  spacing: "2rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      # Show a call-to-action button under your biography? (optional)
      # button:
      #   text: CV
      #   url: https://8759s.github.io/uploads/shawn_cv.pdf

  - block: service
    id: service
    content:
      title: Professional Activities
      subtitle: Program Committees
      years:
        - year: '2027'
          venues:
            - USENIX Security Symposium (USENIX Security)
        - year: '2026'
          venues:
            - Trustworthy AI for Good Workshop at the International Conference on Machine Learning (AI4Good @ ICML) [Organizing & Program Committee]
            - Trustworthy AI for Good Workshop at the Conference on Neural Information Processing Systems (AI4Good @ NeurIPS) [Organizing & Program Committee]
            - International Conference on Privacy, Security and Trust (PST)
            - Symposium on Electronic Crime Research (eCrime)
            - IEEE Transactions on Dependable and Secure Computing (TDSC)
        - year: '2025'
          collapsed: true
          venues:
            - IEEE Transactions on Dependable and Secure Computing (TDSC)

  - block: compact-news
    id: news
    content:
      title: News
      count: 3
      filters:
        folders:
          - research-posts
      order: desc
      archive:
        enable: true
        link: news/
        text: View all news
  # - block: collection
  #   id: papers
  #   content:
  #     title: Featured Publications
  #     filters:
  #       folders:
  #         - publication
  #       featured_only: true
  #   design:
  #     view: article-grid
  #     columns: 2
  # - block: collection
  #   content:
  #     title: Recent Publications
  #     text: ""
  #     filters:
  #       folders:
  #         - publication
  #       exclude_featured: false
  #   design:
  #     view: citation
  # - block: collection
  #   id: talks
  #   content:
  #     title: Recent & Upcoming Talks
  #     filters:
  #       folders:
  #         - event
  #   design:
  #     view: article-grid
  #     columns: 1
  # - block: collection
  #   id: news
  #   content:
  #     title: Recent News
  #     subtitle: ''
  #     text: ''
  #     # Page type to display. E.g. post, talk, publication...
  #     page_type: post
  #     # Choose how many pages you would like to display (0 = all pages)
  #     count: 5
  #     # Filter on criteria
  #     filters:
  #       author: ""
  #       category: ""
  #       tag: ""
  #       exclude_featured: false
  #       exclude_future: false
  #       exclude_past: false
  #       publication_type: ""
  #     # Choose how many pages you would like to offset by
  #     offset: 0
  #     # Page order: descending (desc) or ascending (asc) date.
  #     order: desc
  #   design:
  #     # Choose a layout view
  #     view: date-title-summary
  #     # Reduce spacing
  #     spacing:
  #       padding: [0, 0, 0, 0]
---
