<script setup>
const props = defineProps({
    title: String,
    action: String
})
const emit = defineEmits(['create'])
</script>

<template>
    <main>
        <header>
            <h1>{{ title }}</h1>
            <button @click.stop="() => emit('create', '')">{{ action }}</button>
        </header>
        <table>
            <slot></slot>
        </table>
    </main>
</template>

<style>

main {
    margin: 1rem;
    padding: 1.5rem;
    background-color: var(--clr-background-main);
    color: #232c3b;
    border-radius: 1.25rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

header {
    width: 100%;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

button {
    background: var(--clr-background-button);
    color: var(--clr-text-button);
    border: none;
    outline: none;
    border-radius: .75rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
}

table {
    width: 100%;
    border-spacing: 0;
    border-collapse: collapse;
    text-align: center;
}
th {
    background-color: #f5f7fb;
    padding: 1rem 0 1rem;
    color: black;
}

th:first-child {
    border-top-left-radius: .75rem;
    border-bottom-left-radius: .75rem;
}

th:last-child {
    border-top-right-radius: .75rem;
    border-bottom-right-radius: .75rem;
}

td {
    position: relative;
    padding: 1.4rem 0 1.4rem;
    font-weight: 500;
}

tbody>tr:not(:last-child) {
    border-bottom: 1px solid #f5f7fb;
}
</style>