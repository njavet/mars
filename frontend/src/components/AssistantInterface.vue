<template>
  <div class="right-sidebar">
    <button @click="handleClick('option1')">Option 1</button>
    <button @click="handleClick('option2')">Option 2</button>
    <button @click="handleClick('option3')">Option 3</button>
  </div>
</template>

<script setup>
function handleClick(option) {
  console.log("Clicked:", option)
  // Emit or handle logic here
}
</script>

<style scoped>
.right-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 200px;
  height: 100vh;
  background-color: #222;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
  gap: 1rem;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.3);
}

.right-sidebar button {
  width: 80%;
  padding: 0.5rem;
  border: none;
  background-color: #444;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.right-sidebar button:hover {
  background-color: #666;
}
</style>
