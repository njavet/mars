<template>
  <div class="home-container">
    <h1>Welcome to the Assistant Platform</h1>
    <p>
      This application lets you interact with different language models and evaluate their responses
      on medical documents.
    </p>
    <ul>
      <li><strong>Chatbot:</strong>Query a selected model with your own prompts.</li>
      <li><strong>Assistant:</strong>Send your document for evalation.</li>
    </ul>
    <p>
      Select a model from the sidebar and start exploring.
    </p>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home-container {
  padding: 2rem;
  color: white;
  line-height: 1.6;
  text-align: left;
}

ul {
  margin-top: 1rem;
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.5rem;
}
</style>