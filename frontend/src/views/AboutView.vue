<template>
  <div class="about">
    <h1>About ContextDB</h1>
    <section>
      <h2>Overview</h2>
      <p>ContextDB is a cutting-edge application designed to empower large language models (LLMs) with up-to-date context on various tools and frameworks. By providing the latest information on technologies like React, FastAPI, Vue.js, and more, ContextDB enables LLMs to generate more accurate and relevant responses.</p>
    </section>
    <section>
      <h2>Key Features</h2>
      <ul>
        <li><strong>Documentation Downloads:</strong> Easily download and update documentation for various technologies.</li>
        <li><strong>API Integration:</strong> Seamlessly integrate ContextDB into RAG (Retrieval-Augmented Generation) applications.</li>
        <li><strong>Embedding Generation:</strong> Create high-quality embeddings from downloaded documentation, optimizing retrieval and context understanding.</li>
        <li><strong>Real-time Updates:</strong> Stay current with the latest changes in technology documentation.</li>
      </ul>
    </section>
    <section>
      <h2>Embedding Feature (Beta)</h2>
      <p>We're currently exploring an embedding feature to enhance our context retrieval capabilities:</p>
      <ul>
        <li>Currently in beta, using ChromaDb as a proof of concept</li>
        <li>Aims to improve semantic search and context understanding</li>
        <li>Potential for more efficient information retrieval for LLMs</li>
      </ul>
      <p>This experimental feature is part of our ongoing efforts to optimize ContextDB's performance and explore new possibilities in context management for LLMs.</p>
    </section>
  </div>
</template>

<style scoped>
.about {
  max-width: 100%;
  margin: 0;
  padding: 40px;
  line-height: 1.8;
  font-size: 18px;
  color: var(--text-active-color);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5em;
  color: var(--active-link-color);
  margin-bottom: 30px;
}

h2 {
  font-size: 1.8em;
  color: var(--active-link-color);
  margin-top: 30px;
  margin-bottom: 20px;
}

section {
  margin-bottom: 40px;
}

ul {
  padding-left: 20px;
}

li {
  margin-bottom: 10px;
}

strong {
  color: var(--active-link-color);
}
</style>