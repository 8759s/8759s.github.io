---
# Leave the homepage title empty to use the site title
title: ""
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      # Show a call-to-action button under your biography? (optional)
      # button:
      #   text: Download CV
      #   url: https://docs.google.com/document/d/1ldJVn-KgAqguadPmfuXJR01J-toKCi7RZkMcUIMEeXQ/edit?usp=sharing
  - block: buttons
      cotnent: 
        buttons:
          - title: Download CV
            url: https://docs.google.com/document/d/1ldJVn-KgAqguadPmfuXJR01J-toKCi7RZkMcUIMEeXQ/edit?usp=sharing 
          - title: Download Resume
            url: https://docs.google.com/document/d/1nFI1ov0UeHxTUXksuZIgvXToLbcZqXzx/edit?usp=sharing&ouid=117630638173681529061&rtpof=true&sd=true
  - block: markdown
    content:
      title: 'My Research'
      subtitle: ''
      text: |-
        ###### Web Security
        Web security is a dynamic and evolving research area, where malicious actors continuously develop new methods to extract or exchange undesirable information from  clients, while detectors strive to identify such activities. This constant struggle represents an arms race. Reliable detection mechanisms benefit from the development of creative client-side tools that gather contextual information about web requests to identify undesirable information exchanges. My research projects, vWitness and Duumviri, exemplify this approach by using contextual data to detect and block undesirable activities. For instance, vWitness leverages user-provided inputs extracted from a series of screenshots leading to the generation of a request to uncover user-impersonating requests, while Duumviri the consequential effect of blocking a request to identify trackers. However, these are just the beginning --- there remains significant potential for further exploration into advanced contextual information, including browser state dynamics, fine-grained user interaction data, and even AI-powered behavioral models, to enhance web security.

        ###### Vulnerabilities
        Bugs in software systems are inevitable, and vulnerabilities (exploitable bugs) can have devastating consequences, such as data breaches, infrastructure failures, and financial losses, when exploited. Detecting, verifying, fixing vulnerabilities and validating their fixes is a resource-intensive process, requiring significant human expertise that is both time-consuming and prone to error. Large Language Models (LLMs) offer promising solutions by enhancing these tasks with human-like decision-making capabilities. For example, LLMs can detect early signs of emerging vulnerabilities (e.g., from social media activity like tweets), aggregate and synthesize information from diverse sources, assess a system's exploitability based on usage patterns, and even propose potential fixes. By integrating LLMs into the software security lifecycle, organizations can accelerate and improve the accuracy of vulnerability management, reducing the window of opportunity for exploitation.














        

       
    # design:
    #   columns: '1'
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
  - block: collection
    content:
      title: Recent Publications
      text: ""
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      view: citation
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
  - block: cta-card
    demo: true # Only display this section in the Hugo Blox Builder demo site
    content:
      title: 👉 Build your own academic website like this
      text: |-
        This site is generated by Hugo Blox Builder - the FREE, Hugo-based open source website builder trusted by 250,000+ academics like you.

        <a class="github-button" href="https://github.com/HugoBlox/hugo-blox-builder" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star HugoBlox/hugo-blox-builder on GitHub">Star</a>

        Easily build anything with blocks - no-code required!
        
        From landing pages, second brains, and courses to academic resumés, conferences, and tech blogs.
      button:
        text: Get Started
        url: https://hugoblox.com/templates/
    design:
      card:
        # Card background color (CSS class)
        css_class: "bg-primary-700"
        css_style: ""
---
