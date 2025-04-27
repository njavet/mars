<template>
  <div class="about-page">
    <h1>About MARS</h1>
    <p><strong>Version:</strong> {{ version }}</p>
    <div v-html="changelogHtml" class="changelog"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'
import pkg from '../../package.json'

marked.setOptions({
  breaks: false,
  gfm: true,
})
const version = ref(pkg.version)
const changelogHtml = ref('')

function normalizeMarkdown(text) {
  return text.replace(/(#+ .+)\n(?!\n|- )/g, '$1\n\n')
}

onMounted(async () => {
  const res = await fetch('/CHANGELOG.md')
  const text = await res.text()
  changelogHtml.value = marked(normalizeMarkdown(text))
})
</script>

<style scoped>
.about-page {
  padding: 2rem;
  color: white;
}

.changelog {
  background-color: #333;
  padding: 1rem;
  border-radius: 8px;
  white-space: pre-wrap;
  font-size: 0.9rem;
  overflow-y: auto;
}
</style>
